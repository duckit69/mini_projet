
import cv2 
import numpy as np
import os
from scipy.spatial.distance import cosine
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QImage, QFontDatabase,QPainter
from PyQt5.QtCore import Qt, QTimer
from deepface import DeepFace
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model



#DETECT ALIGN AND CROP FACES TO 112X112 RGB uint8############################################################
def detect_align( image_path: str,
    detector_backend: str = "mtcnn",
    align: bool = True,
    enforce_detection: bool = True,
):
    
    try:
        faces = DeepFace.extract_faces(
            img_path=image_path,
            detector_backend=detector_backend,
            align=align,
            enforce_detection=enforce_detection,
        )

        if not faces:
            return None

        face = faces[0]["face"]  # RGB float image [0,1]
        face = (face * 255).astype("uint8")
        face = cv2.resize(face, (112, 112), interpolation=cv2.INTER_LINEAR)

        return face

    except Exception as e:
        print(f"*****------[ERROR] {detector_backend}: {e}")
        return None
#################################################################################################################
#converts opencv image array to QPixmap
def cv_to_qt(rgb):
    h, w, ch = rgb.shape
    bytes_per_line = ch * w
    qt_img = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qt_img)

#draw bounding boxes 
def draw_bounding_boxes(img, faces):
    if img is None:
        return None

    img_disp = img.copy()

    if faces:
        area = faces[0]["facial_area"]
        x, y, w, h = area["x"], area["y"], area["w"], area["h"]
        cv2.rectangle(img_disp, (x, y), (x+w, y+h), (0, 255, 0), 1)

    return img_disp

#get bbox size and position
def get_face_bbox(img, faces):
    if img is None or not faces:
        return None

    area = faces[0]["facial_area"]
    x, y, w, h = area["x"], area["y"], area["w"], area["h"]

    return x, y, w, h


####################################
###################################


def NEWanimate_display_all(img_path, label):

    img_cam = cv2.imread(img_path)

    faces_cam = DeepFace.extract_faces(
        img_path=img_path,
        detector_backend="mtcnn",
        align=True,
        enforce_detection=False,
    )
    face = faces_cam[0]
    face = face["face"]
    face = (face * 255).astype("uint8")
    face = cv2.resize(face, (112, 112), interpolation=cv2.INTER_LINEAR)

    if not faces_cam:
        return

    x, y, w, h = get_face_bbox(img_cam, faces_cam)

    # Convert BGR → RGB
    rgb = cv2.cvtColor(img_cam, cv2.COLOR_BGR2RGB)
    h_img, w_img, ch = rgb.shape

    qt_img = QImage(rgb.data, w_img, h_img, ch * w_img, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qt_img)

    # Scale while keeping aspect ratio
    scaled_pixmap = pixmap.scaled(
        label.size(),
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation
    )

    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter)

    # After 0.8 seconds overlay aligned face
    def show_aligned():

        aligned_img = face
        if aligned_img is None:
            return

        # Get displayed pixmap size
        disp_pix = label.pixmap()
        disp_w = disp_pix.width()
        disp_h = disp_pix.height()

        # Compute top-left offset (because of centering)
        offset_x = (label.width() - disp_w) // 2
        offset_y = (label.height() - disp_h) // 2

        # Compute scale factor
        scale = min(disp_w / w_img, disp_h / h_img)

        new_x = int(x * scale) + offset_x
        new_y = int(y * scale) + offset_y
        new_w = int(w * scale)
        new_h = int(h * scale)

        overlay_label = QLabel(label)
        overlay_label.setPixmap(cv_to_qt(aligned_img))
        overlay_label.setScaledContents(True)
        overlay_label.setGeometry(new_x, new_y, new_w, new_h)
        overlay_label.setStyleSheet("border: 0.5px solid lime;")
        overlay_label.show()
        label.setPixmap(QPixmap())
        
        

    QTimer.singleShot(800, show_aligned)


#####################################
####################################
###################################
#####################################
####################################
###################################
#####################################

# Verify face all-in-one recognition using insightface models 
def verify_face(face_cam_img: str, face_card_img: str):
    # 0.Disable GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1" 
    app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(128,128))  # use det_size=(640,640) if card image has half body (shoulders showing)

    img_cam = cv2.imread(face_cam_img)
    img_card = cv2.imread(face_card_img)

    faces_cam = app.get(img_cam)
    faces_card = app.get(img_card)
   
    
    emb1 = faces_cam[0].normed_embedding  # 512-D vector
    emb2 = faces_card[0].normed_embedding
 
    score = 1 - cosine(emb1, emb2)
    sharpness = 15
    threshold = 0.32
    confidence = 100 * (1 / (1 + np.exp(-sharpness * (score - threshold))))
    match = confidence >= 50
    #match = score >= 0.50
    print(f"[Cosine_Sim]: {score}")
    return confidence, match





# ------------------------------ VERIFICATION WINDOW -------------
class VerifyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face verification window")
        self.setFixedSize(1280, 720)
        
        self.layout = QVBoxLayout()

        self.setStyleSheet("""
        QPushButton{
                        font-weight: bold;
                        font-size:16px; 
                        color:teal;
                        
                       }
""")
        # ROW
        self.row1 = QHBoxLayout()

        self.face_cam_label = QLabel("FACE CAM")
        self.face_card_label = QLabel("FACE CARD")
        self.face_cam_label.setAlignment(Qt.AlignCenter)
        self.face_cam_label.setFixedSize(520, 380)
        self.face_card_label.setAlignment(Qt.AlignCenter)
        self.face_card_label.setFixedSize(520, 380)
        self.row1.addWidget(self.face_cam_label)
        self.row1.addWidget(self.face_card_label)

         # customize pics borders:
        self.face_cam_label.setStyleSheet("""
        QLabel {
            border: 2px solid #00C853;
            border-radius: 12px;
            background-color: #1e1e1e;
        }
        """)

        self.face_card_label.setStyleSheet("""
        QLabel {
           
            border: 2px solid #00C853;
            border-radius: 12px;
            background-color: #1e1e1e;
        }
        """)


        #display card image
        self.card_img_path = "output.jpg"
        self.display_image(self.card_img_path, self.face_card_label)

        self.layout.addLayout(self.row1)
        #live cam
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(30)
        #result label
        self.resultLabel = QLabel("-- RESULT --")
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setMaximumHeight(300)
        self.resultLabel.setWordWrap(True)
        self.layout.addWidget(self.resultLabel)
        
        self.resultLabel.setStyleSheet("""
        QLabel {
            color: black;
            font-weight: bold;
            font-size: 24px;
        }
        """)
        #get cam button
        self.get_cam_btn = QPushButton("Get Face")
        self.get_cam_btn.clicked.connect(self.get_face_cam)
       
        self.layout.addWidget(self.get_cam_btn)

        #verify button
        self.verify_btn = QPushButton("Verify")
        self.verify_btn.clicked.connect(self.verify)
      
        self.layout.addWidget(self.verify_btn)
        #restart button
        self.restart_btn = QPushButton("Restart")
        self.restart_btn.clicked.connect(self.restart)
   
        self.layout.addWidget(self.restart_btn)
        #store image paths
        self.cam_img_path = None
        

      
        self.setLayout(self.layout)

    def restart(self):
        self.resultLabel.setText("-- Result --")
        self.resultLabel.setStyleSheet("color: black; font-weight: bold; font-size: 24px;")
        self.display_image(self.card_img_path, self.face_card_label)
        # overlay label clearing
         # Clear the overlay labels
        for cam_overlay_label in self.face_cam_label.findChildren(QLabel):
            cam_overlay_label.deleteLater()
        for card_overlay_label in self.face_card_label.findChildren(QLabel):
            card_overlay_label.deleteLater() 
        #live cam
        self.cap = cv2.VideoCapture(0)
        self.current_frame = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_preview)
        self.timer.start(30)
    
    def get_face_cam(self):
        if self.current_frame is None:
            return
        self.cam_img_path = "camera_original.jpg"
        cv2.imwrite(self.cam_img_path, self.current_frame)
        if self.cam_img_path:
            self.timer.stop()
            self.cap.release()
            self.display_image(self.cam_img_path, self.face_cam_label)
            NEWanimate_display_all(self.cam_img_path, self.face_cam_label)
            NEWanimate_display_all(self.card_img_path, self.face_card_label)
            
 
    def verify(self):
        if self.cam_img_path:
          
            try:            
                confidence, match = verify_face(self.cam_img_path, self.card_img_path)
            except Exception as e:
                self.resultLabel.setText(f"No face detected in camera")
                print(f"[Error]: {e}")
                return
            print(f"------------------ \n [Confidence]:  {confidence} \n [MATCH]:  {match} \n ---------------------")
            self.resultLabel.setText(f"Match: {match} \n {confidence:.2f} % ")
            if match:
                self.resultLabel.setStyleSheet("color: teal; font-weight: bold; font-size: 24px;")
            else:
                self.resultLabel.setStyleSheet("color: red; font-weight: bold; font-size: 24px;")

            
    def update_preview(self):
        # 1.Get live preview (camera)
        ret, frame = self.cap.read()
        if not ret:
            return
        self.current_frame = frame
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h,w,ch = rgb.shape
        img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.face_cam_label.setPixmap(QPixmap.fromImage(img).scaled(
            self.face_cam_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    def display_image(self, image_path, label):
        image = QImage(image_path)
        pixmap = QPixmap(image)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerifyApp()
    window.show()
    sys.exit(app.exec_())
