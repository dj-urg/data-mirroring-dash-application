# src/components/utils/security_utils.py

import logging
import os
import tempfile
from werkzeug.utils import secure_filename

# Define allowed file extensions for security
ALLOWED_EXTENSIONS = {'json'}

# Define maximum file size (20 MB)
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB in bytes

def allowed_file(filename):
    """
    Check if the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(contents, filename):
    """
    Validate the uploaded file for size and type.
    """
    if len(contents) > MAX_FILE_SIZE:
        raise ValueError("File is too large")

    if not allowed_file(filename):
        raise ValueError("File type not allowed")

def save_temp_file(contents, filename):
    """
    Save the uploaded file to a temporary location securely.
    """
    validate_file(contents, filename)
    secure_name = secure_filename(filename)
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, secure_name)
    
    with open(temp_file_path, 'wb') as f:
        f.write(contents)
    
    logging.info(f"File saved temporarily at {temp_file_path}")
    
    return temp_file_path

def cleanup_temp_file(file_path):
    """
    Delete the temporary file after processing.
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Temporary file {file_path} deleted.")
