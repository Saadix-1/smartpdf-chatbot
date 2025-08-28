# Saad's SmartPDF Chatbot

Saad's SmartPDF Chatbot is a local AI-powered assistant that lets you interact with your PDF documents through natural language queries. It uses **Ollama** to run the LLM locally, combined with **FAISS** for semantic search over document embeddings. This makes it fully private, fast, and independent from cloud services.

## Features

* **Local AI**: Runs entirely on your machine with Ollama, ensuring privacy and no external dependencies.
* **PDF Understanding**: Extracts and processes PDF text for efficient semantic search.
* **Vector Search**: Uses FAISS to store and retrieve embeddings for accurate, context-aware answers.
* **Natural Interaction**: Query your documents in plain English and receive clear, concise responses.
* **Lightweight & Modular**: Simple Python scripts, easy to adapt for other use cases.

## Tech Stack

* **Python**
* **FAISS** (vector database for embeddings)
* **PyMuPDF** (PDF text extraction)
* **Ollama** (local LLM engine)
* **Flask** (API layer for queries)

## Demo

<img width="1508" height="863" alt="Screenshot 2025-08-28 at 23 03 50" src="https://github.com/user-attachments/assets/df02fb97-b5f9-4a0d-855c-e603ee69445e" />
<img width="1508" height="863" alt="Screenshot 2025-08-28 at 23 06 15" src="https://github.com/user-attachments/assets/dcd9bacc-3034-4e6e-be0d-5bbc738c46f1" />
<img width="1508" height="863" alt="Screenshot 2025-08-28 at 23 09 02" src="https://github.com/user-attachments/assets/9fa16e4f-370f-47fd-9b0d-a057f4290e7f" />



## Project Structure

```
smartpdf-chatbot/
│
├── scripts/
│   ├── embed_text.py      # Create embeddings from PDFs
│   ├── query_engine.py    # Query the FAISS index using Ollama
│
├── app.py                 # Flask API for local interaction
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/smartpdf-chatbot.git
   cd smartpdf-chatbot
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the embedding script on your PDF:

   ```bash
   python scripts/embed_text.py your_file.pdf
   ```

4. Start querying your PDF:

   ```bash
   python scripts/query_engine.py "Summarize this PDF"
   ```

5. (Optional) Launch the Flask API:

   ```bash
   python app.py
   ```

## Why This Project Matters

* Demonstrates skills in **LLM integration**, **vector databases**, and **backend APIs**.
* Showcases ability to build **practical AI tools** with focus on **privacy** and **local-first architecture**.
* Relevant to roles in **AI engineering**, **software development**, and **data-driven applications**.

---
## Future Improvements

* Support for multiple file formats (DOCX, TXT).
* Advanced UI features such as chat history and multi-file search.
* Deployment on cloud platforms (Heroku, AWS, etc.).

## License

This project is licensed under the MIT License.

---


        
   
   
      
  
   
        
  
   
 
 
