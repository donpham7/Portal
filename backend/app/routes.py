from flask import Blueprint, jsonify, request, Flask, send_from_directory, send_file,  json
from flask import abort
from .helper import get_file_path, get_patient_info, parse_pdf_contents
import os

app = Flask(__name__)
main = Blueprint("main", __name__)

UPLOADS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads"))
# USERS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "users"))

app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
os.makedirs(UPLOADS_FOLDER, exist_ok=True)


@main.route("/api/upload", methods=["POST"])
def upload():
    """
    Upload a pdf into uploads folder

    Args:

    Returns:
    """

    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No file part", 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"File uploaded successfully: {file.filename}"
    

@main.route('/api/file/<path:folder>/<path:filename>')
def file(folder, filename):
    """Retrieves file from data/uploads"""

    file_path = get_file_path(folder, filename)
    return send_file(file_path)



@main.route('/api/patient_info/<path:folder>/<path:filename>')
def patient_info(folder, filename):
    """Retrieves patient info"""

    file_path = get_file_path(folder, filename)
    return get_patient_info(file_path)




@main.route('/api/parse_pdf/<path:folder>/<path:filename>')
def parse_pdf(folder, filename):
    """Taking pdf and storing in a json: all words, per page a dictionary of text and coordinates"""

    file_path = get_file_path(folder, filename)
    return parse_pdf_contents(file_path)

    



app.register_blueprint(main)
