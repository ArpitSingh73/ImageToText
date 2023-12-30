import streamlit as st
import pytesseract as tess
from pytesseract import Output
import cv2
import tempfile
import os

var = st.sidebar.radio("Navigation", ["Home", "About"])

if var == "Home":
    st.title("Image To Text")
    st.text("")
    st.header("Upload an image...", divider="rainbow")

    file = st.file_uploader("Upload an image...", label_visibility="collapsed")
    if file:
        try:
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, file.name)
            with open(path, "wb") as f:
                f.write(file.getvalue())

            st.image(file, file.name)
            # st.write(file.name)
            # st.write(file)
            # st.write(file.type)
            myconfig = r"--psm 11 --oem 3"

            img = cv2.imread(path)
            height, width, _ = img.shape
            data = tess.image_to_data(
                img, config=myconfig, output_type=Output.DICT, lang="eng+fra"
            )

            ls = []
            amount_boxes = len(data["text"])
            for i in range(amount_boxes):
                if float(data["conf"][i]) > 70:
                    if not ls.__contains__(data["text"]):
                        ls.append(data["text"])
                    (x, y, width, height) = (
                        data["left"][i],
                        data["top"][i],
                        data["width"][i],
                        data["height"][i],
                    )
                    img = cv2.rectangle(
                        img, (x, y), (x + width, y + height), (0, 255, 0), 2
                    )
                    img = cv2.putText(
                        img,
                        data["text"][i],
                        (x, y + height + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

            # st.header(" ")
            st.text("")
            st.header("Image after recognotion :", divider="rainbow")
            st.image(img, file.name)
            st.header("Recognized characters are : ", divider="rainbow")
            # container = st.container(border=True)
            st.write(" ".join(data["text"]))

        except:
            st.warning("Select proper file..", icon="⚠️")

elif var == "About":
    st.subheader(
        "Hi there, the theme of this project is Optical Character Recognitioin(OCR). Optical character recognition or optical character reader (OCR) is the electronic or mechanical conversion of images of typed, handwritten or printed text into machine-encoded text, whether from a scanned document, a photo of a document, or a scene photo.I have used `Pytesseract` and `Open-Cv` libraries for this project. Pytesseract is a Python wrapper for Google’s Tesseract-OCR Project, which can recognize and read text embedded in images of various formats . It supports image processing, language detection, box estimation, data extraction also. OpenCV is an open-source computer vision and machine learning software library by which we(computers) can understand the images and videos how they are stored and how we can manipulate and retrieve data from them. Computer Vision is the base or mostly used for Artificial Intelligence                    "
    )
    st.text("")
    st.subheader(" Thank You.")
