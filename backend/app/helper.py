from flask import jsonify, json, abort
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
    



