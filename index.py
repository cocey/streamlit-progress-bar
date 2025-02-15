import os
import requests
import streamlit as st
import uuid
import mimetypes

downloadDir = "downloads"
os.makedirs(downloadDir, exist_ok=True)


def getMb(size):
    return "{:10.2f}".format(size / (1024 * 1024))


col1, col2 = st.columns([5, 1])

urlInput = col1.text_input(label="url")

col2.write(" ")
col2.write(" ")

btnDownload = col2.button(":material/start:", use_container_width=True)
if btnDownload and urlInput:

    progressBar = st.progress(0, text="Operation in progress. Please wait.")

    url = str(urlInput)
    # TODO: validate url

    response = requests.get(url, stream=True, allow_redirects=True)

    total = int(response.headers.get("content-length", 0))
    limit = 110000000

    if total > limit:
        st.warning(f"file is too big, maximum allowed size is : {getMb(limit)} MB")
    else:
        contentType = response.headers.get("content-type", "application/x-binary")

        ext = mimetypes.guess_extension(contentType, strict=True)
        fileName = str(uuid.uuid4()) + ext
        filePath = os.path.join(downloadDir, fileName)

        blockSize = 1024
        downloaded = 0

        with open(filePath, "wb") as file:
            for data in response.iter_content(blockSize):
                downloaded += len(data)
                file.write(data)

                percentComplete = min(100, int(100 * downloaded / total))
                progressBar.progress(
                    percentComplete,
                    text=f"loading: {getMb(downloaded)} MB / {getMb(total)} MB",
                )

        os.remove(filePath)
