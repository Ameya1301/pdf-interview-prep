import logging
import os
from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.templating import Jinja2Templates
from pypdf.errors import PyPdfError

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

app = FastAPI()
templates = Jinja2Templates(directory=ROOT / "templates")
logger = logging.getLogger(__name__)
MAX_PDF_BYTES = 20 * 1024 * 1024


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/upload")
def upload(pdf_file: UploadFile = File(...)):
    filename = (pdf_file.filename or "").replace("\\", "/").rsplit("/", 1)[-1]

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(415, "Choose a PDF file.")

    if pdf_file.size is not None and pdf_file.size > MAX_PDF_BYTES:
        raise HTTPException(413, "Choose a PDF that is 20 MB or smaller.")

    if b"%PDF-" not in pdf_file.file.read(1024):
        raise HTTPException(415, "This file is not a valid PDF.")
    pdf_file.file.seek(0)

    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(503, "Set OPENAI_API_KEY in your .env file.")

    items = []
    with TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / "upload.pdf"
        with pdf_path.open("wb") as target:
            copyfileobj(pdf_file.file, target)

        try:
            from src.helper import llm_pipeline

            answer_chain, questions = llm_pipeline(str(pdf_path))
            for question in questions:
                result = answer_chain.invoke({"query": question})
                items.append({
                    "question": question,
                    "answer": result["result"],
                    "pages": [],
                })
        except PyPdfError as exc:
            raise HTTPException(422, "The PDF could not be read.") from exc
        except Exception as exc:
            logger.exception("Study guide generation failed")
            raise HTTPException(
                502, "Study guide generation failed. Check the terminal."
            ) from exc

    if not items:
        raise HTTPException(502, "No questions were generated. Try a different PDF.")

    return {"filename": filename, "items": items}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)