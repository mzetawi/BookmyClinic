# BookMyClinic 🏥

**BookMyClinic** is a Django-based web application that allows patients to register, search for doctors, book appointments, and leave reviews. Doctors can manage appointments, update their profiles, and view patient feedback.

---

## 🌟 Features
- Patient & Doctor registration and login  
- Admin approval workflow for doctors  
- Book, confirm, cancel, and complete appointments  
- Patient reviews with average doctor rating  
- Doctor dashboard & Patient dashboard  
- Secure authentication with sessions  
- File uploads for doctors’ certificates and ID cards  

---

## 🚀 Installation

 1. Clone the repository
```bash
#git clone https://github.com/your-username/BookMyClinic.git
cd BookMyClinic
```bash

2. Create virtual environment

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


#3. Install dependencies
pip install -r requirements.txt


4. Run migrations
python manage.py migrate

5. Create superuser (Admin account)
python manage.py createsuperuser

6. Start the development server
python manage.py runserver

---

## 📸 Screenshots

### 🔑 Admin Login Page
<img width="664" height="429" alt="Admin Login" src="https://github.com/user-attachments/assets/e8edbba0-49f9-471a-b27e-4d3460d57d12" />

### ⚙️ Django Administration
<img width="1352" height="761" alt="Django Admin" src="https://github.com/user-attachments/assets/bd0df932-37df-4488-87af-c34cd4155a57" />

### 👤 Login Page
<img width="774" height="586" alt="Login Page" src="https://github.com/user-attachments/assets/efc68459-0273-4086-8ecb-1b98d6b134c2" />

### 🆕 Register a New Account
<img width="556" height="333" alt="Register Account" src="https://github.com/user-attachments/assets/55027e8b-1aac-4055-b15f-477bfcab4e06" />

### 🧑‍⚕️ Patient Account
<img width="770" height="610" alt="Patient Account" src="https://github.com/user-attachments/assets/671e4a4d-30af-4ceb-b5c5-63d31c9140a6" />

### 📊 Patient Dashboard
<img width="1352" height="757" alt="Patient Dashboard" src="https://github.com/user-attachments/assets/cd44c8d6-18ff-48c6-b705-29120b2e227d" />

### 👨‍⚕️ Doctor Account
<img width="642" height="718" alt="Doctor Account" src="https://github.com/user-attachments/assets/94073cc5-dec6-474e-8bfa-5b1956dc9887" />

### ⏳ Pending Approval (Doctor Account)
<img width="548" height="437" alt="Pending Approval" src="https://github.com/user-attachments/assets/e209721b-7a5e-4901-8e14-a2c38a8e297a" />

### 🩺 Doctor Dashboard
<img width="1352" height="878" alt="Doctor Dashboard" src="https://github.com/user-attachments/assets/65271c11-5527-41a8-a612-2287beb6d6c1" />

---

**Note:** AJAX is used throughout the app to improve user experience for both patients and doctors.



