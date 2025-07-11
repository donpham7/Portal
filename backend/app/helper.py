from flask import jsonify, json, abort
from google import genai

import fitz  # PyMuPDF
import os


def get_file_path(folder, filename):
    """Retrieves file from data/uploads"""
    full_folder_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", folder)
    )

    file_path = os.path.join(full_folder_path, filename)

    if not os.path.isfile(file_path):
        print("File not found:", file_path)
        abort(404)

    return file_path


def get_patient_info(file_path):
    """
    Retrieves patient info

    Args:
        filename (string): Filename of user.json.

    Returns:
        JSON: content of user.json's patient_info.
    """

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return jsonify(data.get("patient_info", {}))
    except FileNotFoundError:
        return jsonify({"error": f"{file_path} not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Malformed JSON file"}), 500


def parse_pdf_contents(file_path):
    """
    Taking pdf and storing in a json: all words, per page a dictionary of text and coordinates

    Args:
        filename (string): Filename of pdf.

    Returns:
        JSON: content of pdf and coordinates for each word.
    """

    try:
        doc = fitz.open(file_path)
        result = {}
        all_words = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            words = page.get_text("words")

            word_data = []
            for w in words:
                x0, y0, x1, y1, text, *_ = w
                word_data.append({"text": text, "bbox": [x0, y0, x1, y1]})
                all_words.append(text)

            result[f"page_{page_num + 1}"] = word_data

        result["all_words"] = all_words
        return result

    except FileNotFoundError:
        return jsonify({"error": f"{file_path} not found"}), 404


def llm_process(pdf_file_path, patient_info_file_path):
    """
    Taking parsed pdf data and patient info, running in LLM, storing in a json:
        filename, patient id, doctor id, key details, personal takeaways, tasks
    Args:
        filename (string): Filename of pdf.

    Returns:
        JSON: filename, patient_id, doctor_id, key_details, personal_takeaways, tasks
    """

    parsed_pdf_contents = parse_pdf_contents(pdf_file_path)
    parsed_pdf_str = " ".join(parsed_pdf_contents["all_words"])

    patient_info = get_patient_info(patient_info_file_path)
    with open(patient_info_file_path, "r") as f:
        patient_info = json.load(f)["patient_info"]
    patient_info_str = json.dumps(patient_info, indent=2)

    prompt = f"""
    
    Instructions:
    You are going to read 2 prompts. You must respond in a list where Prompt 1's answer is index 0, and Prompt 2's answer is index 1 
    Like this, [Answer 1, Answer 2]
    Prompt 1.
    You are medical report summarizer and related patient info, provide what a doctor would want to explain to a patient who doesn't understand difficult healthcare terminology. 
    Find key details and select words and phrases that are specific to healthcare and involve complex terminology without including simple words. 
    Key details should be formated as a dictionary where the key is the extracted text from the document and the value is the more readable summary.
    This list should include EVERY word that could be possibly confusing for a patient to read. 
    Absolutely DO NOT include elementary words about history, symptoms, characterization, or patient identification. 
    ONLY put key details that normal people would not understand, challenging medical terms for key details. 
    Include every disease name, condition symptom, or anatomical location. 
    Absolutely DO NOT include source information. 
    Absolutely DO NOT provide details on hospital locations or terms. 
    Avoid choosing phrases over direct words when possible. 
    DO NOT incliude the words admissmion, history, or chief complaint. 

    
    Personal takeaways that summarize the report and relate to patient info
    
    Patient Info:
    {patient_info_str}

    Document Data:
    {parsed_pdf_str}

    Format of Response is in JSON with the following fields:
        filename,
        key_details,
        personal_takeaways

    Prompt 2.
    This is a health document. You are creating tasks for a patient to do by scanning the health document. 
    This should be specific actions for the patient, quantitative when possible. Do not summarize any patient specific data. 
    The tasks should be actions that the user needs to do; 
    Do not include tasks that medical professionals have performed on the user, these should only be future tasks that the user will need to complete themselves. 
    Each task needs to be checked off, so keep this in mind for wording. 
    Format the tasks by numbering each one with a short but descriptive header, and including the specific actions and purpose of the task below that. 
    Keep in mind low literacy level, but not at the cost of incorrect medical vocab (to prevent miscommunication). 
    Create 3-20 tasks, depending on what makes sense. 
    Each separate medication and or PT exercise, etc is a separate task. 
    This is a health document. 
    You are creating tasks for a patient to do by scanning the health document. 
    This should be specific actions for the patient, quantitative when possible.
    Do not summarize any patient specific data. 
    The tasks should be actions that the user needs to do; 
    Do not include tasks that medical professionals have performed on the user, these should only be future tasks that the user will need to complete themselves. 
    Each task needs to be checked off, so keep this in mind for wording. 
    Format the tasks by numbering each one with a short but descriptive header, and including the specific actions and purpose of the task below that. 
    The headers should ve quantified if applicable (e.g. take 2 mg Aspirin twice daily). 
    Keep in mind low literacy level, but not at the cost of incorrect medical vocab (to prevent miscommunication). 
    Create 3-20 tasks, depending on what makes sense. Each separate medication and or PT exercise, etc is a separate task. 
    Put this into json format. Use the header of each task as the key and do not number the tasks, and then any extra details as the value.

    Must be JSON format.

    Data to read:
        Patient Info:
        {patient_info_str}

        Document Data:
        {parsed_pdf_str}

    Response format criteria:
    [Answer 1 in valid JSON, Answer 2 in valid JSON]
    """

    client = genai.Client(api_key="AIzaSyDAtOO9m0zixcFdtnAk6ZAJ1pP-Dz91J2A")

    generated_content = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    result = json.loads(generated_content.text[8:-4])
    word_coordinates_dict = {}
    for key_detail in result[0]["key_details"].keys():
        first_bbox = None
        last_bbox = None
        list_key_detail = key_detail.split(" ")
        for page_key in parsed_pdf_contents.keys():
            if page_key[0:5] != "page_":
                break
            for doc_idx in range(len(parsed_pdf_contents[page_key])):
                if parsed_pdf_contents[page_key][doc_idx]["text"] == list_key_detail[0]:
                    if first_bbox == None:
                        first_bbox = parsed_pdf_contents[page_key][doc_idx]["bbox"]
                    match = True
                    for key_word_idx in range(len(list_key_detail)):

                        if (
                            parsed_pdf_contents[page_key][doc_idx + key_word_idx][
                                "text"
                            ]
                            != list_key_detail[key_word_idx]
                        ):
                            first_bbox = None
                            match = False
                            break
                    if match == True:
                        last_bbox = parsed_pdf_contents[page_key][
                            doc_idx + key_word_idx
                        ]["bbox"]
                        word_coordinates_dict[key_detail] = {
                            "page": page_key,
                            "bbox": [first_bbox, last_bbox],
                        }
    result.append(word_coordinates_dict)
    return result
