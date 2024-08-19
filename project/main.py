import streamlit as st
from kudra_cloud_client import KudraCloudClient
import os
import google.generativeai as genai
<<<<<<< HEAD
from streamlit_option_menu import option_menu
import re
import tempfile
from googletrans import Translator
# Initialize API and KudraCloudClient
=======
from streamlit_lottie import st_lottie



>>>>>>> 2a7361e02a38c85d92e81b0dc1b00a1d0259b99f
genai.configure(api_key="AIzaSyAKPCsEM28_jJKaiNGNKWGLSD7_pYkC_hs")
model = genai.GenerativeModel(model_name="gemini-pro")
kudraCloud = KudraCloudClient(token="1b412d10-0fea-4d99-bfb3-f7e5df249875")

# Define the project run ID here
PROJECT_RUN_ID = "David/Invoice%20Extraction-17228469437846134/1b412d10-0fea-4d99-bfb3-f7e5df249875/MTI5MA=="

<<<<<<< HEAD
import os
import tempfile
=======
def load_lottieurl(url:str):
    r= requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_ai = load_lottieurl("https://lottie.host/54225138-3908-4294-a70b-1b5c9cbb9f7e/mYvbWoiYHD.json")
lottie_ais = load_lottieurl("https://lottie.host/44d9b3f5-6e06-4790-b891-5e9bde7e5a24/7x1fjA2NWz.json")
>>>>>>> 2a7361e02a38c85d92e81b0dc1b00a1d0259b99f

def process_uploaded_files(uploaded_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            st.write(f"Attempting to save file to: {file_path}")  # Debug info
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            st.write(f"File saved successfully. File exists: {os.path.exists(file_path)}")  # Debug info
            
            result = kudraCloud.analyze_documents(files_dir=temp_dir, project_run_id=PROJECT_RUN_ID)
            
            st.write("Document analysis completed")  # Debug info
            
            return result
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None
def generate_response_and_status(question, text):
    validation_question = f"Based on the following text, answer the question: '{question}'. If the information is not found, clearly state 'Information not found'.\n\nText: {text}\n\nQuestion: {question}"
    response = model.generate_content(validation_question)
    answer = response.text.strip()
    
    # Initialize translator
    translator = Translator()

    # Check if the answer indicates the information is not found
    if any(phrase in answer.lower() for phrase in ["information not found", "does not mention", "is not mentioned", "no information"]):
        return answer, "Not Found", None

    # Check for specific patterns based on the question type
    if "name" in question.lower():
        if re.search(r'[\u4e00-\u9fff]+', answer):  # Check for Chinese characters
            translated = translator.translate(answer, src='zh-cn', dest='en')
            return f"{answer} (English: {translated.text})", "Found", None
        elif re.search(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b', answer):
            return answer, "Found", None
    elif any(keyword in question.lower() for keyword in ["invoice number", "receipt num", "reference number"]):
        # Updated regex pattern for invoice/reference numbers
        if re.search(r'\b(?:INV-?)?[A-Z0-9-]+\b|\b\d+\b', answer, re.IGNORECASE):
            return answer, "Found", None
    elif "date" in question.lower():
        if re.search(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', answer):
            return answer, "Found", None
    elif "total" in question.lower():
        if re.search(r'\$?\d+(\.\d{2})?', answer):
            return answer, "Found", None
    elif "traditional chinese medicine" in question.lower() or "tcm" in question.lower():
        if any(word in answer.lower() for word in ["yes", "mentioned", "traditional chinese medicine", "tcm"]):
            return answer, "Found", "Benefit Category: Traditional Medicine"
        else:
            return answer, "Not Found", "Benefit Category: Not Traditional Medicine"

    # If no specific pattern is found but the answer seems substantial
    if len(answer.split()) > 1 and answer.lower() not in ["no", "none", "not applicable"]:
        return answer, "Found", None
    
    return answer, "Not Found", None


def confirmation_logic(answer, question):
    answer_lower = answer.lower()
    question_lower = question.lower()
    
    if "not mentioned" in answer_lower or "no information" in answer_lower:
        return False
    
    if "name" in question_lower:
        return any(word.istitle() for word in answer.split()) and "doctor" not in answer_lower
    
    if "invoice number" in question_lower or "receipt num" in question_lower:
        return bool(re.search(r'\d+', answer))
    
    if "date" in question_lower:
        return bool(re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', answer))
    
    if "total" in question_lower:
        return bool(re.search(r'\$?\d+(\.\d{2})?', answer))
    
    if "traditional chinese medicine" in question_lower or "tcm" in question_lower:
        return "traditional chinese medicine" in answer_lower or "tcm" in answer_lower
    
    return len(answer) > 5  # If the answer is more than 5 words, consider it found

# Streamlit app interface
st.set_page_config('claims validator', '🌐')

<<<<<<< HEAD
# Sidebar for file upload and page navigation
with st.sidebar:
    st.sidebar.title('Upload Document☁️')
    selected = option_menu(
        menu_title="Menu",
        options=["Upload File", "Set Keywords"],
        icons=["folder-plus", "pencil-square"],
        menu_icon="menu-down",
        default_index=0
=======

st.title("Automated Claims Verification🚀")

# Sidebar for file upload
st.sidebar.title('Upload Document☁️')
uploaded_file = st.sidebar.file_uploader("Choose a file to upload", accept_multiple_files=False)

# Reset state when a new file is uploaded
if uploaded_file and (not st.session_state.get("uploaded_file") or st.session_state.uploaded_file.name != uploaded_file.name):
    st.session_state.texts = ""
    st.session_state.selected_question = ""
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Please extract the text from your uploaded document, then select a question to get a response."
        }
    ]
    st.session_state.uploaded_file = uploaded_file

# Display uploaded file details in the sidebar
if uploaded_file:
    st.sidebar.write(f"**File name:** {uploaded_file.name}")
    if uploaded_file.type.startswith('image'):
        st.sidebar.image(uploaded_file, use_column_width=True)

# Initialize session state for messages, texts, and selected question
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Please extract the text from your uploaded document, then select a question to get a response."
        }
    ]

if "texts" not in st.session_state:
    st.session_state.texts = ""

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

# Text extraction logic
if st.button('Extract text🏥', key='extract_button'):
    if uploaded_file:
        with st.spinner('Analyzing document. This may take a few minutes...'):
            results = process_uploaded_files(uploaded_file)
            st.session_state.texts = results[0]["text"] if results else ""

# Display predefined questions above the extracted text
if st.session_state.texts:
    st.header("Select a Question to query extracted text")
    st.session_state.selected_question = st.selectbox(
        "Select a question:", 
        options=[
            "Find name in the provided text, The name shouldn't be the name of a doctor",
            "What is the invoice number?",
            "What is the invoice date?",
            "What is the date ?",
            "What is the invoice reference number?note that reference number is not the same as invoice number",
            "What is Co Reg No?",
            "What is GST Reg No?",
            "What is the total?",
            "From the text provided, can you find traditional Chinese medicine or TCM?"
        ],
        key="question_select"
>>>>>>> 2a7361e02a38c85d92e81b0dc1b00a1d0259b99f
    )

# Keyword dictionary to store mapping of keywords to questions
keyword_to_question = {
    "person name": "What is the person name on the document not the name of the doctor?",
    "Total": "What is the total amount?",
    "Invoice Number": "What is the invoice number or receipt Num?",
    "Date": "What is the invoice date?",
    "Reference Number": "What is the reference number?",
    "TCM": "Is traditional Chinese medicine or TCM mentioned?"
}

if "keywords" not in st.session_state:
    st.session_state.keywords = []

if selected == "Set Keywords":
    st.title("Set Keywords🔑")
    st.subheader("select or unselect keywords")
    st.info("document will be queried based on keyword selected")

    selected_keywords = st.multiselect(
        "Select Keywords",
        options=list(keyword_to_question.keys()),
        default=st.session_state.keywords
    )
    st.session_state.keywords = selected_keywords

if selected == "Upload File":
    st.title("Automated Claims Verification🚀")
    uploaded_file = st.sidebar.file_uploader("Choose a file to upload", accept_multiple_files=False)

<<<<<<< HEAD
    # Reset state when a new file is uploaded
    if uploaded_file and (not st.session_state.get("uploaded_file") or st.session_state.uploaded_file.name != uploaded_file.name):
        st.session_state.texts = ""
        st.session_state.responses = []
        st.session_state.uploaded_file = uploaded_file

    # Display uploaded file details in the sidebar
    if uploaded_file:
        st.sidebar.write(f"**File name:** {uploaded_file.name}")
        if uploaded_file.type.startswith('image'):
            st.sidebar.image(uploaded_file, use_column_width=True)

    # Initialize session state for texts and responses
    if "texts" not in st.session_state:
        st.session_state.texts = ""

    if "responses" not in st.session_state:
        st.session_state.responses = []

    # Determine questions based on selected keywords or use predefined ones
    if st.session_state.keywords:
        questions = [keyword_to_question[keyword] for keyword in st.session_state.keywords]
    else:
        st.info("Please set keywords in the 'Set Keywords' section else document will be queried based on default rules")
        questions = list(keyword_to_question.values())

    # Text extraction and automatic question answering
    if st.button('Extract text and Generate Responses🏥', key='extract_button'):
        if uploaded_file:
            with st.spinner('Analyzing document and generating responses...'):
                results = process_uploaded_files(uploaded_file)
                st.session_state.texts = results[0]["text"] if results else ""

                # Iterate through questions and get responses
                st.session_state.responses = []
                for question in questions:
                    answer, status, category = generate_response_and_status(question, st.session_state.texts)

                    st.session_state.responses.append({
                        "question": question,
                        "answer": answer,
                        "status": status
                    })

                # Display verification result
                found_count = sum(1 for response in st.session_state.responses if response["status"] == "Found")
                total_count = len(st.session_state.responses)
                
                if found_count == total_count:
                    st.success("Document fully verified")
                elif found_count > total_count // 2:
                    st.warning(f"Document partially verified ({found_count}/{total_count} fields found)")
                else:
                    st.error(f"Document verification failed ({found_count}/{total_count} fields found)")

                if any("traditional Chinese medicine" in response["answer"].lower() or "TCM" in response["answer"].lower() for response in st.session_state.responses):
                    st.info("Category Benefit: Traditional Medicine")
                if category is not None:
                    benefit_category = category
                    st.info(benefit_category)
    # Display the responses in a table format
    if st.session_state.responses:
        st.header("Responses Table")
        st.table(st.session_state.responses)
         
        
        

    # Display the extracted text below the responses
    if st.session_state.texts:
        st.header("Extracted Text")
        st.write(st.session_state.texts)
=======
# Display chat messages from session state in an orderly fashion
if st.session_state.messages:
    st.header("Query History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
>>>>>>> 2a7361e02a38c85d92e81b0dc1b00a1d0259b99f
