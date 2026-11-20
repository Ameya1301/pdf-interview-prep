# PDF Interview Prep

PDF Interview Prep is a web app that turns text-based PDFs into practice questions and answers. Upload course notes or technical documentation, review the generated answers in collapsible cards, or download the full study guide as a CSV.

## Features

- Upload or drag and drop a PDF up to 20 MB.
- See a loading indicator while the study guide is being generated.
- Expand answers individually or open the whole guide at once.
- Export questions and answers as a CSV for offline review.

## Run locally

You’ll need Conda and an OpenAI API key.

1. From the project root, create and activate the Conda environment, then install the dependencies.

   ```bash
   conda create -n interview python=3.11 -y
   conda activate interview
   python -m pip install -r requirements.txt
   ```

2. Create a `.env` file next to `app.py` and add your OpenAI API key. Add `.env` to `.gitignore` before committing.

   ```dotenv
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Start the app.

   ```bash
   python app.py
   ```

4. Open [http://127.0.0.1:8080](http://127.0.0.1:8080), upload a PDF, and select **Generate study guide**. Try [`data/stats.pdf`](data/stats.pdf) for a quick test.

Use a PDF with selectable text. The app sends extracted text to OpenAI to generate questions, embeddings, and answers.

## How it works

1. PyPDF extracts the text, and LangChain splits it into chunks.
2. An OpenAI model drafts questions from the first chunk and refines the list with additional chunks.
3. The app embeds smaller passages, indexes them with FAISS, and retrieves relevant passages for each question.
4. FastAPI returns the questions and answers to the browser for review and CSV export.

## Project structure

| Path | Purpose |
| --- | --- |
| [`app.py`](app.py) | FastAPI entry point and PDF upload route |
| [`src/helper.py`](src/helper.py) | PDF processing, question generation, and answer retrieval |
| [`src/prompt.py`](src/prompt.py) | Prompts for drafting and refining questions |
| [`templates/index.html`](templates/index.html) | Web interface, styles, and CSV export |
| [`research/experiment.ipynb`](research/experiment.ipynb) | Notebook used to prototype the study guide workflow |
| [`requirements.txt`](requirements.txt) | Python dependencies |
