from setuptools import find_packages, setup

setup(
    name="Generative AI project",
    version="0.1.0",
    author="Ameya Warade",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "aiofiles",
        "jinja2",
        "langchain",
        "openai",
        "faiss-cpu"
    ]
)