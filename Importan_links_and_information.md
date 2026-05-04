
## 🚀 Installation & Usage

1.  **Hardware Setup:** Wire the components according to the [Schematic Diagram].
2.  **Firmware:** Upload the ESP32-CAM and ESP8266 code. **Note:** Update the IP address in the ESP32-CAM code to match your laptop's local IP.
3.  **Authorized Faces:** Add photos of authorized users to the `known_faces/` folder.
4.  **Run Server:** Execute the Python script:
    ```bash
    python python_file_gui.py
    ```
5.  **Scan:** Press the hardware push button. The system will capture the face, verify the identity, and log the results.

---

## 📊 Results & Performance
*   **Success Status:** GUI displays "WELCOME [NAME]" and the Green LED activates.
*   **Denied Status:** GUI flags "ACCESS DENIED" and the Red LED/Buzzer activates.
*   **Logs:** All data is recorded in `attendance.csv` including Name, Date, and Time.

---

## 🎓 Acknowledgments
Developed at the **Samrat Ashok Technological Institute (SATI), Vidisha**, within the **Department of Internet of Things**This is an impressive IoT project! Based on the briefing and technical details provided, here is a professional, well-structured README template you can use for your GitHub repository.

---

# AI-Powered Face Recognition Attendance & Security System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/Platform-ESP32--CAM%20%7C%20ESP8266-green.svg)
![Language](https://img.shields.io/badge/Language-Python%20%7C%20C%2B%2B-yellow.svg)

A robust, contactless, and wireless IoT solution designed to automate identity verification and security logging using Computer Vision and Deep Learning.

## 📌 Overview
Traditional biometric systems are prone to wear and tear and pose hygiene risks in a post-pandemic world[cite: 1]. This project introduces a **Zero-Touch** facial recognition system that utilizes an **ESP32-CAM** to capture data and a **Python Flask backend** to process identification in real-time[cite: 1].

### Key Features
*   **Contactless & Hygienic:** Eliminates physical contact for safer identity verification[cite: 1].
*   **Wireless Flexibility:** Operates over a local Wi-Fi network, allowing for easy mounting and installation[cite: 1].
*   **Real-time Processing:** Uses `dlib` deep learning models for high-speed facial analysis and matching[cite: 1].
*   **Automated Logging:** Saves attendance logs with precise timestamps in a tamper-proof CSV format[cite: 1].
*   **Visual Feedback:** Features a Tkinter-based GUI on the server and an I2C/Serial LCD on the hardware for user status[cite: 1].

---

## 🏗️ System Architecture
The system functions through a synchronized three-phase process:
1.  **Capture & Upload:** The ESP32-CAM captures a high-resolution image and sends it via HTTP POST to the Flask server[cite: 1].
2.  **Facial Analysis:** The backend extracts landmarks and compares them against a database of "Known Faces"[cite: 1].
3.  **Action & Feedback:** If matched, the system logs the entry and sends a signal back to the hardware to trigger indicators (Green LED/Buzzer)[cite: 1].



---

## 🛠️ Hardware Requirements
*   **ESP32-CAM:** Main camera module for image capture[cite: 1].
*   **ESP8266 (NodeMCU):** Used to expand I/O for the LCD display and security peripherals[cite: 1].
*   **16x2 LCD Display (WINSTAR-STN):** For real-time status messages (e.g., "Ready to Scan", "Face Matched")[cite: 1].
*   **Peripherals:** 5V Regulator (7805), 3.7V Li-ion batteries, Buzzer, and Status LEDs (Red/Green)[cite: 1].

---

## 💻 Software Setup

### Prerequisites
*   Python 3.12+
*   Arduino IDE (for ESP32/ESP8266 firmware)

>
> 
YOUTUBE EXPLAINATION VIDEO WITH DEMOSTRATION - https://youtu.be/ezGEntegwR8?feature=shared

SCHEMETIC DIAGRAM - https://u.easyeda.com/join?type=project\&key=9cd9b9547d57c8c4d0d3f8d251307d29\&inviter=daca3f5d21f74c309367984f05076846

### Python Libraries
Install the required dependencies:
```bash
pip install opencv-python face_recognition flask numpy pillow







