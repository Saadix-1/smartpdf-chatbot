from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
from ..services.pdf_service import extract_text_from_pdf
from ..services.vector_store import vector_store
from ..services.llm_service import query_ollama

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    response: str
    context: list[str] = []

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
        
    try:
        # Read file into memory (Warning: very large PDFs might stress memory,
        # but suitable for MVP serverless deployments)
        pdf_bytes = await file.read()
            
        text = extract_text_from_pdf(pdf_bytes)
        if not text:
             raise HTTPException(status_code=400, detail="Could not extract text from PDF")
             
        vector_store.process_pdf(text)
        
        return {"message": "PDF processed and indexed successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    context_chunks = vector_store.search(request.question)
    
    if not context_chunks:
        return ChatResponse(response="No context found. Please upload a PDF first.", context=[])
        
    context_text = "\n\n".join(context_chunks)
    prompt = f"Context:\n{context_text}\n\nQuestion: {request.question}\nAnswer:"
    
    response_text = query_ollama(prompt)
    
    return ChatResponse(response=response_text, context=context_chunks)
