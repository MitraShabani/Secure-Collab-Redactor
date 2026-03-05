### Secure-Collab-Redactor 🛡️

A Streamlit web application that implements a hybrid text-redaction system designed to detect and remove sensitive information from both well-structured and unstructured text, including uploaded log files. The system outputs a redacted report in structured JSON format.

The system combines:

- Rule-based pattern matching (regex engine)

- Named Entity Recognition (NER)

- Label-specific confidence thresholds

- Context-aware filtering

The objective is to balance precision (avoid over-redaction) and recall (avoid missing sensitive data).

### System Architecture

 #### Rule-Based Engine

Detects structured sensitive patterns:

+ Emails

+ Phone numbers

+ IPv4 addresses (with port / CIDR)

+ API keys & cloud access keys

+ JWT tokens

+ Credit card numbers

Includes light normalization:

+ (at) → @

+ (dot) → .

This layer provides high precision for well-structured data.

#### NER-Based Layer

Uses a pretrained Named Entity Recognition model
`dslim/bert-base-NER` via the
*Hugging Face Transformers* pipeline to detect contextual entities such as:

+ PER (Person)

+ LOC (Location)

+ ORG (Organization)

Enhancements implemented:

+ Label-specific thresholds are applied to reduce false positives:

  + PER → 0.70

  + LOC → 0.75

  + ORG → 0.85

+ Context-aware filtering:

  + Locations are redacted only if a person appears in the same text.This reduces unnecessary redactions when locations or organizations appear in general, non-identifiable contexts.

This design helps balance privacy protection and over-redaction, improving overall system precision.

### Evaluation

Testing was performed on a curated dataset of mixed inputs including:

+ Valid sensitive data

+ Obfuscated formats

+ Ambiguous named entities

+ Non-sensitive capitalized words

### Observations

+ Structured patterns achieved high precision.

+ Person detection is generally reliable using the pretrained NER model.

+ Context-aware filtering reduced unnecessary location redactions when no identifiable person is present.

+ Organization detection remains sensitive to contextual ambiguity.

The system demonstrates strong performance for well-structured data and reasonable trade-offs for unstructured entity detection.

### Failure Analysis
**Case 1 — Ambiguous Organizations**

Example:

> “Apple was delicious.”

Issue:

+ “Apple” detected as ORG with high confidence.

+ Semantic ambiguity cannot be resolved without deeper contextual reasoning.

Decision:
No hard-coded disambiguation added to avoid overfitting.

**Case 2 — Word-Based Phone Numbers**

Example:

> “five five five one two three four”

Issue:
+ Regex detects digit-based formats only.

Decision:
Full numeric word normalization considered out-of-scope for current system design.

### Limitations

+ No semantic disambiguation for ambiguous entities.

+ No multilingual support.

+ No normalization of fully written numeric expressions.

+ Dependent on pretrained NER confidence calibration.



 🚀 *Getting Started* :
1. Clone the repository
        ```
        git clone https://github.com/MitraShabani/Secure-Collab-Redactor.git
        cd Secure-Collab-Redactor
        ```
2. Install dependencies
        ```pip install -r requirements.txt```
3. Run the app
        ```streamlit run app.py```

The app will open in your browser at:

 http://localhost:8501.
