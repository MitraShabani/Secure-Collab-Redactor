## ML LAYER ##
from transformers import pipeline
from typing import Dict, Any

# use internal Lazy-loading to prevent loading model each time.
# NER (Named Entity Recognition)
_NER = None

def get_ner():
    global _NER
    if _NER is None:

        # for 'transformers' : what task, which model, what format for output
        _NER = pipeline(
            "token-classification",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple"  # it is used to group the entities
            )

    return _NER

def detect_and_redact(text: str, min_score: float = 0.70) -> Dict[str, Any]:

    ner = get_ner()
    spans = []
    persons_present = False

    LABEL_THRESHOLDS = {
        "PER": 0.70,
        "LOC": 0.75,
        "ORG": 0.85
    }

    for entity in ner(text):

        label = entity["entity_group"]
        threshold = LABEL_THRESHOLDS.get(label, min_score) # If this label exists in the dictionary, use its value. Otherwise, use min_score

        if entity["score"] >= threshold:  # only accept this detection if the model is confident enough.
            spans.append({
                "start": entity["start"],
                "end": entity["end"],
                "label": entity['entity_group'],
                "score": float(entity["score"]),
                "source": "NER"
            })
        if label == "PER":
            persons_present = True

    # In-place filtering: remove LOC and ORG spans if no person
    if not persons_present:
        spans[:] = [s for s in spans if s["label"] != "LOC" and s["label"] != "ORG"]

    return spans

def nlp_redact(text: str, min_score: float = 0.70) -> Dict[str, Any]:

    spans = detect_and_redact(text, min_score)
    redacted = list(text)

    for span in spans:
        for i in range(span["start"], span["end"]):
            redacted[i] = "*"

    redacted_text = "".join(redacted)

    return {
        "redacted_text": redacted_text,
        "count": len(spans)
    }

