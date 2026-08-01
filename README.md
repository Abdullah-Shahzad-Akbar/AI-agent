# Abdullah GPT

Abdullah GPT is an AI-powered chatbot built with **FastAPI**, **LangChain**, **LangGraph**, **Groq**, **Google Gemini**, **Ollama**, and **ChromaDB**. It supports conversational AI, document processing (PDF/CSV), image understanding, internet search, and chat history.

---

# Prerequisites

Before running the project, make sure you have:

* Python 3.10 or later installed
* Git (optional, for cloning the repository)

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Or download the project as a ZIP file and extract it.

---

## 2. Install the required dependencies

This project includes a `requirements.txt` file containing all required packages.

Run the following command from the project folder:

```bash
pip install -r requirements.txt
```

---

## 3. Configure environment variables

Create a `.env` file in the project root and add your API keys.

Example:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
SECRET_KEY=your_secret_key
TAVILY_API_KEY=your_tavily_api_key
```

---

# Running the application

Open the project folder in your terminal.

Run the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

If the server starts successfully, you should see output similar to:

```text
Uvicorn running on http://0.0.0.0:8000
```

Open your browser and visit:

```
http://127.0.0.1:8000
```

or

```
http://localhost:8000
```

---

# Features

* AI chatbot with streaming responses
* User registration and login
* Conversation history
* PDF question answering
* CSV analysis
* Image understanding
* Internet search integration
* Retrieval-Augmented Generation (RAG) using ChromaDB
* Markdown-formatted responses

---

# Project Structure

```text
.
├── main.py
├── agent_test.py
├── database.py
├── Chromadb.py
├── pdf_to_text.py
├── csv_functions.py
├── binary_convertor.py
├── dict_convertor.py
├── filename.py
├── requirements.txt
├── templates/
├── static/
├── files/
├── text_of_pdf/
└── .env
```

---

# Notes

* Install all dependencies from `requirements.txt` before running the project.
* The `files/` and `text_of_pdf/` directories are created automatically if they do not already exist.
* Ensure your API keys are correctly configured in the `.env` file before starting the server.

---

# License

This project is provided for educational and personal use.
.
