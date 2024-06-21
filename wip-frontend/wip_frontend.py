import streamlit as st
from google.cloud import storage
from google.api_core.exceptions import NotFound


def check_gcs(bucket):
    client = storage.Client()
    try:
        client.get_bucket(bucket)  # Check if bucket exists
        return True
    except NotFound:
        return False


def upload_files(bucket, files):
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    upload_messages = []
    for file in files:
        blob = bucket.blob(file.name)
        blob.upload_from_file(file)
        upload_messages.append(f"File {file.name} uploaded to {bucket.name}.")
    return upload_messages


st.title("Upload portal 💜")
st.subheader("Example frontend to showcase wip upload/extraction solution!")

if "bucket_exists" not in st.session_state:
    st.session_state.bucket_exists = False
if "bucket_status_message" not in st.session_state:
    st.session_state.bucket_status_message = ""
if "upload_status" not in st.session_state:
    st.session_state.upload_status = []


bucket = st.text_input(
    label="Enter GCS bucket to upload file to",
    key="01_text_input",
    placeholder="Please enter existing GCS bucket...",
)

if st.button("Check GCS bucket", key="01_button"):
    if bucket:
        st.session_state.bucket_exists = check_gcs(bucket)
        if st.session_state.bucket_exists:
            st.session_state.bucket_status_message = "GCS bucket exists"
        else:
            st.session_state.bucket_status_message = "GCS bucket does not exist"
    else:
        st.error("Text input field is empty")

if st.session_state.bucket_status_message:
    if st.session_state.bucket_exists:
        st.success(st.session_state.bucket_status_message)
    else:
        st.error(st.session_state.bucket_status_message)

if st.session_state.bucket_exists:
    uploaded_files = st.file_uploader(
        "Upload files to GCS bucket to be processed for data extraction.",
        accept_multiple_files=True,
        type=["pdf"],
        key="01_file_uploader",
    )
    if uploaded_files:
        if st.button("Upload Files"):
            upload_status_messages = upload_files(bucket, uploaded_files)
            st.session_state.upload_status = upload_status_messages
            for message in st.session_state.upload_status:
                st.success(message)
else:
    st.warning("Please enter an existing GCS bucket to unlock the upload portal")
