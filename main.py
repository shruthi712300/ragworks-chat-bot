from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
from typing import List, Optional

from models import get_session_local, create_tables, User, Conversation, Document, Message
from auth import get_current_user, create_access_token, get_password_hash, verify_password
from rag import process_document, query_rag_system, init_vector_store
from llm import generate_response, train_custom_model, medical_disclaimer
from email_service import send_email_notification

# Initialize database tables and vector store
create_tables()
init_vector_store()

# Create FastAPI app
app = FastAPI(
    title="Medical Information Chatbot API",
    version="1.0.0",
    description="An API for medical Q&A with RAG, authentication, and document uploads."
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database session dependency
def get_db():
    DBSession = get_session_local()
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    sources: List[str] = []

# Root endpoint (so "/" doesn’t return Not Found)
@app.get("/")
def root():
    return {"message": "✅ Medical Information Chatbot API is running. Visit /docs to explore available endpoints."}

# User registration
# @app.post("/register")
# def register(user: UserCreate, db: Session = Depends(get_db)):
#     if db.query(User).filter(User.username == user.username).first():
#         raise HTTPException(status_code=400, detail="Username already exists")
#     if db.query(User).filter(User.email == user.email).first():
#         raise HTTPException(status_code=400, detail="Email already exists")
#     hashed = get_password_hash(user.password)
#     new_user = User(username=user.username, email=user.email, hashed_password=hashed)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User created successfully"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check for existing username
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=409, detail="Username already exists")

    # Check for existing email
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    # Create new user
    hashed = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# Upload medical document
@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    content = await file.read()
    os.makedirs("documents", exist_ok=True)
    filename = f"documents/{current_user.id}_{file.filename}"
    with open(filename, "wb") as f:
        f.write(content)
    doc_count = process_document(filename, current_user.id, file.filename)
    new_doc = Document(user_id=current_user.id, filename=file.filename, storage_path=filename, processed=True)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return {"message": "Document uploaded and processed", "document_chunks": doc_count}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(
    message: ChatMessage,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Start or continue conversation
    if not message.conversation_id:
        conv = Conversation(user_id=current_user.id, title=message.message[:50])
        db.add(conv)
        db.commit()
        db.refresh(conv)
        conversation_id = conv.id
    else:
        conversation_id = message.conversation_id

    # Query RAG + generate response
    context, sources = query_rag_system(message.message, current_user.id)
    llm_resp = generate_response(message.message, context)
    llm_resp = f"""{llm_resp}\n\n{medical_disclaimer()}"""

    # Save conversation messages
    msg_user = Message(conversation_id=conversation_id, role="user", content=message.message)
    msg_assistant = Message(conversation_id=conversation_id, role="assistant", content=llm_resp)
    db.add(msg_user)
    db.add(msg_assistant)
    db.commit()

    # Optional: send email notifications
    if os.getenv("EMAIL_NOTIFICATIONS", "false").lower() == "true":
        background_tasks.add_task(
            send_email_notification,
            current_user.email,
            "New medical chat response",
            llm_resp
        )

    return ChatResponse(response=llm_resp, conversation_id=str(conversation_id), sources=sources)


