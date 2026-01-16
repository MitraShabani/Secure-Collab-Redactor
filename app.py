import streamlit as st
from privacy_utils import redact
from storage import saveReport

st.set_page_config(page_title="Privacy-Safe-Collab", page_icon="🛡️", layout="wide")
st.title("🛡️ Privacy-Aware Collaboration")
st.caption("Text reports with automatic redaction.")

tabs = st.tabs(["✍️ New Report"])

with tabs[0]:
    st.subheader("Submit a bug/content report")

    # text inputs
    title = st.text_input("Title", placeholder="Give your content a title...", key="title_input")
    orig_text = st.text_area("Content", height=220, placeholder="Paste logs/steps here...", key="text_input")

    # optional file upload
    st.write("Optional: upload your file")
    uploadedFile = st.file_uploader(
        "Upload your log here",
        type=['txt', 'json', 'csv']
        )
    if uploadedFile:
        file_name = uploadedFile.name.lower()
        try:
            if file_name.endswith(".txt"):
                textFile = uploadedFile.read().decode("utf-8", errors="replace")

            elif file_name.endswith(".json"):
                import json
                jsonFile = json.load(uploadedFile)
                textFile = [item["text"] for item in jsonFile]

            # If the user already typed something
            if isinstance(textFile, list):
                # JSON batch mode: keepong orig_text as list of string
                orig_text = ([orig_text] if orig_text else []) + textFile
            else:
                # txt/csv mode: keep orig_text as string
                orig_text = (orig_text + "\n\n" + textFile) if orig_text else textFile

            st.success(f"File {uploadedFile.name} uploaded.\n\nThe description content will be added to the file.")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    # Button
    if st.button("🔍 Redaction"):

        # orig_text can be string or list
        texts = orig_text if isinstance(orig_text, list) else [orig_text]

        results = []
        total_count = 0

        for i, text in enumerate(texts, start=1):

            if not isinstance(text, str):
                text = str(text)

            redacted_text, predicted_sensitive = redact(text)
            redacted_text, count = redact(text)
            total_count += int(count)

            results.append({
                "id": i,
                "text": text,
                "redacted_text": redacted_text,
                "count": int(count)
            })
            # redacted_text, predicted_sensitive = redact(text)
            # st.write("DEBUG type:", type(predicted_sensitive), "value:", predicted_sensitive)


        st.json(results)

        st.session_state["preview"] = {
            "title": title,
            "original": orig_text,
            "results": results,
            "count": total_count
        }


    def save_and_clear():
        pv = st.session_state.get("preview")
        if not pv:
            return
        # save
        saveReport({
            "title": pv["title"],
            "redacted_text": pv["results"],
            "found_count": pv["count"],
        })
        st.success("Saved.")

        # clear session state safely
        st.session_state.pop("preview", None)
        st.session_state["text_input"] = ""
        st.session_state["title_input"] = ""


    # Streamlit reruns the script on every click, so:
    previewText = st.session_state.get("preview")
    if previewText:

        st.write("---")
        st.metric("Potential sensitive items found", previewText["count"])

        col1, col2 = st.columns(2)
        with col1:
            st.write("**Original**")
            st.code(previewText["original"], language="text")
        with col2:
            st.write("**Redacted (to be saved)**")
            st.code(previewText["results"], language="text")

        st.info("Click **Save Report**. Otherwise, edit and preview again.")

        st.button("Save Report", on_click=save_and_clear)




