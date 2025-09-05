#  Saad's Smart PDF Chatbot
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow?logo=javascript&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-blue?logo=flask&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.85%2B-green?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.0%2B-blue?logo=react&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Search-orange?logo=apache&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.20%2B-red?logo=adobe&logoColor=white)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-2.2%2B-blueviolet?logo=huggingface&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue?logo=postgresql&logoColor=white)
---

 **Smart PDF Chatbot** is an intelligent chatbot application that leverages advanced NLP techniques and large language models (LLMs) to interact with users based on the content of uploaded PDF documents. It uses **Ollama** to run the LLM locally. This project demonstrates expertise in modern AI, backend development, and deployment, making it a great showcase for your skills.

---


## **Features**

- **PDF Content Extraction**: Extracts and processes text from uploaded PDF files using `PyMuPDF`.
- **Semantic Search**: Uses `FAISS` for efficient similarity search on document embeddings.
- **Large Language Model Integration**: Employs GPT-based models for generating intelligent responses.
- **Database Integration**: Stores metadata and embeddings in PostgreSQL for persistence.
- **Web Interface**: User-friendly frontend built with React for uploading PDFs and interacting with the chatbot.

---
##  **Getting Started**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Heroku CLI (for deployment)

##  **Technologies Used**

### **Backend**
- **Flask** or **FastAPI**: For building the REST API.
- **FAISS**: For fast similarity search on embeddings.
- **PyMuPDF**: For extracting text from PDFs.
- **SentenceTransformers**: For generating embeddings from text.
- **PostgreSQL**: For storing metadata and embeddings.

### **Frontend**
- **React**: For building the web interface.
- **Axios**: For making API calls to the backend.

## 📂 **Project Structure**

```
smart-pdf-chatbot/
├── backend/
│   ├── app.py               # Flask/FastAPI app
│   ├── scripts/
│   │   ├── extract_pdf.py # Extracts text from PDFs
│   │   ├── embed_text.py    # Generates and saves embeddings
│   │   ├── query_engine.py   # Engine
│   │   ├── store_embeddings_pg.py # Store embedding using pgvector
│   └── requirements.txt     # Backend dependencies
├── smartpdf-frontend/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css         # Main React component
│   │   ├── components/      # React components
│   ├── package.json         # Frontend dependencies
├── workflows/
│   ├── n8n_workflows.json   # Automation workflows
├── Procfile                 # Heroku deployment configuration
├── README.md                # Project documentation
```

---



### **Backend Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/Saadix-1/smart-pdf-chatbot.git
   cd smart-pdf-chatbot/backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Set up environment variables for PostgreSQL:
   ```bash
   export DATABASE_URL=postgresql://username:password@localhost/dbname
   ```
4. Run the backend server:
   ```bash
   python app.py
   ```

### **Frontend Setup**
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`.

---

## Demo

<img width="1508" height="863" alt="Screenshot 2025-08-28 at 23 03 50" src="https://github.com/user-attachments/assets/df02fb97-b5f9-4a0d-855c-e603ee69445e" />
<img width="1508" height="863" alt="Screenshot 2025-08-28 at 23 06 15" src="https://github.com/user-attachments/assets/dcd9bacc-3034-4e6e-be0d-5bbc738c46f1" />
<img width="1508" height="863" alt="Screenshot 2025-08-28 at 23 09 02" src="https://github.com/user-attachments/assets/9fa16e4f-370f-47fd-9b0d-a057f4290e7f" />


## 🧪 **Testing**

### **Backend Tests**
- Add unit tests for PDF extraction, embedding generation, and FAISS operations.
- Run tests using `pytest`:
  ```bash
  pytest
  ```

### **Frontend Tests**
- Includes a basic test suite for React components using `@testing-library/react`.
- Run tests:
  ```bash
  npm test
  ```
---

##  **Key Functionalities**

### **1. PDF Content Extraction**
- Extracts text from PDFs using `PyMuPDF`.
- Preprocesses text for embedding generation.

### **2. Embedding Generation**
- Generates embeddings for text chunks using `SentenceTransformers`.
- Stores embeddings in a FAISS index for efficient similarity search.

### **3. Chatbot Query**
- Accepts user queries and retrieves relevant text chunks using FAISS.
- Sends the retrieved text to the GPT-based LLM for generating responses.

### **4. Web Interface**
- Allows users to upload PDFs and interact with the chatbot.
- Displays chatbot responses in a user-friendly format.


##  **Why This Project Stands Out**

- **End-to-End Solution**: Combines backend, frontend, and automation into a cohesive application.
- **Modern AI Techniques**: Demonstrates expertise in NLP, embeddings, and LLMs.
- **Scalable Architecture**: Designed with modularity and scalability in mind.
- **Cloud Deployment**: Fully deployed and accessible online.

---
## Future Improvements

* Support for multiple file formats (DOCX, TXT).
* Advanced UI features such as chat history and multi-file search.
* Deployment on cloud platforms (Heroku, AWS, etc.)
* Automation using n8n .

## License

This project is licensed under the MIT License.
## 🤝 **Contributing**

Contributions are welcome! If you have ideas for improving this project, feel free to fork the repository and submit a pull request.

---


   
        
  
   
 
 
