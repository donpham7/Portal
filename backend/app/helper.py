import fitz # PyMuPDF

def extract_words_with_coordinates(file_path):

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