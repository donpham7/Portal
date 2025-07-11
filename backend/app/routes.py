from flask import (
    Blueprint,
    jsonify,
    request,
    Flask,
    send_from_directory,
    send_file,
    json,
)
from flask import abort
from .helper import get_file_path, get_patient_info, parse_pdf_contents, llm_process, llm_process
import os

app = Flask(__name__)
main = Blueprint("main", __name__)

UPLOAD_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "uploads")
)
USERS_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "users")
)
REPORTS_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "reports")
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@main.route("/api/upload", methods=["POST"])
def upload():
    """
    Upload a pdf into uploads folder

    Args:

    Returns:
    """
    userId = str(request.form.get("user_id"))
    print(userId)
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No file part", 400
    if file:
        print(type(userId))
        os.makedirs(app.config["UPLOAD_FOLDER"] + "/user_id" + userId, exist_ok=True)
        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"], "user_id" + userId, file.filename
        )
        file.save(filepath)
        llm_result = llm(
            os.path.join(app.config["UPLOAD_FOLDER"], "user_id" + userId),
            file.filename,
            USERS_FOLDER,
            "user_id" + userId + ".json",
        )
        os.makedirs(os.path.join(REPORTS_FOLDER, "user_id" + userId), exist_ok=True)
        with open(
            os.path.join(REPORTS_FOLDER, "user_id" + userId, file.filename + ".json"),
            "w",
        ) as f:
            json.dump(llm_result, f, indent=4)
        return f"File uploaded successfully: {file.filename}"


@main.route("/api/file/<path:folder>/<path:filename>")
def file(folder, filename):
    """Retrieves file from data/uploads"""

    file_path = get_file_path(folder, filename)
    return send_file(file_path)


@main.route("/api/patient_info/<path:folder>/<path:filename>")
def patient_info(folder, filename):
    """Retrieves patient info"""

    file_path = get_file_path(folder, filename)
    return get_patient_info(file_path)


@main.route("/api/parse_pdf/<path:folder>/<path:filename>")
def parse_pdf(folder, filename):
    """Taking pdf and storing in a json: all words, per page a dictionary of text and coordinates"""

    file_path = get_file_path(folder, filename)
    return parse_pdf_contents(file_path)


@main.route("/api/get_reports/<int:user_id>")
def get_reports(user_id):
    print(user_id)
    """Retrieves reports JSONs by user ID"""
    folder_path = REPORTS_FOLDER + "/" + "user_id" + str(user_id)

    json_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                json_list.append(json.load(f))
    print("Got reports")
    return jsonify(json_list), 200


@main.route("/api/get_tasks/<int:user_id>")
def get_tasks(user_id):
    print(user_id)
    """Retrieves reports JSONs by user ID"""
    folder_path = REPORTS_FOLDER + "/" + "user_id" + str(user_id)

    tasks = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                tasks.extend(json.load(f)["tasks"])
    print("Got tasks")
    return jsonify(tasks), 200


@main.route("/api/get_patients/")
def get_patients():
    print()
    """Retrieves all patients"""
    folder_path = USERS_FOLDER

    patients = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                userData = json.load(f)
                if userData["role"] == "patient":
                    patients.append(userData)
    print("Got Patients")
    return jsonify(patients), 200


@main.route(
    "/api/llm/<path:pdf_folder>/<path:pdf_filename>/<path:patient_folder>/<path:patient_filename>"
)
def llm(pdf_folder, pdf_filename, patient_folder, patient_filename):
    """Taking parsed pdf data and patient info, running in LLM, storing in a json:
    filename, patient id, doctor id, key details, personal takeaways, tasks
    http://localhost:5000/api/llm/uploads/UMNwriteup.pdf/users/pamela.json
    """

    pdf_file_path = get_file_path(pdf_folder, pdf_filename)
    patient_info_file_path = get_file_path(patient_folder, patient_filename)
    result = llm_process(pdf_file_path, patient_info_file_path)
    return result


app.register_blueprint(main)
