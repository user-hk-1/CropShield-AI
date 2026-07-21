import streamlit as st
from PIL import Image
import tempfile
import base64
import os
import predict_TM
import llm_app

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="CropShield AI",
    page_icon="🌾",
    layout="wide"
)

# -----------------------------------
# Session State Initialization
# -----------------------------------
if "qa_answer" not in st.session_state:
    st.session_state.qa_answer = ""

# -----------------------------------
# Helper Function for Background Image
# -----------------------------------
def get_base64_image(image_path):
    """Converts a local image file into a Base64 string for CSS injection."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

bg_base64 = get_base64_image("background.jpg")

# -----------------------------------
# Premium Uniform Dark Glassmorphism Theme
# -----------------------------------
st.markdown(
    f"""
    <style>
    /* Full-screen background image */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Main Title Container */
    h1 {{
        color: #FFFFFF !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 800 !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        background: rgba(12, 28, 14, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }}

    /* Section Headers */
    h2, h3, h4, h5, h6 {{
        color: #E8F5E9 !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        text-shadow: 1px 2px 4px rgba(0, 0, 0, 0.6);
    }}
    
    /* Dark Glassmorphism Layout Panels */
    div[data-testid="column"] {{
        background: rgba(15, 32, 17, 0.75) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), inset 0px 1px 2px rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }}
    
    /* Global Text Inside Panels */
    div[data-testid="column"] p, 
    div[data-testid="column"] li, 
    div[data-testid="column"] span,
    div[data-testid="column"] label,
    div[data-testid="column"] small {{
        color: #F1F8E9 !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }}

    /* Text Input Boxes */
    .stTextInput>div>div>input {{
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
        height: 48px;
        box-shadow: inset 2px 4px 8px rgba(0,0,0,0.4) !important;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: #4CAF50 !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.4) !important;
    }}
    
    /* File Uploader Box */
    div[data-testid="stFileUploader"] {{
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 2px dashed rgba(255, 255, 255, 0.25) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }}
    
    /* Detection Success Alert Box */
    .stAlert {{
        background-color: rgba(27, 94, 32, 0.85) !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 10px !important;
    }}
    .stAlert p {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }}
    
    hr {{
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
        margin: 25px 0 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Dashboard Header Title
st.title("🌾 CropShield AI")

# Layout Configuration
col1, col2 = st.columns([1, 1.3])

# ===================================
# LEFT COLUMN: Inputs, Detection & Q&A
# ===================================
with col1:
    st.subheader("🌱 Crop Protection Input")
    
    crop_name = st.text_input("What crop are you growing?", placeholder="e.g., Wheat, Cotton, Tomatoes", key="crop_input")

    uploaded_file = st.file_uploader(
        "📸 Upload Pesticide/Chemical Image",
        type=["jpg", "jpeg", "png"],
        key="chemical_upload"
    )

    if uploaded_file is not None:
        if crop_name.strip() == "":
            st.warning("⚠️ Please enter a crop name before proceeding.")
        else:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Specimen", width=240)

            # Process prediction using temporary files
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            image.save(temp_file.name)

            pesticide_name = predict_TM.predict_TM(temp_file.name)
            pesticide_clean = pesticide_name[2:].strip()

            st.markdown("---")
            st.subheader("🧪 Detected Chemical:")
            st.success(f" {pesticide_clean}")
            
            # -----------------------------------------------------------------
            # INTEGRATED GROQ LLM Q&A MODULE
            # -----------------------------------------------------------------
            st.markdown("---")
            st.subheader("💬 Ask a Follow-up Question")
            
            user_question = st.text_input(
                "Ask specific questions about application, safety, or dosage:",
                placeholder="e.g., Can I mix this with liquid urea?",
                key="farmer_qa_input"
            )

            if user_question:
                with st.spinner("Consulting Groq LLM..."):
                    qa_response = llm_app.llm_qa(pesticide_clean, crop_name, user_question)
                    st.session_state.qa_answer = qa_response

            if st.session_state.qa_answer:
                qa_card_html = f"""
                <div style="background: rgba(0, 0, 0, 0.45); padding: 20px; border-radius: 12px; border-left: 4px solid #4CAF50; box-shadow: inset 0 2px 8px rgba(0,0,0,0.5); margin-top: 15px;">
                    <h4 style='color: #4CAF50; margin-top: 0; margin-bottom: 8px;'>🤖 AI Expert Answer:</h4>
                    <p style='color: #FFFFFF; line-height: 1.6; margin: 0;'>{st.session_state.qa_answer}</p>
                </div>
                """
                st.markdown(qa_card_html, unsafe_allow_html=True)

# ===================================
# RIGHT COLUMN: Groq Advisory Report
# ===================================
with col2:
    if uploaded_file is not None and crop_name.strip() != "":
        st.subheader("📋 Agricultural Advisory Report")
        
        with st.spinner("Analyzing chemical safety and crop compatibility..."):
            report = llm_app.llm_app(pesticide_clean, crop_name)
            
            report_html = f"""
            <div style="background: rgba(0, 0, 0, 0.5); padding: 25px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 8px 32px 0 rgba(0,0,0,0.5);">
            {report}
            </div>
            """
            st.markdown(report_html, unsafe_allow_html=True)