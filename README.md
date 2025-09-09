# Medical Chatbot Application

The Medical Chatbot Application provides intelligent healthcare assistance through a user-friendly platform. It offers chat assistance powered by the Gemini API for accurate and interactive medical guidance. A quick symptom checker helps users assess their health conditions efficiently. The app supports medical document analysis in RAG mode, offering AI-driven insights from uploaded reports. Document management allows secure storage and easy access to medical report softcopies. An emergency call feature triggers automatic calls without requiring login, ensuring instant access to help in critical situations.

---

## Login/Register

The application implements a secure login and registration system to control access:

The application uses a secure user authentication system to manage access.
New users must register with a username, email, and password to gain full access.
Registered users can log in to utilize all features of the application.
Access control ensures that non-logged-in users cannot access app functionalities, except for the emergency call, which remains available at all times.
Passwords are securely hashed, and session management guarantees that only authenticated users can interact with the system.

---

## Medical Chat Assistance

A chatbot feature that allows users to interact with the system for medical advice:

The application includes a chat-based medical assistant powered by the Gemini API.
Users can ask questions about symptoms, medications, and general health concerns.
The system provides accurate and interactive responses, combining AI-powered guidance with medical knowledge.
This feature is designed for registered and logged-in users, ensuring secure and personalized assistance.
It enhances patient engagement by offering real-time support and quick medical guidance in a conversational format.

---

## Basic Symptom Checker

A simple tool to help users understand possible causes of symptoms:

The application provides a checkbox-based selection panel to quickly choose common symptoms without typing them manually.

Available Options in the UI:

✅ Fever (pre-selected in screenshot)
⬜ Cough
⬜ Shortness of Breath
⬜ Fatigue
⬜ Headache
⬜ Chest Pain
⬜ Nausea
⬜ Dizziness

---

## Document Management

The Document Management module allows uploading of clinical documents (guidelines, protocols, research papers).
Users can upload files by drag & drop or browsing (supports PDF, TXT, DOCX, CSV up to 200MB).
Upload Options include immediate processing and text extraction.
A progress bar shows the upload status, and successful uploads are confirmed with a green notification.
The interface displays the uploaded file details (name, size) and confirms processing completion.

---

## Medical Document Analysis (RAG Mode)

RAG (Retrieval-Augmented Generation) mode provides advanced analysis of medical documents:

The Medical Information Chatbot supports Medical Document Analysis (RAG Mode) to extract structured medical data using AI.
Users can upload medical documents via drag & drop or file browsing (PDF, DOCX, TXT, up to 200MB).
Analysis Options allow selecting the type of extraction (e.g., Comprehensive Medical Extraction).
A main action button (Extract Medical Information) triggers the analysis process.
Quick Analysis Templates are available to directly extract specific details such as Diagnoses, Medications, and Lab Results.

---

## Emergency Call

A critical feature accessible to all users, even without login:
The Medical Information Chatbot provides an Emergency Notifications feature for urgent situations.
Users can initiate an emergency call directly through the interface with a single click.
A confirmation message appears once the call is successfully triggered.
In the automatic emergency call triggering system, login is not even required, ensuring faster response during emergencies.

---

## Setup and Installation


## ⚙️ Backend Installation

1. **Clone the Repository**

   ```bash
   git clone <repo-url>
   cd backend
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Backend Server**

   ```bash
   uvicorn app.main:app --reload
   ```

   > Replace `app.main:app` with your actual entry point (e.g., Flask or Django command).

📌 Backend runs at: **[http://localhost:8000](http://localhost:8000)**

---

## 💻 Frontend Installation

1. **Navigate to Frontend Directory**

   ```bash
   cd frontend
   ```

2. **Install Node.js Packages**

   ```bash
   npm install
   ```

3. **Set Environment Variables (if needed)**
   Create a `.env` file in the frontend folder with:

   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Run the Frontend**

   ```bash
   npm start
   ```

📌 Frontend runs at: **[http://localhost:3000](http://localhost:3000)**

---

## ✅ System Workflow

* **Backend** → Runs on `http://localhost:8000` (serves API requests).
* **Frontend** → Runs on `http://localhost:3000` (UI layer, communicates with backend).

---

## 🚀 Features

* 🔍 **Symptom Checker** – Enter symptoms and view possible conditions.
* 📄 **Document Management** – Upload, process, and extract medical data.
* 🧠 **Medical Document Analysis (RAG Mode)** – Extract diagnoses, medications, and lab results using AI.
* 📞 **Emergency Notifications** – Trigger emergency calls instantly (no login required for automatic triggers).

---

## APPLICATION OUTPUTS

<img width="1845" height="900" alt="Screenshot 2025-09-09 210640" src="https://github.com/user-attachments/assets/0aa26431-e6a4-4d1c-8f28-0760c7e819b8" />

<img width="1853" height="898" alt="Screenshot 2025-09-09 210620" src="https://github.com/user-attachments/assets/00eae556-a538-4ed0-bdae-7fdb719afd9d" />

<img width="1854" height="906" alt="Screenshot 2025-09-09 210510" src="https://github.com/user-attachments/assets/cc0f6470-7bfd-4363-b795-448a7716b482" />

<img width="1846" height="910" alt="Screenshot 2025-09-09 210456" src="https://github.com/user-attachments/assets/493c0d7f-6a73-4101-9ada-2b8081082b89" />

<img width="1848" height="949" alt="Screenshot 2025-09-09 210412" src="https://github.com/user-attachments/assets/ed332c67-a0c9-49c7-9b0d-e7cc01472906" />

<img width="1863" height="956" alt="Screenshot 2025-09-09 210241" src="https://github.com/user-attachments/assets/590f0451-b663-4b0f-b29b-aff4a98901ea" />






