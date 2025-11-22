import streamlit as st
import os
from utils import configure_genai, get_ai_filename, safe_rename, get_category, safe_move

# Page Config
st.set_page_config(
    page_title="FileFlow - Intelligent Organizer",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    h1, h2, h3 {
        color: #F8FAFC;
        font-weight: 700;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
    }
    
    .stTextInput > div > div > input {
        background-color: #1E293B;
        color: #F8FAFC;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > div {
        background-color: #1E293B;
        color: #F8FAFC;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Card-like styling for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1E293B;
        border-radius: 8px 8px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94A3B8;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #334155;
        color: #F8FAFC;
        font-weight: 600;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Main Content Header
col1, col2 = st.columns([1, 5])
with col1:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.write("📂")

with col2:
    st.title("FileFlow")
    st.markdown("### Intelligent File Organization")

st.markdown("Transform your chaotic folders into a structured library using AI power.")

# Configuration Section (Moved from Sidebar)
with st.expander("⚙️ Configuration", expanded=True):
    col_a, col_b = st.columns(2)
    with col_a:
        api_key = st.text_input("Gemini API Key", type="password", help="Get your key from Google AI Studio")
    with col_b:
        model_name = st.text_input("Gemini Model Name", placeholder="e.g. gemini-2.5-flash", help="Enter the specific Gemini model version you want to use")
    
    target_folder = st.text_input("Target Folder", placeholder=r"e.g. C:\Users\Name\Documents\Unsorted", help="Copy and paste the full path of the folder you want to organize.")
    
    if api_key and model_name:
        success, msg = configure_genai(api_key)
        if success:
            st.success("✅ Connected to Gemini")
        else:
            st.error(f"❌ API Error: {msg}")
    else:
        st.info("ℹ️ Enter API Key and Model Name to start")

# Tabs
tab1, tab2 = st.tabs(["✨ Smart Rename", "📂 Smart Organize"])

with tab1:
    st.header("Smart Rename")
    st.markdown("Automatically rename files based on their content.")
    
    if st.button("Start Renaming", type="primary", disabled=not (api_key and model_name)):
        if not target_folder or not os.path.exists(target_folder):
            st.error("Please enter a valid Target Folder path!")
        else:
            # Filter out hidden files
            files = [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]
            target_files = [f for f in files if not f.startswith('.')]
            
            if not target_files:
                st.info("No files found to rename.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, filename in enumerate(target_files):
                    file_path = os.path.join(target_folder, filename)
                    status_text.markdown(f"**Processing {i+1}/{len(target_files)}:** `{filename}`...")
                    
                    new_name_base = get_ai_filename(file_path, model_name=model_name)
                    
                    if new_name_base and new_name_base != "Unknown_Document":
                        success, new_filename = safe_rename(file_path, new_name_base)
                        if success:
                            st.toast(f"Renamed: {filename} -> {new_filename}", icon="✅")
                        else:
                            st.error(f"Failed to rename {filename}: {new_filename}")
                    else:
                        st.warning(f"Could not generate name for {filename}")
                    
                    progress_bar.progress((i + 1) / len(target_files))
                
                status_text.text("Renaming Complete!")
                st.balloons()

with tab2:
    st.header("Smart Organize")
    st.markdown("Categorize and move files into folders.")
    
    if st.button("Start Organizing", type="primary", disabled=not (api_key and model_name)):
        if not target_folder or not os.path.exists(target_folder):
            st.error("Please enter a valid Target Folder path!")
        else:
            files = [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]
            target_files = [f for f in files if not f.startswith('.')]
            
            if not target_files:
                st.info("No files found to organize.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, filename in enumerate(target_files):
                    file_path = os.path.join(target_folder, filename)
                    status_text.markdown(f"**Categorizing {i+1}/{len(target_files)}:** `{filename}`...")
                    
                    category = get_category(filename, model_name=model_name)
                    success, dest = safe_move(file_path, category)
                    
                    if success:
                        st.toast(f"Moved: {filename} -> {dest}", icon="📂")
                    else:
                        st.error(f"Failed to move {filename}: {dest}")
                        
                    progress_bar.progress((i + 1) / len(target_files))
                
                status_text.text("Organization Complete!")
                st.balloons()
