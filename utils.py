import os
import time
import shutil
import google.generativeai as genai
from pathlib import Path

def configure_genai(api_key):
    """Configures the Gemini API with the provided key."""
    if not api_key:
        return False, "API Key is missing."
    try:
        genai.configure(api_key=api_key)
        return True, "Success"
    except Exception as e:
        return False, str(e)

def get_ai_filename(file_path, model_name):
    """Uploads file to Gemini and asks for a descriptive filename."""
    try:
        model = genai.GenerativeModel(model_name)
        
        # Upload file
        sample_file = genai.upload_file(path=file_path, display_name="User Document")
        
        # Wait for processing
        while sample_file.state.name == "PROCESSING":
            time.sleep(1)
            sample_file = genai.get_file(sample_file.name)
            
        prompt = (
            "Analyze this document. Output ONLY a short, descriptive filename "
            "using snake_case (like: Data_Engineering_SQL_Basics). "
            "Do not include the file extension. Do not use spaces. "
            "If you cannot determine a name, return 'Unknown_Document'."
        )
        
        response = model.generate_content([sample_file, prompt])
        
        # Cleanup
        try:
            genai.delete_file(sample_file.name)
        except:
            pass
            
        return response.text.strip()
    except Exception as e:
        return None

def get_category(filename, model_name):
    """Asks Gemini to categorize the filename."""
    try:
        model = genai.GenerativeModel(model_name)
        prompt = (
            f"Categorize this file based on its name: '{filename}'. "
            "Return ONLY a single, short category name (e.g., 'SQL', 'Python', 'Finance', 'Personal'). "
            "Do not use special characters or spaces. "
            "If unclear, return 'Uncategorized'."
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "Uncategorized"

def clean_filename(text):
    """Sanitizes the filename."""
    if not text:
        return "Untitled"
    # Keep only safe chars
    safe_text = "".join([c if c.isalnum() or c in "-_" else "_" for c in text])
    # Remove duplicates
    while "__" in safe_text:
        safe_text = safe_text.replace("__", "_")
    return safe_text.strip("_")[:60]

def safe_rename(old_path, new_name_base):
    """Renames a file safely, handling duplicates."""
    folder = os.path.dirname(old_path)
    ext = os.path.splitext(old_path)[1]
    
    clean_name = clean_filename(new_name_base)
    new_filename = f"{clean_name}{ext}"
    new_path = os.path.join(folder, new_filename)
    
    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{clean_name}_{counter}{ext}"
        new_path = os.path.join(folder, new_filename)
        counter += 1
        
    try:
        os.rename(old_path, new_path)
        return True, new_filename
    except Exception as e:
        return False, str(e)

def safe_move(file_path, category):
    """Moves a file to a category folder safely."""
    folder = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
    # Sanitize category
    category = "".join([c for c in category if c.isalnum() or c in "_-"])
    if not category:
        category = "Uncategorized"
        
    dest_folder = os.path.join(folder, category)
    dest_path = os.path.join(dest_folder, filename)
    
    try:
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            
        shutil.move(file_path, dest_path)
        return True, f"{category}/{filename}"
    except Exception as e:
        return False, str(e)
