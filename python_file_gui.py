import os
import cv2
import csv
import numpy as np
import face_recognition
from datetime import datetime
from flask import Flask, request
from threading import Thread
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- Backend Logic (Flask) ---
app = Flask(__name__)

# Settings
KNOWN_FACES_DIR = "known_faces"
RECEIVED_DIR = "received_captures"
ATTENDANCE_FILE = "attendance.csv"

known_encodings = []
known_names = []

def load_faces():
    print("[SYSTEM] Loading faces...")
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    print(f"[SYSTEM] {len(known_names)} faces loaded.")

@app.route('/upload', methods=['POST'])
def upload():
    if not request.data: return "NO DATA", 400
    
    nparr = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None: return "INVALID", 400

    # Save capture
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(RECEIVED_DIR, f"cap_{timestamp}.jpg")
    cv2.imwrite(save_path, img)

    # Recognition
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(rgb_img)
    face_encs = face_recognition.face_encodings(rgb_img, face_locs)

    result_text = "FACE NOT MATCHED"
    status_color = "red"
    display_name = "ACCESS DENIED"

    if face_encs:
        matches = face_recognition.compare_faces(known_encodings, face_encs[0], tolerance=0.5)
        if True in matches:
            name = known_names[matches.index(True)]
            log_attendance(name)
            result_text = "FACE MATCHED"
            display_name = f"WELCOME {name.upper()}"
            status_color = "green"
    
    # Update GUI from background thread
    update_gui(save_path, result_text, display_name, status_color)
    
    return f"{display_name} ATTENDANCE MARKED" if "WELCOME" in display_name else "ACCESS DENIED", 200

def log_attendance(name):
    now = datetime.now()
    with open(ATTENDANCE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])

# --- Frontend Logic (Tkinter) ---
def update_gui(img_path, status, name, color):
    # Update Image
    img = Image.open(img_path)
    img = img.resize((300, 225), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    lbl_img.config(image=photo)
    lbl_img.image = photo
    
    # Update Status
    lbl_status.config(text=status, fg=color)
    lbl_name.config(text=name)
    
    # Update Log Table
    tree.insert("", 0, values=(datetime.now().strftime("%H:%M:%S"), name, status))

def start_server():
    app.run(host='0.0.0.0', port=5000, threaded=True)

# GUI Setup
root = tk.Tk()
root.title("ESP32-CAM Local Attendance System")
root.geometry("800x600")
root.configure(bg="#2c3e50")

# Header: College Branding
top_frame = tk.Frame(root, bg="#2c3e50", padx=20, pady=10)
top_frame.pack(side="top", fill="x")

logo_path = "college_logo.png"
logo_label = tk.Label(top_frame, bg="#2c3e50")
if os.path.exists(logo_path):
    try:
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label.config(image=logo_photo)
        logo_label.image = logo_photo
    except Exception:
        logo_label.config(text="LOGO", fg="white", font=("Arial", 10, "bold"))
else:
    logo_label.config(text="LOGO", fg="white", font=("Arial", 10, "bold"))
logo_label.pack(side="left", padx=(0, 15))

header_text_frame = tk.Frame(top_frame, bg="#2c3e50")
header_text_frame.pack(side="left", anchor="w")
tk.Label(header_text_frame,
         text="SAMRAT ASHOK TECHNOLOGICAL INSTITUTE",
         font=("Arial", 16, "bold"),
         bg="#2c3e50",
         fg="white").pack(anchor="w")
tk.Label(header_text_frame,
         text="DEPARTMENT OF INTERNET OF THINGS",
         font=("Arial", 12),
         bg="#2c3e50",
         fg="#ecf0f1").pack(anchor="w")

# Left Panel: Image & Status
left_frame = tk.Frame(root, bg="#2c3e50", padx=20, pady=20)
left_frame.pack(side="left", fill="both", expand=True)

lbl_img = tk.Label(left_frame, text="Waiting for Capture...", bg="#34495e", fg="white", width=40, height=15)
lbl_img.pack(pady=10)

lbl_status = tk.Label(left_frame, text="SYSTEM READY", font=("Arial", 18, "bold"), bg="#2c3e50", fg="#ecf0f1")
lbl_status.pack(pady=5)

lbl_name = tk.Label(left_frame, text="Scan to Begin", font=("Arial", 14), bg="#2c3e50", fg="#bdc3c7")
lbl_name.pack(pady=5)

# Right Panel: Log Table
right_frame = tk.Frame(root, bg="#ecf0f1", padx=10, pady=10)
right_frame.pack(side="right", fill="both", expand=True)

tk.Label(right_frame, text="Attendance Log", font=("Arial", 12, "bold"), bg="#ecf0f1").pack()

tree = ttk.Treeview(right_frame, columns=("Time", "User", "Result"), show="headings")
tree.heading("Time", text="Time")
tree.heading("User", text="User")
tree.heading("Result", text="Result")
tree.column("Time", width=80)
tree.column("User", width=150)
tree.pack(fill="both", expand=True)

# Start Backend
load_faces()
server_thread = Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

root.mainloop()
