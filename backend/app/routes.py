from flask import Blueprint, jsonify, request, Flask, send_from_directory, json
from flask import abort
from .helper import extract_words_with_coordinates
import os

app = Flask(__name__)
main = Blueprint("main", __name__)

UPLOADS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads"))
USERS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "users"))

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
    

@main.route('/api/get_file/<path:filename>')
def get_file(filename):
    """Retrieves file from data/uploads"""

    file_path = os.path.join(UPLOADS_FOLDER, filename)
    
    if not os.path.isfile(file_path):
        print("File not found:", file_path)
        abort(404)

    return send_from_directory(UPLOADS_FOLDER, filename)


@main.route('/api/get_patient_info/<path:filename>')
def get_patient_info(filename):
    """
    Retrieves patient info

    Args:
        filename (string): Filename of user.json.

    Returns:
        JSON: content of user.json's patient_info.
    """

    file_path = os.path.join(USERS_FOLDER, filename)

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return jsonify(data.get("patient_info", {}))
    except FileNotFoundError:
        return jsonify({"error": f"{filename} not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Malformed JSON file"}), 500



@main.route('/api/parse_pdf/<path:filename>')
def parse_pdf(filename):
    """
    Taking pdf and storing in a json: all words, per page a dictionary of text and coordinates

    Args:
        filename (string): Filename of pdf.

    Returns:
        JSON: content of pdf and coordinates for each word.
    """


    file_path = os.path.join(UPLOADS_FOLDER, filename)

    try:
        result = extract_words_with_coordinates(file_path)
        return(result)


    except FileNotFoundError:
        return jsonify({"error": f"{filename} not found"}), 404
    



app.register_blueprint(main)
