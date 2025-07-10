from flask import jsonify, json, abort
from google import genai

import fitz # PyMuPDF
import os


def get_file_path(folder, filename):
    """Retrieves file from data/uploads"""
    full_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", folder))

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
                word_data.append({
                    "text": text,
                    "bbox": [x0, y0, x1, y1]
                })
                all_words.append(text)


            result[f"page_{page_num + 1}"] = word_data
        
        result["all_words"] = all_words
        return result


    except FileNotFoundError:
        return jsonify({"error": f"{file_path} not found"}), 404
    

def llm_process(file_path):
    """
    Taking parsed pdf data and patient info, running in LLM, storing in a json:
        filename, patient id, doctor id, key details, personal takeaways, tasks
    Args:
        filename (string): Filename of pdf.

    Returns:
        JSON: filename, patient_id, doctor_id, key_details, personal_takeaways, tasks
    """

    patient_info = get_patient_info(file_path)
    patient_info_str = json.dumps(patient_info, indent=2)
    parsed_pdf = parse_pdf_contents(file_path)
    parsed_pdf_str = json.dumps(parsed_pdf, indent=2)


    prompt = f"""
    
    Instructions:
    1.
    You are medical report summarizer and related patient info, provide what a doctor would want to explain to a patient who doesn't understand difficult healthcare terminology. 
    Selected words and phrases should be specific to healthcare and involve complex terminology without including simple words. 
    This list should include EVERY word that could be possibly confusing for a patient to read. 
    Absolutely DO NOT include elementary words about history, symptoms, characterization, or patient identification. 
    Include every disease name, condition symptom, or anatomical location. 
    Absolutely DO NOT include source information. 
    Absolutely DO NOT provide details on hospital locations or terms. 
    Avoid choosing phrases over direct words when possible. 
    DO NOT incliude the words admissmion, history, or chief complaint. 
    
    Patient Info:
    {patient_info_str}

    Document Data:
    {parsed_pdf_str}

    Format of Response is in JSON with the following fields

    Key is quotes or a word directly from the document. 
    Value is your summarization

    """

    client = genai.Client(api_key="AIzaSyDAtOO9m0zixcFdtnAk6ZAJ1pP-Dz91J2A")

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )

    return 


