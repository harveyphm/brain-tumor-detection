import os
import cv2
import numpy as np
import streamlit as st
from io import BytesIO


from models.cnn.utils import load_model
from opencv import findTumorContour

CASCADE_PATH = os.path.join('models', 'haar', 'cascade.xml')
CNN_PATH = os.path.join('models', 'cnn', 'base.pt')
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

class TumorDetectorGUI():

    def __init__(self):

        # Face dection algorithm from cv2
        self.cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.cnn = load_model(CNN_PATH)
        self.seg = findTumorContour

    @staticmethod
    def _convert_image(img):
        # encode
        _, buffer = cv2.imencode(".jpg", img)
        io_buf = BytesIO(buffer)
        byte_im = io_buf.getvalue()
        return byte_im
    
    def _detect_tumors_image(self,col1, col2, path = None ):
            
        if self.img_file_buffer is not None:
            bytes_data = self.img_file_buffer.getvalue()
            self.img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        else:
            self.img = cv2.imread(path)

        # Convert img to gray scale and detect faces
        gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Detect tumor with HAAR cascade 
        boxes = self.cascade.detectMultiScale(gray_img, 1.1, 4)
        draw_img = self.img.copy()
        if len(boxes) == 0:
            #Detect tumor with CNN
            boxes = self.cnn(gray_img)
            if len(boxes) > 0:
                cnts_list = []
                for box in boxes:
                    x, y, w, h = boxes[0]
                    x = x - w/2
                    y = y - h/2
                    h_img, w_img = self.img.shape[:2]
                    x = int(x*w_img)
                    y = int(y*h_img)
                    w = int(w*w_img)
                    h = int(h*h_img)
                    mask = np.zeros((h_img, w_img), dtype=np.uint8)
                    mask[y:y+h, x:x+w] = 255
                    masked_img = cv2.bitwise_and(self.img, self.img, mask=mask)
                    seg_boxes, cnts, final = self.seg(masked_img)
                    cnts_list.append(cnts)
                #Create a image with draw contours
                for c in cnts_list:
                    draw_img = cv2.drawContours(draw_img, c, -1, (0, 255, 0), 2)
        else: 
            cnts_list = []
            for box in boxes:
                x, y, w, h = box
                mask = np.zeros(gray_img.shape, dtype=np.uint8)
                mask[y:y+h, x:x+w] = 255
                masked_img = cv2.bitwise_and(self.img, self.img, mask=mask)
                seg_boxes, cnts, final = self.seg(masked_img)
                cnts_list.append(cnts)
            #Create a image with draw contours
            for c in cnts_list:
                draw_img = cv2.drawContours(draw_img, c, -1, (0, 255, 0), 2)            
                        
        
        col1.write("Original Image :camera:")
        col1.image(self.img)
        col2.write("Segmented Image :wrench:")
        col2.image(draw_img)
        st.sidebar.markdown("\n")
        st.sidebar.download_button("Download fixed image", self._convert_image(draw_img), "fixed.png", "image/png")


    def window(self):
        
        st.set_page_config(page_title="Group 8 - Brain Tumor Detecor", page_icon=":brain:")
        

        with st.container():
            
            # st.title('Digital Image Processing - Group 8')
            # st.title('Brain Tumor Detecor')
            st.markdown("<h1 style='text-align: center; color: white;'>Digital Image Processing - Group 8</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: white;'>Brain Tumor Detecor </h2>", unsafe_allow_html=True)

        with st.container():
            col1, col2 = st.columns(2)

            # Webcam display
            self.img_file_buffer = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

            if self.img_file_buffer is not None:
                if self.img_file_buffer.size > MAX_FILE_SIZE:
                    st.error("The uploaded file is too large. Please upload an image smaller than 5MB.")
                else:
                    self._detect_tumors_image(col1, col2)
            else:
                self._detect_tumors_image(col1, col2, path = "./demo/demo.jpg")