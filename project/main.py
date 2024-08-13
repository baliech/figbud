import streamlit as st
from kudra_cloud_client import KudraCloudClient
import os
import requests
import google.generativeai as genai
from streamlit_lottie import st_lottie



genai.configure(api_key="AIzaSyCGEbJVxzvysT8Q-XJTecx46j9lV1IKSxU")
model = genai.GenerativeModel(model_name="gemini-pro")







# nlps = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Initialize KudraCloudClient with your authentication token
kudraCloud = KudraCloudClient(token="1b412d10-0fea-4d99-bfb3-f7e5df249875")

# Define the project run ID here
PROJECT_RUN_ID = "David/Invoice%20Extraction-17228469437846134/1b412d10-0fea-4d99-bfb3-f7e5df249875/MTI5MA=="

def load_lottieurl(url:str):
    r= requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_ai = load_lottieurl("https://lottie.host/54225138-3908-4294-a70b-1b5c9cbb9f7e/mYvbWoiYHD.json")
lottie_ais = load_lottieurl("https://lottie.host/44d9b3f5-6e06-4790-b891-5e9bde7e5a24/7x1fjA2NWz.json")

def process_uploaded_files(uploaded_file):
    temp_dir = 'temp_uploaded_files'
    os.makedirs(temp_dir, exist_ok=True)
    
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    result = kudraCloud.analyze_documents(files_dir=temp_dir, project_run_id=PROJECT_RUN_ID)
    
    os.remove(file_path)
    os.rmdir(temp_dir)
    
    return result

# Streamlit app interface
st.set_page_config('claims validator', '🌐')
st_lottie(lottie_ai,width=200,height=200)

st.title("Automated Claims Verification🚀")
st.markdown("""
<style>
[data-testid="stSidebarContent"] {
    background-color:F0F2F6;
    color:#0c005a;
   box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
}
[data-testid="stMarkdownContainer"]{
            color:#0c005a;}
          h1{
            color:#6643b5;
            }
            [id="c525ad7c"]{color:#6643b5;
            }
            [class="st-emotion-cache-1aehpvj e1bju1570"]{
            color:#0c005a;}
            [class="main st-emotion-cache-bm2z3a ea3mdgi8"]{
            background-color:#dbd8e3;}
            [data-testid="stHeader"]{
            background-color:#dbd8e3;}
[class="st-emotion-cache-uhkwx6 ea3mdgi6"]{
            background-color:grey;}
</style>
    """, unsafe_allow_html=True)

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
    )

    if st.button("Submit", key='submit_button'):
        with st.chat_message("user"):
            st.markdown(st.session_state.selected_question)

        # Spinner while waiting for the response
        with st.spinner('Generating response...'):
            response = model.generate_content(st.session_state.selected_question + " " + st.session_state.texts)

            with st.chat_message("assistant"):
                st.markdown(response.text)

            # Store messages in session state
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": st.session_state.selected_question
                }
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response.text
                }
            )

# Display the extracted text below the predefined questions
if st.session_state.texts:
    st.header("Extracted Text")
    st.write(st.session_state.texts)

# Display chat messages from session state in an orderly fashion
if st.session_state.messages:
    st.header("Query History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
