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
# Helper Function for Background Image
# -----------------------------------
def get_base64_image(image_path):
    """Converts a local image file into a Base64 string for CSS injection."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# Fetch the background image string
bg_base64 = get_base64_image("background.jpg")

# -----------------------------------
# Premium Dark Glassmorphism Theme
# -----------------------------------
st.markdown(
    f"""
    <style>
    /* Full-screen background image setup */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Main App Header: Deep translucent bar with white text */
    h1 {{
        color: #FFFFFF !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        background: rgba(12, 28, 14, 0.85);
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Panel Section Headers forced to clean White */
    h2, h3, h4, h5, h6 {{
        color: #FFFFFF !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }}
    
    /* Dark Glassmorphism content layout panels (80% opacity dark green-black blend) */
    div[data-testid="column"] {{
        background-color: rgba(15, 32, 17, 0.82) !important;
        padding: 35px !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    
    /* Global Text Override inside panels to Pure White */
    div[data-testid="column"] p, 
    div[data-testid="column"] li, 
    div[data-testid="column"] span,
    div[data-testid="column"] label,
    div[data-testid="column"] small {{
        color: #FFFFFF !important;
        font-family: 'Segoe UI', system-ui, sans-serif !important;
        font-size: 1.05rem !important;
        line-height: 1.65 !important;
        font-weight: 500 !important;
    }}

    /* Add spacing to lists for readability */
    div[data-testid="column"] li {{
        margin-bottom: 12px !important;
    }}
    
    /* Clean text input boxes with dark backgrounds and white text */
    .stTextInput>div>div>input {{
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
        height: 45px;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: #A5D6A7 !important;
        box-shadow: 0 0 0 1px #A5D6A7 !important;
    }}
    
    /* Translucent White File Uploader Dialog Box */
    div[data-testid="stFileUploader"] {{
        background-color: rgba(255, 255, 255, 0.12) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }}
    
    /* Target internal elements of the file uploader to match white theme */
    div[data-testid="stFileUploader"] section button {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }}
    
    /* High-contrast target detection alert box */
    .stAlert {{
        background-color: rgba(27, 94, 32, 0.85) !important;
        border: 1px solid #4CAF50 !important;
        border-radius: 8px !important;
    }}
    .stAlert p {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}
    
    hr {{
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
        margin: 25px 0 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Main Dashboard Title
st.title("🌾 CropShield")

# Column Layout Configuration
col1, col2 = st.columns([1, 1.3])

# ===================================
# LEFT COLUMN: Inputs & Detection
# ===================================
with col1:
    st.subheader("🌱 Crop Protection Input")
    
    crop_name = st.text_input("What crop are you growing?", placeholder="e.g., Wheat, Cotton, Tomatoes")

    uploaded_file = st.file_uploader(
        "📸 Upload Pesticide/Chemical Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        if crop_name.strip() == "":
            st.warning("⚠️ Please enter a crop name before proceeding.")
        else:
            image = Image.open(uploaded_file)
            
            # --- FIX 1: Reduced Image Size ---
            st.image(image, caption="Uploaded Image", width=250)

            # Process prediction using temporary files
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            image.save(temp_file.name)

            pesticide_name = predict_TM.predict_TM(temp_file.name)
            pesticide_clean = pesticide_name[2:].strip()

            st.markdown("---")
            st.subheader("🧪 Detected Chemical:")
            st.success(f"{pesticide_clean}")
            
            # ===================================
            # RIGHT COLUMN: LLM Report Generation
            # ===================================
            with col2:
                st.subheader("📋 Agricultural Advisory Report")
                
                with st.spinner("Analyzing chemical safety and crop compatibility..."):
                    report = llm_app.llm_app(pesticide_clean, crop_name)
                    
                    # --- FIX 2: Black Translucent Box Around LLM Text ---
                    report_html = f"""
                    <div style="background-color: rgba(0, 0, 0, 0.65); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.15); box-shadow: 0 8px 32px 0 rgba(0,0,0,0.5);">
                    {report}
                    </div>
                    """
                    st.markdown(report_html, unsafe_allow_html=True)