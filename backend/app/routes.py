from flask import Blueprint, jsonify, request, Flask, send_from_directory, json
from flask import abort
import os


app = Flask(__name__)
main = Blueprint("main", __name__)

UPLOAD_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads")
)
USERS_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "users")
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@main.route("/api/upload", methods=["POST"])
def upload():
    """Uploads file into data/uploads"""

    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No file part", 400
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return f"File uploaded successfully: {file.filename}"


@main.route("/api/get_file/<path:filename>")
def get_file(filename):
    """Retrieves file from data/uploads"""

    full_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.isfile(full_path):
        print("File not found:", full_path)
        abort(404)

    return send_from_directory(UPLOAD_FOLDER, filename)


@main.route("/api/get_patient_info/<path:filename>")
def get_patient_info(filename):
    """Retrieves patient_info from data/users"""

    full_path = os.path.join(USERS_FOLDER, filename)

    try:
        with open(full_path, "r") as f:
            data = json.load(f)
            return jsonify(data.get("patient_info", {}))
    except FileNotFoundError:
        return jsonify({"error": f"{filename} not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Malformed JSON file"}), 500


app.register_blueprint(main)
