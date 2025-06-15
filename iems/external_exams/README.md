# External Exams API

This module provides RESTful endpoints for managing external exam records for students.

## Endpoints

### Create External Exam

- **POST** `/v1/external_exams/`
- **Roles:** STUDENT
- **Request Body:**  
    ```json
    {
        "student_id": "UUID",
        "name": "string (max 64)",
        "score": "float (0-100)",
        "seat_no": "string (max 64)",
        "yoa": "int",
        "marksheet_uuid": "UUID (optional)",
        "rank": "int (optional)"
    }
    ```
- **Response:**  
    ```json
    {
        "id": "UUID"
    }
    ```

---

### Get External Exam by ID

- **GET** `/v1/external_exams/<exam_id>`
- **Response:**  
    ```json
    {
        "id": "UUID",
        "student_id": "UUID",
        "name": "string",
        "score": "float",
        "seat_no": "string",
        "yoa": "int",
        "rank": "int (optional)",
        "marksheet_uuid": "UUID (optional)"
    }
    ```
- **404:**  
    ```json
    {
        "error": "external_exam_not_found",
        "message": "External exam not found"
    }
    ```

---

### Get All External Exams for a Student

- **GET** `/v1/external_exams/student/<student_id>`
- **Response:**  
    ```json
    {
        "external_exams": [ ... ]
    }
    ```

---

### Update External Exam

- **PATCH** `/v1/external_exams/<exam_id>`
- **Roles:** STUDENT
- **Request Body:**  
    ```json
    {
        "name": "string (max 64)",
        "score": "float (0-100)",
        "seat_no": "string (max 64)",
        "yoa": "int",
        "rank": "int"
    }
    ```
- **Response:**  
    Empty object on success  
    **404:**  
    ```json
    {
        "error": "external_exam_not_found",
        "message": "External exam not found"
    }
    ```

---

### Delete External Exam

- **DELETE** `/v1/external_exams/<exam_id>`
- **Roles:** STUDENT
- **Response:**  
    Empty object on success  
    **404:**  
    ```json
    {
        "error": "external_exam_not_found",
        "message": "External exam not found"
    }
    ```