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
from .helper import get_file_path, get_patient_info, parse_pdf_contents, llm_process
import os
import fitz

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
REPORT_IMAGES_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "report_images")
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@main.route("/api/routes")
def list_routes():
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:30s} {methods:20s} {rule}")
        output.append(line)
    return "<br>".join(sorted(output))


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

        doc = fitz.open(filepath)

        # Iterate through pages
        out_folder = os.path.join(REPORT_IMAGES_FOLDER, "user_id" + userId)
        os.makedirs(out_folder, exist_ok=True)
        out_folder = os.path.join(out_folder, file.filename)
        os.makedirs(out_folder, exist_ok=True)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # 0-based indexing
            pix = page.get_pixmap(dpi=150)  # Increase DPI for better quality
            # Save image
            output_path = os.path.join(out_folder, f"page_{page_num + 1}.png")
            pix.save(output_path)
            print(f"Saved {output_path}")
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
    """Retrieves reports JSONs by user ID"""
    folder_path = REPORTS_FOLDER + "/" + "user_id" + str(user_id)

    json_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as f:
                json_list.append({"filename": filename[:-5], "data": json.load(f)})
    print("Got reports", (json_list))
    return jsonify(json_list), 200


@main.route("/api/get_report/<int:user_id>/<string:report_name>")
def get_report(user_id, report_name):
    print(user_id)
    print(report_name)
    """Retrieves reports JSONs by user ID"""
    file_path = (
        REPORTS_FOLDER + "/" + "user_id" + str(user_id) + "/" + report_name + ".json"
    )

    with open(file_path, "r") as f:
        report = json.load(f)
    print("Got report")
    return jsonify(report), 200


@main.route("/api/get_report_images/<int:user_id>/<string:report_name>")
def get_report_images(user_id, report_name):
    print(user_id)
    print(report_name)
    print("IMAGES")
    folder = os.path.join(REPORT_IMAGES_FOLDER, "user_id" + str(user_id), report_name)
    images = [
        f for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    return jsonify(images)


@main.route("/api/serve_image/<int:user_id>/<string:report_name>/<string:file_name>")
def serve_image(user_id, report_name, file_name):
    print("SERVING")
    folder = os.path.join(REPORT_IMAGES_FOLDER, "user_id" + str(user_id), report_name)
    print(folder, file_name)
    return send_from_directory(folder, file_name)


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
                tasks.extend(json.load(f)[1])
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
