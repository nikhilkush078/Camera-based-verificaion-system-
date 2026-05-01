from flask import Flask, request
import face_recognition
import os
import cv2
import numpy as np
from datetime import datetime
import csv

app = Flask(__name__)

# Folder Configuration
KNOWN_FACES_DIR = "known_faces"
RECEIVED_DIR = "received_captures"
ATTENDANCE_FILE = "attendance.csv"

for folder in [KNOWN_FACES_DIR, RECEIVED_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

known_encodings = []
known_names = []

def load_faces():
    print("\n[SYSTEM] Initializing Database...")
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                name = os.path.splitext(filename)[0]
                known_names.append(name)
                print(f" > Encoded: {name}")
    print(f"[SYSTEM] {len(known_names)} faces loaded and ready.\n")

def log_attendance(name):
    now = datetime.now()
    file_exists = os.path.isfile(ATTENDANCE_FILE)
    with open(ATTENDANCE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(ATTENDANCE_FILE).st_size == 0:
            writer.writerow(["Name", "Date", "Time"])
        writer.writerow([name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])

@app.route('/upload', methods=['POST'])
def upload():
    if not request.data:
        return "NO DATA", 400

    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return "INVALID IMAGE", 400

    # Recognition Process
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(rgb_img)
    face_encs = face_recognition.face_encodings(rgb_img, face_locs)

    print("\n" + "="*40)
    print(f" SCAN ATTEMPT: {datetime.now().strftime('%H:%M:%S')}")
    print("-"*40)

    if not face_encs:
        print(" STATUS: FACE NOT MATCHED")
        print(" REASON: No face detected in frame.")
        print(" ACTION: ACCESS DENIED")
        print("="*40)
        return "FACE NOT MATCHED ACCESS DENIED", 200

    matches = face_recognition.compare_faces(known_encodings, face_encs[0], tolerance=0.5)
    
    if True in matches:
        name = known_names[matches.index(True)]
        log_attendance(name)
        print(f" STATUS: FACE MATCHED")
        print(f" USER  : {name.upper()}")
        print(f" ACTION: ATTENDANCE MARKED")
        print("="*40)
        return f"WELCOME {name.upper()} ATTENDANCE MARKED", 200
    
    print(" STATUS: FACE NOT MATCHED")
    print(" REASON: Unauthorized user.")
    print(" ACTION: ACCESS DENIED")
    print("="*40)
    return "FACE NOT MATCHED ACCESS DENIED", 200

if __name__ == '__main__':
    load_faces()
    app.run(host='0.0.0.0', port=5000)