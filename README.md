# File Management System API

This project is a simple and secure file management backend built using Django and Django REST Framework.The main idea behind this project is to allow users to create folders, upload files and download them securely using authentication.
This was built mainly for learning purpose, but the structure is close to real world backend systems.

**What this project does**

* User registration and login using JWT authentication
* Each user can create their own folders
* Files can be uploaded only inside user folders
* Only allowed file types can be uploaded
* Users can download only their own files
* No user can access another user data

**Tech used**

* Django 4.2.7
* Django REST Framework
* Simple JWT for authentication
* SQLite database (for development)

**Setup and Installation**

Requirements
* Python 3.8 or above
* pip
* virtualenv (optional but recommanded)


### Installation steps

**clone the Repo**
-- git clone <your-repo-url>
-- cd file_management_system

**Create virtual environment**
-- python -m venv venv
-- source venv/bin/activate #for mac
-- venv\Scripts\activate #for windows



**Install dependencies**

uv pip install -r requirements.txt   # i am using uv so started with uv 


**Run migrations**
-- python manage.py makemigrations
-- python manage.py migrate


**Create superuser (optional)**
-- python manage.py createsuperuser

**Start the server**
-- python manage.py runserver


# API Endpoints

**Authentication APIs**
|  Method   |     Endpoint          | Description      |
|  ------   | -------------------  | ---------------- |
|  POST     | /api/auth/register/  | Register user    |
|  POST     | /api/auth/login/     | Login user       |
|  POST     | /api/auth/refresh/   | Refresh token    |
|  GET      | /api/auth/profile/   | Get user profile |
 


**Folder APIs**

|  Method  | Endpoint            | Description   |
|  ------  | -------------       | ------------- |
|  POST    | /api/create-folder/ | Create folder |
|  GET     | /api/folders/       | List folders  |


**File APIs**

| Method | Endpoint                        | Description   |
| ------ | -------------------------       | ------------- |
| POST   | /api/upload-file/               | Upload file   |
| GET    | /api/list-files//               | List files    |
| GET    | /api/file/{id}/download/        | Download file |



# How to use the API

**Register user**

POST /api/auth/register/

{
  "username": "johndoe",
  "email": "john@gmail.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}


**Login**

POST /api/auth/login/

{
  "username": "johndoe",
  "password": "SecurePass123!"
}


**Create folder**

POST /api/folders/
Authorization: Bearer <access_token>

{
  "name": "My Documents"
}


**Upload file**

-- This uses multipart form data

POST /api/files/
Authorization: Bearer <access_token>

Form data:
* name: Report 2024
* folder: 1
* file: select file


**Download file**

GET /api/files/1/download/
Authorization: Bearer <access_token>

>Only the owner of the file can download it

File upload rules
* Allowed file types: PDF, JPG, JPEG, PNG
* Max file size: 10MB
* File is rejected if validation fails


**Security details**
--- JWT authentication is used for all protected APIs
--- Users can access only their own folders and files
-- Folder names are unique per user
---File download is blocked if user is not owner


# Project structure


file_management_system/
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── file_management_system/
│   ├── settings.py
│   └── urls.py
├── media/
├── manage.py
├── requirements.txt
├── README.md
└── postman_collection.json



# Admin panel
Admin panel is available at:

-- http://127.0.0.1:8000/admin/


# Postman Collection

This project includes a Postman collection for testing all APIs

