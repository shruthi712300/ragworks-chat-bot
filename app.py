import streamlit as st
import requests
import pandas as pd
import json
import tempfile
import os
from PyPDF2 import PdfReader
import docx
import io


from notify import  trigger_bland_call


# ==========================
# Configuration
# ==========================
# API_BASE = st.secrets.get('API_BASE', 'http://localhost:8000')
API_BASE = os.getenv("API_BASE", "http://localhost:8000")


st.set_page_config(page_title=' MediWise', layout='wide', page_icon='🩺')

# ==========================
# Session State Initialization
# ==========================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'conversation_id' not in st.session_state:
    st.session_state['conversation_id'] = None
if 'uploaded_documents' not in st.session_state:
    st.session_state['uploaded_documents'] = []
if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = ""

# ==========================
# Authentication Functions
# ==========================
# def register_user(username, email, password):
#     """Register a new user"""
#     try:
#         r = requests.post(f"{API_BASE}/register", json={'username': username, 'email': email, 'password': password})
#         return r.status_code == 200 or r.status_code == 201
#     except:
#         return False

def register_user(username, email, password):
    """Register a new user with proper error handling"""
    try:
        r = requests.post(
            f"{API_BASE}/register",
            json={'username': username, 'email': email, 'password': password}
        )
        if r.status_code in [200, 201]:
            return True
        else:
            # Show actual backend error
            try:
                error_detail = r.json().get('detail', r.text)
            except Exception:
                error_detail = r.text
            st.error(f"❌ Registration failed: {error_detail}")
            return False
    except Exception as e:
        st.error(f"❌ Could not contact backend: {str(e)}")
        return False


def login_user(username, password):
    """Login user and store token"""
    try:
        r = requests.post(f"{API_BASE}/login", data={'username': username, 'password': password})
        if r.status_code == 200:
            st.session_state['token'] = r.json().get('access_token')
            st.session_state['authenticated'] = True
            return True
        return False
    except:
        return False

def api_headers():
    """Generate API headers with authentication token"""
    headers = {}
    if st.session_state.get('token'):
        headers['Authorization'] = f"Bearer {st.session_state['token']}"
    return headers

# ==========================
# Document Processing Functions
# ==========================
def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"

def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        return file.getvalue().decode('utf-8')
    except Exception as e:
        return f"Error extracting TXT: {str(e)}"

def extract_medical_info_from_text(text):
    """Extract medical information using RAG mode"""
    if not st.session_state['authenticated']:
        return "Please login to use RAG features"
    
    prompt = f"""
    Extract comprehensive medical information from the following text. Organize it into structured categories:
    
    TEXT TO ANALYZE:
    {text[:4000]}  # Limit text length
    
    Please extract and structure the following information:
    1. Patient demographics (age, gender, etc.)
    2. Medical history
    3. Current symptoms
    4. Diagnoses
    5. Medications
    6. Lab results
    7. Treatment plans
    8. Recommendations
    9. Key medical findings
    
    Format the response in a clear, structured manner with headings.
    """
    
    try:
        headers = api_headers()
        data = {
            'message': prompt,
            'conversation_id': st.session_state.get('conversation_id')
        }
        r = requests.post(f"{API_BASE}/chat", json=data, headers=headers)
        
        if r.status_code == 200:
            result = r.json()
            return result.get('response', 'No response received.')
        else:
            return f"Error from API: {r.text}"
    except Exception as e:
        return f"Error contacting API: {str(e)}"

# ==========================
# API Functions
# ==========================
def upload_document(file):
    """Upload document to backend"""
    files = {'file': (file.name, file.getvalue(), file.type)}
    headers = api_headers()
    try:
        r = requests.post(f"{API_BASE}/upload-document", files=files, headers=headers)
        return r.json()
    except Exception as e:
        return {'error': f'Upload failed: {str(e)}'}

# def send_chat(message):
#     """Send chat message to backend"""
#     headers = api_headers()
#     data = {'message': message, 'conversation_id': st.session_state.get('conversation_id')}
#     try:
#         r = requests.post(f"{API_BASE}/chat", json=data, headers=headers)
#         if r.status_code == 200:
#             result = r.json()
#             # Update conversation ID if provided
#             if result.get('conversation_id'):
#                 st.session_state['conversation_id'] = result['conversation_id']
#             return result
#         return {'response': f'Error from backend: {r.text}', 'sources': []}
#     except Exception as e:
#         return {'response': f'Error contacting API: {str(e)}', 'sources': []}




import google.generativeai as genai

# Configure Gemini with your API key
genai.configure(api_key="AIzaSyDZknFNaZZn7TMzThLURx9bzcSS7AC0c-o")

# ==========================
# Chatbot Integration with Gemini
# ==========================
def send_chat(message):
    """Send chat message to Google Gemini API"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # You can use gemini-1.5-pro if needed
        response = model.generate_content(message)

        result_text = response.text if response and hasattr(response, "text") else "No response received."
        return {
            'response': result_text,
            'sources': []  # Gemini doesn’t return sources directly
        }
    except Exception as e:
        return {'response': f'Error contacting Gemini API: {str(e)}', 'sources': []}



def symptom_checker(symptoms_list):
    """Basic symptom checker with mock data"""
    mapping = {
        'fever': ['Influenza', 'COVID-19', 'Malaria', 'Bacterial infection'],
        'chest pain': ['Angina', 'Myocardial infarction', 'GERD', 'Pneumonia', 'Costochondritis'],
        'headache': ['Migraine', 'Tension headache', 'Cluster headache', 'SAH (rare)', 'Sinusitis'],
        'cough': ['Common cold', 'Bronchitis', 'Pneumonia', 'Asthma', 'COVID-19'],
        'shortness of breath': ['Asthma', 'Pneumonia', 'Heart failure', 'Anxiety', 'COPD'],
        'nausea': ['Gastroenteritis', 'Food poisoning', 'Pregnancy', 'Migraine', 'Appendicitis'],
        'fatigue': ['Anemia', 'Depression', 'Thyroid disorders', 'Sleep disorders', 'Viral infection'],
        'dizziness': ['Vertigo', 'Low blood pressure', 'Dehydration', 'Anemia', 'Inner ear problems']
    }
    
    suggestions = {}
    for s in symptoms_list:
        s_low = s.lower().strip()
        suggestions[s] = mapping.get(s_low, ['Consult clinician; broad differential diagnosis required.'])
    return suggestions

# ==========================
# Main UI
# ==========================
st.title('🩺 Medical Information Chatbot')

# Sidebar menu
# menu = st.sidebar.selectbox('Menu', ['Login/Register', 'Chat', 'Symptom Checker', 'Documents', 'RAG Medical Extraction', 'Settings'])

menu = st.sidebar.selectbox('Menu', [
    'Login/Register', 'Chat', 'Symptom Checker', 'Documents',
    'RAG Medical Extraction', 'Notifications', 'Settings'
])


# Authentication status in sidebar
if st.session_state['authenticated']:
    st.sidebar.success('✅ Authenticated')
    if st.sidebar.button('Logout'):
        st.session_state['authenticated'] = False
        st.session_state['token'] = None
        st.session_state['messages'] = []
        st.session_state['conversation_id'] = None
        st.session_state['uploaded_documents'] = []
        st.session_state['extracted_text'] = ""
        st.rerun()
else:
    st.sidebar.warning('❌ Not authenticated')

# ==========================
# Login/Register Page
# ==========================
if menu == 'Login/Register':
    st.header('🔐 Authentication')
    
    if not st.session_state['authenticated']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Login')
            with st.form("login_form"):
                user = st.text_input('Username')
                pwd = st.text_input('Password', type='password')
                login_submitted = st.form_submit_button('Login')
                
                if login_submitted:
                    if user and pwd:
                        ok = login_user(user, pwd)
                        if ok:
                            st.success('✅ Logged in successfully!')
                            st.rerun()
                        else:
                            st.error('❌ Login failed. Please check your credentials.')
                    else:
                        st.error('Please enter both username and password.')
        
        with col2:
            st.subheader('Register')
            with st.form("register_form"):
                r_user = st.text_input('New username')
                r_email = st.text_input('Email')
                r_pwd = st.text_input('Password', type='password')
                r_pwd_confirm = st.text_input('Confirm Password', type='password')
                register_submitted = st.form_submit_button('Register')
                
                if register_submitted:
                    if r_user and r_email and r_pwd and r_pwd_confirm:
                        if r_pwd == r_pwd_confirm:
                            ok = register_user(r_user, r_email, r_pwd)
                            if ok:
                                st.success('✅ Registered successfully! Please login.')
                            else:
                                st.error('❌ Registration failed. Username or email might already exist.')
                        else:
                            st.error('❌ Passwords do not match.')
                    else:
                        st.error('Please fill in all fields.')
    else:
        st.success('You are already logged in!')
        st.info('Use the sidebar menu to navigate to other features.')

# ==========================
# Chat Page
# ==========================
elif menu == 'Chat':
    st.header('💬 Medical Chat Assistant')
    st.info('Ask clinical questions (for healthcare professionals only)')
    
    if not st.session_state['authenticated']:
        st.warning('⚠️ Please login to use the chat feature.')
    else:
        # Chat history display
        chat_container = st.container()
        with chat_container:
            for m in st.session_state['messages']:
                if m['role'] == 'user':
                    st.markdown(f"**🧑 You:** {m['content']}")
                else:
                    st.markdown(f"**🤖 Assistant:** {m['content']}")
                    # Show sources if available
                    if 'sources' in m and m['sources']:
                        with st.expander("📚 Sources"):
                            for source in m['sources']:
                                st.write(f"- {source}")
        
        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            prompt = st.text_area('Enter your medical question:', 
                                placeholder='e.g., What are the treatment guidelines for hypertension?',
                                height=100)
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                send_button = st.form_submit_button('Send 📤')
            with col2:
                clear_button = st.form_submit_button('Clear Chat 🗑️')
            
            if send_button and prompt.strip():
                # Add user message
                st.session_state['messages'].append({'role': 'user', 'content': prompt})
                
                # Send to API
                with st.spinner('Getting response...'):
                    result = send_chat(prompt)
                
                # Add assistant response
                assistant_msg = {
                    'role': 'assistant', 
                    'content': result.get('response', 'No response received.'),
                    'sources': result.get('sources', [])
                }
                st.session_state['messages'].append(assistant_msg)
                st.rerun()
            
            if clear_button:
                st.session_state['messages'] = []
                st.session_state['conversation_id'] = None
                st.rerun()

# ==========================
# Symptom Checker Page
# ==========================
elif menu == 'Symptom Checker':
    st.header('🔍 Basic Symptom Checker')
    st.warning('⚠️ This is a basic educational tool. Always consult a healthcare professional for proper diagnosis.')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader('Enter Symptoms')
        symp = st.text_area('Enter symptoms (comma-separated)', 
                           placeholder='fever, headache, cough',
                           height=100)
        
        # Common symptoms quick select
        st.subheader('Quick Select Common Symptoms')
        common_symptoms = ['fever', 'headache', 'cough', 'chest pain', 'shortness of breath', 
                          'nausea', 'fatigue', 'dizziness']
        selected_symptoms = []
        
        cols = st.columns(2)
        for i, symptom in enumerate(common_symptoms):
            with cols[i % 2]:
                if st.checkbox(symptom.title(), key=f'symptom_{i}'):
                    selected_symptoms.append(symptom)
        
        if st.button('Check Symptoms 🔍', type='primary'):
            # Combine manual and selected symptoms
            manual_symptoms = [s.strip() for s in symp.split(',') if s.strip()]
            all_symptoms = list(set(manual_symptoms + selected_symptoms))
            
            if all_symptoms:
                res = symptom_checker(all_symptoms)
                
                with col2:
                    st.subheader('Possible Conditions')
                    for symptom, conditions in res.items():
                        st.write(f"**{symptom.title()}:**")
                        for condition in conditions:
                            st.write(f"  • {condition}")
                        st.write("")
                    
                    st.error('🚨 IMPORTANT: This is not a medical diagnosis. Please consult a healthcare professional for proper evaluation and treatment.')
            else:
                st.warning('Please enter or select at least one symptom.')

# ==========================
# Documents Page
# ==========================
elif menu == 'Documents':
    st.header('📄 Document Management')
    st.info('Upload clinical documents (guidelines, protocols, research papers)')
    
    if not st.session_state['authenticated']:
        st.warning('⚠️ Please login to upload documents.')
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded = st.file_uploader(
                'Upload medical documents', 
                type=['pdf', 'txt', 'docx', 'csv'],
                accept_multiple_files=True,
                help='Supported formats: PDF, TXT, DOCX, CSV'
            )
            
            if uploaded:
                st.write(f"Selected {len(uploaded)} file(s):")
                for file in uploaded:
                    st.write(f"• {file.name} ({file.size} bytes)")
        
        with col2:
            st.subheader('Upload Options')
            process_immediately = st.checkbox('Process immediately', value=True)
            extract_text = st.checkbox('Extract text content', value=True)
        
        if uploaded and st.button('Upload & Process 📤', type='primary'):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, file in enumerate(uploaded):
                status_text.text(f'Uploading {file.name}...')
                result = upload_document(file)
                
                progress_bar.progress((i + 1) / len(uploaded))
                
                if 'error' in result:
                    st.error(f"❌ Failed to upload {file.name}: {result['error']}")
                else:
                    st.success(f"✅ Successfully uploaded {file.name}")
                    if result.get('message'):
                        st.info(result['message'])
            
            status_text.text('Upload complete!')

# ==========================
# RAG Medical Extraction Page (NEW)
# ==========================
elif menu == 'RAG Medical Extraction':
    st.header('🔬 Medical Document Analysis (RAG Mode)')
    st.info('Upload medical documents to extract structured medical information using AI')
    
    if not st.session_state['authenticated']:
        st.warning('⚠️ Please login to use RAG extraction features.')
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader('Upload Medical Document')
            uploaded_file = st.file_uploader(
                'Choose a medical document',
                type=['pdf', 'docx', 'txt'],
                help='Upload medical reports, research papers, or clinical documents'
            )
            
            if uploaded_file:
                st.success(f'📄 {uploaded_file.name} uploaded successfully!')
                
                # Extract text based on file type
                if uploaded_file.type == 'application/pdf':
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    extracted_text = extract_text_from_docx(uploaded_file)
                elif uploaded_file.type == 'text/plain':
                    extracted_text = extract_text_from_txt(uploaded_file)
                else:
                    extracted_text = "Unsupported file format"
                
                st.session_state['extracted_text'] = extracted_text
                
                # Show text preview
                with st.expander("📋 View Extracted Text Preview"):
                    st.text_area("Extracted Text", extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text, height=200)
        
        with col2:
            st.subheader('Analysis Options')
            
            analysis_type = st.selectbox(
                'Analysis Type',
                ['Comprehensive Medical Extraction', 'Diagnosis Focus', 'Medication Review', 'Lab Results Analysis']
            )
            
            if st.button('🔍 Extract Medical Information', type='primary'):
                if st.session_state['extracted_text']:
                    with st.spinner('Analyzing document with RAG...'):
                        result = extract_medical_info_from_text(st.session_state['extracted_text'])
                    
                    st.subheader('📊 Extracted Medical Information')
                    st.markdown("---")
                    st.markdown(result)
                    
                    # Download option
                    st.download_button(
                        label='📥 Download Analysis',
                        data=result,
                        file_name='medical_analysis_report.md',
                        mime='text/markdown'
                    )
                else:
                    st.warning('Please upload a document first.')
        
        # Quick analysis templates
        st.subheader('🔄 Quick Analysis Templates')
        template_col1, template_col2, template_col3 = st.columns(3)
        
        with template_col1:
            if st.button('🧬 Extract Diagnoses'):
                if st.session_state['extracted_text']:
                    with st.spinner('Extracting diagnoses...'):
                        prompt = f"Extract all medical diagnoses from this text: {st.session_state['extracted_text'][:3000]}"
                        result = extract_medical_info_from_text(prompt)
                        st.markdown(result)
        
        with template_col2:
            if st.button('💊 Extract Medications'):
                if st.session_state['extracted_text']:
                    with st.spinner('Extracting medications...'):
                        prompt = f"Extract all medications and prescriptions from this text: {st.session_state['extracted_text'][:3000]}"
                        result = extract_medical_info_from_text(prompt)
                        st.markdown(result)
        
        with template_col3:
            if st.button('🩸 Extract Lab Results'):
                if st.session_state['extracted_text']:
                    with st.spinner('Extracting lab results...'):
                        prompt = f"Extract all laboratory results and values from this text: {st.session_state['extracted_text'][:3000]}"
                        result = extract_medical_info_from_text(prompt)
                        st.markdown(result)



elif menu == 'Notifications':
    st.header("📞 Emergency Notifications")

    col1, = st.columns(1)   # unpack single column

    with col1:
        if st.button("📞 Initiate Call"):
            success, msg = trigger_bland_call()
            if success:
                st.success(msg)
            else:
                st.error(msg)
