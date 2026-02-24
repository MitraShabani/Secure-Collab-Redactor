## SYSTEM DESIGN LAYER ##
from typing import List, Union
from regex_redactor import redact as regex_redact
from nlp_redactor import nlp_redact

TextInput = Union[str, List[str]]

def process_batch(orig_text):

    # orig_text can be string or list
    texts = orig_text if isinstance(orig_text, list) else [orig_text]

    results = []
    total_count = 0

    for i, text in enumerate(texts, start=1):
        if not isinstance(text, str):
            text = str(text)

        # Step 1: Regex redaction
        regex_text, regex_count = regex_redact(text)

        # Step 2: NLP redaction applied on top
        nlp_result = nlp_redact(regex_text)

        final_text = nlp_result["redacted_text"]
        nlp_count = nlp_result.get("count", 0)

        count = int(regex_count) + int(nlp_count)

        results.append({
            "id": i,
            "text": text,
            "redacted_text": final_text,
            "count": int(count)
        })

        total_count += count

    return results, total_count