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
    st.write("Optional: upload a .txt log file")
    uploadedFile = st.file_uploader("Upload your log here", type=['txt'])
    if uploadedFile:
        try:
            uploadedText = uploadedFile.read().decode("utf-8", errors="replace")
            # If the user already typed something
            orig_text = (orig_text + "\n\n" + uploadedText) if orig_text else uploadedText

            st.success(f"File {uploadedFile.name} uploaded.\n\nThe description content will be added to the file.")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    # Button
    if st.button("🔍 Redaction"):
        redacted, count = redact(orig_text)

        st.session_state["preview"] = {
            "title": title,
            "original": orig_text,
            "redacted": redacted,
            "count": count
        }


    def save_and_clear():
        pv = st.session_state.get("preview")
        if not pv:
            return
        # save
        saveReport({
            "title": pv["title"],
            "redacted_text": pv["redacted"],
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
            st.code(previewText["redacted"], language="text")

        st.info("Click **Save Report**. Otherwise, edit and preview again.")

        st.button("Save Report", on_click=save_and_clear)




