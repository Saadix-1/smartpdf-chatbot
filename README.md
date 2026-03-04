# Saad AI (Smart PDF Chatbot)
![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-ES6%2B-blue?logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18.0%2B-blue?logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.0%2B-purple?logo=vite&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-blueviolet?logo=database&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT_3.5_&_Embeddings-green?logo=openai&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.20%2B-red?logo=adobe&logoColor=white)

---

**Saad AI** is a modernized, cloud-native chatbot application that leverages advanced NLP techniques and large language models (LLMs) to interact with users based on the content of uploaded PDF documents. 

Re-architected from local LLMs to a fully stateless cloud deployment model using **OpenAI** and **Pinecone**, this project demonstrates expertise in building scalable, enterprise-ready AI backends and modern React frontends.

---

## **Features**

- **Cloud-Native & Stateless Processing**: Extracts and processes text from uploaded PDF files directly via memory streams. No local disk persistence is required, meaning it operates perfectly on serverless infrastructure like Google Cloud Run or AWS Fargate.
- **Managed Vector Database**: Uses **Pinecone** for extremely fast and reliable similarity search on document embeddings without the overhead of maintaining local FAISS indices.
- **State-of-the-Art LLMs**: Employs OpenAI's `gpt-3.5-turbo` for generating intelligent responses, and `text-embedding-3-small` for generating highly accurate dense vector embeddings.
- **Fast Web Interface**: A sleek, user-friendly frontend built with React, Vite, and Tailwind CSS for instant answers and fluid interactions.

---

## **Technologies Used**
 
### **Backend**
- **FastAPI**: For building the lightning-fast asynchronous REST API.
- **Pinecone**: Managed vector database for semantic search.
- **OpenAI API**: For semantic embeddings and LLM chat completions.
- **PyMuPDF (`fitz`)**: For rapid, highly accurate text extraction from PDFs.

### **Frontend**
- **React 18 & Vite**: High-performance frontend rendering framework and dev server.
- **Tailwind CSS**: For crafting a rich, dynamic, and responsive aesthetic.
- **Lucide Icons**: Crisp, SVG-based interface iconography.

---

## 📂 **Project Structure**

```
smartpdf-chatbot/
├── backend/
│   ├── app/                 # FastAPI application and routes
│   │   ├── main.py          # Application entry point
│   │   ├── api/             # REST Endpoints (upload, chat)
│   │   ├── core/            # Configuration and Application State
│   │   └── services/        # Business Logic (Pinecone, OpenAI, PDF Extraction)
│   ├── requirements.txt     # Python Dependencies
│   └── .env.example         # Template for required cloud API keys
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React web UI interface
│   │   ├── components/      # Reusable React components
│   │   ├── index.css        # Global Tailwind CSS definitions
│   ├── package.json         # Node Dependencies
│   └── vite.config.ts       # React Bundler Configuration
├── docker-compose.yml       # Stateless container deployment manifest
├── README.md                # Project documentation
```

---

##  **Getting Started Locally**

To run Saad AI locally, you will need active API keys from the respective cloud providers. 

### **Prerequisites**
- Node.js v20+
- Python 3.10+
- An [OpenAI Developer Account](https://platform.openai.com) & API Key
- A [Pinecone Account](https://app.pinecone.io) & API Key (Free Tier supported)

### **Backend Setup**
1. Clone the repository and navigate to the backend:
   ```bash
   git clone https://github.com/Saadix-1/smartpdf-chatbot.git
   cd smartpdf-chatbot/backend
   ```
2. Create your environment configuration file:
   ```bash
   touch .env
   ```
3. Open the `.env` file and insert your cloud API credentials:
   ```env
   OPENAI_API_KEY=sk-proj-your_openai_api_key_here
   PINECONE_API_KEY=pcsk_your_pinecone_api_key_here
   PINECONE_INDEX_NAME=smartpdf-index
   ```
4. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Run the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### **Frontend Setup**
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd smartpdf-chatbot/frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to `http://localhost:5173`. You can now upload PDFs and interact with Saad AI!

---
## Demo
<img width="1512" height="855" alt="Screenshot 2026-03-04 at 14 27 22" src="https://github.com/user-attachments/assets/73a077cd-f373-49aa-90c8-75a62286b412" />

##  **Deployment in the Cloud**

Because the application is entirely stateless and does not rely on local SQL databases or persistent mounted volumes, it is exceptionally easy to deploy:

1. **Frontend Hosting (Vercel / Netlify / Firebase)**: Run `npm run build` and deploy the output static assets (`/dist`) directly to any global CDN.
2. **Backend Hosting (Google Cloud Run / AWS AppRunner)**: Package the backend into a Docker container using the provided `Dockerfile`. Deploy the image as a serverless container, ensuring you pass the `OPENAI_API_KEY` and `PINECONE_API_KEY` configuration variables directly into your cloud provider's secret manager or environment variables.

---

##  **Why This Project Stands Out**

- **Production-Ready Architecture**: Shifted from local monolithic state to a scalable microservice architecture utilizing managed services.
- **Stateless Engineering**: Designed with ephemeral disks in mind; PDFs and database connections are handled strictly in memory and over HTTP APIs.
- **Modern AI Techniques**: Demonstrates expertise building around leading Enterprise models instead of slower local deployments.
- **Beautiful User Interface**: A bespoke, premium dynamic design using cutting-edge CSS tools.

---

## License

This project is licensed under the MIT License.

## 🤝 **Contributing**

Contributions are welcome! If you have ideas for improving this project, feel free to fork the repository and submit a pull request.
