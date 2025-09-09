# Medical Chatbot Application

A web-based application that provides medical assistance through chat, symptom checking, document management, and emergency services. The application ensures secure access through login and registration while allowing critical features like emergency calls without authentication.

---

## Table of Contents

- [Login/Register Page](#loginregister-page)
- [Medical Chat Assistance](#medical-chat-assistance)
- [Basic Symptom Checker](#basic-symptom-checker)
- [Document Management](#document-management)
- [Medical Document Analysis (RAG Mode)](#medical-document-analysis-rag-mode)
- [Emergency Call](#emergency-call)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)

---

## Login/Register Page

The application implements a secure login and registration system to control access:

- **Registration Required:** New users must register by providing a username, email, and password.
- **Login:** Registered users can log in to access all features.
- **Access Control:** Only authenticated users can access most features. Unauthenticated users can only use the emergency call feature.
- **Security:** Passwords are securely hashed and session management ensures safe user authentication.

---

## Medical Chat Assistance

A chatbot feature that allows users to interact with the system for medical advice:

- Users can ask questions about symptoms, medications, or general health.
- The chatbot provides relevant and accurate responses.
- Responses are generated using a combination of predefined medical knowledge and AI-powered assistance.
- Accessible only to registered and logged-in users.

---

## Basic Symptom Checker

A simple tool to help users understand possible causes of symptoms:

- Users input their symptoms into the system.
- The tool provides suggestions or possible conditions based on the input.
- Works as a **first-level assessment** and does not replace professional medical advice.
- Available only to authenticated users.

---

## Document Management

Allows users to securely upload, store, and manage medical documents:

- Users can upload medical reports, prescriptions, or test results.
- Documents are stored securely in the backend.
- Users can view, download, or delete documents.
- Only accessible after login.

---

## Medical Document Analysis (RAG Mode)

RAG (Retrieval-Augmented Generation) mode provides advanced analysis of medical documents:

- Users can upload a medical document for detailed analysis.
- The system extracts relevant information and generates insights.
- Combines retrieval of existing knowledge with AI-generated summaries.
- Enhances decision-making by providing context-aware responses.
- Requires authentication to access.

---

## Emergency Call

A critical feature accessible to all users, even without login:

- Allows users to make an **emergency call** instantly.
- Ensures quick access to emergency services when needed.
- Always available, regardless of authentication status.

---

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/medical-chatbot-app.git
   cd medical-chatbot-app
