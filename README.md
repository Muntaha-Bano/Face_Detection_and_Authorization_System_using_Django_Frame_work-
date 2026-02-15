# 🚀 Face Recognition Authentication System (Django)

<div align="center"> <h3 style="color: #764ba2; margin-bottom: 30px;">Secure Authentication + Intelligent Conversations</h3><div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap;"> <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django"> <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"> <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Groq-000000?style=for-the-badge" alt="Groq"> <img src="https://img.shields.io/badge/DeepFace-FF6B6B?style=for-the-badge" alt="DeepFace"> </div></div>


---

## 📌 Project Overview

This system allows users to **register and authenticate using their face**. Facial features are extracted using deep learning models and matched using similarity metrics. The application is designed for **secure access control systems**, academic projects, and real-world experimentation with biometric authentication.

---

## ✨ Features

### 🔐 Face Recognition Authentication

* Real-time face detection using **OpenCV**
* Facial embeddings generated using **DeepFace / FaceNet**
* **Cosine similarity** for face matching
* Multi-user registration and authentication

### 👤 User Management

* User registration with face data
* Secure login using face recognition
* Session-based authentication

### ⚙️ Backend & Security

* Built with **Django**
* Environment variables for sensitive data (`.env`)
* Modular and scalable architecture

---

## 🛠️ Tech Stack

**Backend**

* Python 3.x
* Django 4.x / 5.x

**Computer Vision & AI**

* OpenCV
* DeepFace / FaceNet
* NumPy

**Database**

* MongoDB
* PyMongo

**Other Tools**

* dotenv (for environment variables)
* Git & GitHub

---

## 📂 Project Structure

```
face-recognition-chatbot/
├── F/                          # Django project
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── face_verification/         # Face recognition app
│   ├── services/
│   │   ├── face_services.py   # Face recognition logic
│   │   └── chat_services.py   # MongoDB chat operations
│   ├── templates/
│   │   ├── home.html         # Landing page
│   │   ├── signup.html       # Registration page
│   │   └── login.html        # Login page
│   ├── static/
│   │   └── css/
│   │       └── home.css      # Landing page styles
│   ├── views.py              # Face recognition views
│   ├── urls.py               # App URLs
│   └── face_images/          # Captured face storage
├── chatbot/                   # Chatbot app
│   ├── templates/
│   │   └── chatbot/
│   │       └── interface.html # Chat interface
│   ├── views.py              # Chatbot views
│   └── urls.py               # Chatbot URLs
├── media/                    # User uploaded media
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
└── .env                     # Environment variables
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
```



## ▶️ How to Run the Project

1. **Clone the repository**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run migrations**

```bash
python manage.py migrate
```

4. **Start the server**

```bash
python manage.py runserver
```

5. **Open in browser:**

```
http://127.0.0.1:8000/
```

---

## 📸 Screenshots

<p align="center">
  <img src="repository_Pics/home_page.jpeg" width="180" />&nbsp;
  <img src="repository_Pics/login_page.jpeg" width="180" />&nbsp;
  <img src="repository_Pics/sign_up_page.jpeg" width="180" />&nbsp;
  <img src="repository_Pics/verification.jpeg" width="180" />
  <img src="repository_Pics/chatbot.jpeg" width="180" />&nbsp;
  
</p>

---
