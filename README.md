# 🤖 Accident Damage Detection and Repair Cost Estimation

[Accident Damage Detection and Repair Cost Estimation](https://github.com/user-attachments/assets/5b6b8a1d-cb9c-4b57-87a5-dc80ceeb955e)

An AI-powered **Vehicle Damage Detection System** designed to detect and estimate repair costs for damaged car parts based on uploaded images. The system uses **YOLOv8** for object detection and a web-based interface built with **Flask** for seamless user interaction. This project helps automate the process of assessing vehicle damage, making it efficient for insurance companies and repair centers to evaluate repair costs quickly.

---

## Table of Contents

- 🚗 [Project Overview](#project-overview)
- ⚙️ [Features](#features)
- 🛠️ [Technologies Used](#technologies-used)
- 📝 [Setup and Installation](#setup-and-installation)
- 💻 [Usage](#usage)
- 🤖 [Model Information](#model-information)
- 🚀 [Future Improvements](#future-improvements)
---

## 🚗 Project Overview

The **Vehicle Damage Detection System** is designed to help users upload car images and detect damaged parts, including:
- **Bonnet**
- **Bumper**
- **Dickey**
- **Door**
- **Fender**
- **Light**
- **Windshield**

The detected parts are highlighted in the image, and the system estimates repair costs based on the detected damage.

### Key Objectives:
1. **Damage Detection**: Accurately detect damaged car parts using object detection models.
2. **Cost Estimation**: Estimate repair costs for the damaged parts detected in the vehicle image.
3. **Database Integration**: Store user details, car information, spare parts, and repair costs in a MySQL database.
4. **User-Friendly Interface**: Provide an intuitive and simple web-based interface for users to upload images and view results.

---

## ⚙️ Features

- **Object Detection**: Detect damaged car parts using YOLOv8.
- **Cost Estimation**: Estimate repair costs based on detected damage.
- **Image Upload**: Upload car images via a web-based interface.
- **Real-Time Results**: Display detection results and estimated costs in real-time.
- **Database Management**: Store vehicle, user, and spare parts information using MySQL.
- **Visual Damage Display**: View damaged parts highlighted in the uploaded image.

---

## 🛠️ Technologies Used

- **Backend**: 
  - Flask (Python web framework)
  - YOLOv8 (for object detection)
  - MySQL (for database management)
- **Frontend**: 
  - HTML/CSS (for user interface)
  - JavaScript (for frontend logic)
- **Libraries**: 
  - OpenCV (for image processing)
  - Matplotlib (for image visualization)
  - Ultralytics (YOLOv8 integration)

---
## 💻 Usage
- **Sign Up**: Create an account by filling out your personal details and vehicle information.
- **Log In**: Use your credentials to log in to the system.
- **Upload Image**: Upload an image of the damaged vehicle.
- **View Results**: The system detects the damaged parts and provides estimated repair costs.
- **Download Image**: Optionally, download the image with detected parts highlighted.

## 🤖 Model Information
- **YOLOv8 Object Detection**: The model was trained on a custom dataset of vehicle parts, including the bonnet, bumper, dickey, door, fender, light, and windshield.
- **Detection Accuracy**: The model achieves high accuracy in detecting vehicle parts, ensuring reliable damage assessment.

## 🚀 Future Improvements
- **Multi-language Support**: Extend the system to support multiple languages.
- **Damage Severity Analysis**: Improve the system to estimate the extent of damage in more detail.
- **Insurance Integration**: Allow integration with insurance companies for seamless claim processing.
- **Mobile App**: Develop a mobile app version for on-the-go damage detection.

---

## 📝 Setup and Installation

### Prerequisites
- Python 3.11.8
- MySQL Server
- Virtual Environment (optional, but recommended)
  
### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sahilkhan-7/accident-damage-detection.git
   cd accident-damage-detection
   ```

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MySQL Database**:
 - Create a new MySQL database.
 - Update the database credentials in the config.py file:
  ```python
  DB_HOST = 'localhost'
  DB_USER = 'root'
  DB_PASSWORD = 'yourpassword'
  DB_NAME = 'vehicle_damage_detection'
  ```
4. Run the Application:
  ```bash
  python app.py
  ```
