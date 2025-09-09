# Medical Chatbot Application

The Medical Chatbot Application provides intelligent healthcare assistance through a user-friendly platform. It offers chat assistance powered by the Gemini API for accurate and interactive medical guidance. A quick symptom checker helps users assess their health conditions efficiently. The app supports medical document analysis in RAG mode, offering AI-driven insights from uploaded reports. Document management allows secure storage and easy access to medical report softcopies. An emergency call feature triggers automatic calls without requiring login, ensuring instant access to help in critical situations.

---

## Login/Register Page

The application implements a secure login and registration system to control access:

The application uses a secure user authentication system to manage access.
New users must register with a username, email, and password to gain full access.
Registered users can log in to utilize all features of the application.
Access control ensures that non-logged-in users cannot access app functionalities, except for the emergency call, which remains available at all times.
Passwords are securely hashed, and session management guarantees that only authenticated users can interact with the system.
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
