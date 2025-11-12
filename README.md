# **Face Recognition Bus Pass Validation System**

A real-time AI-based system that validates bus passes using **facial recognition** instead of manual checking.
Built using **Flask**, **OpenCV (LBPH)**, **HTML5/JS webcam**, and **SQLite**.

---

## 🚀 **Overview**

Traditional bus pass checking is slow, manual, and prone to fraud. This project automates validation by capturing the passenger’s face and comparing it against a trained database of registered users.

The system:

* Captures **20 face samples** during registration
* Auto-trains the face recognition model (LBPH)
* Prevents **duplicate registrations** (name + face)
* Validates users in real time using webcam input
* Blocks unregistered passengers from using bus passes

---

## 🎯 **Features**

### 🔹 **1. Web-Based Face Registration**

* Captures 20 images through the browser webcam
* Detects face using Haarcascade
* Saves samples as training data
* Automatically retrains the LBPH model
* Checks for:

  * Duplicate name
  * Duplicate face

### 🔹 **2. Real-Time Validation**

Two modes:

* **Browser Validation** (Render-friendly)
* **OpenCV Validation Window** (local real-time detection)

Shows:

* ✅ Valid Pass (recognized user)
* ❌ Invalid User (fraud or unregistered)

### 🔹 **3. Fraud Prevention**

* Detects and blocks attempts to register the same person with a different name
* Ensures every passenger is unique in the system

### 🔹 **4. Clean UI**

Modern UI using HTML, CSS, and JS webcam API.
Buttons: Register, Validate, Back to Home.

### 🔹 **5. Render Deployment Support**

Works perfectly online using browser camera capture.

---

## 🛠️ **Tech Stack**

| Component  | Technology                           |
| ---------- | ------------------------------------ |
| Backend    | Flask                                |
| Frontend   | HTML5, CSS, JavaScript               |
| ML         | OpenCV, LBPH Face Recognizer         |
| Database   | SQLite                               |
| Deployment | Render (uses opencv-python-headless) |

---

## 📦 **Project Structure**

```
face_buspass_project/
│── app.py
│── requirements.txt
│── Procfile
│── haarcascade_frontalface_default.xml
│── buspass.db
│── faces/
│── templates/
│   ├── index.html
│   ├── register.html
│   ├── validate.html
│── static/
```

---

## 🖼️ **How It Works**

### **1. Registration**

✔ User enters their name
✔ System captures 20 images from webcam
✔ Face crops are stored in `/faces`
✔ LBPH model retrains automatically
✔ Duplicate faces/names get blocked

### **2. Validation**

✔ Webcam image sent to server
✔ LBPH predicts user ID + confidence
✔ If confidence < threshold → Valid Pass
✔ Else → Unregistered Passenger

---

## 🚀 **Run Locally**

### **1. Clone Repo**

```bash
git clone https://github.com/YOUR_USERNAME/face-buspass.git
cd face-buspass
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Run App**

```bash
python app.py
```

### **4. Open in Browser**

```
http://127.0.0.1:5000/
```

---

## 🌐 **Deploy on Render**

### **Use these files:**

* `requirements.txt`
* `Procfile`
* No OpenCV GUI (`cv2.imshow`) in deployed version
* Use only browser-based webcam routes

### Start command:

```
gunicorn app:app
```

---

## 🔒 **Duplicate Detection Logic**

* Duplicate **name** → blocked
* Duplicate **face** (LBPH confidence < threshold) → blocked
  Prevents fraud and ensures every passenger is unique.

---

## 📸 **Sample Enrollment Flow**

```
User enters name → System captures 20 images → Model retrains → Registration complete
```

## 🎥 **Sample Validation Flow**

```
User looks into camera → Face detected → LBPH predicts → Pass Approved / Denied
```

## 👨‍💻 **Author**

**Koushik Srirambhatla**
Flask Developer | Machine Learning | Computer Vision
GitHub: [Click](https://github.com/Koushik-Srirambhatla)
LinkedIn: [Click](https://linkedin.com/in/koushiksrirambhatla)

---

## ⭐ **Support**

If you like this project, leave a **star** ⭐ on the repo!
It motivates me to build more AI-based systems.

---
