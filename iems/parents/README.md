# Parents API

This module provides API endpoints and data models for managing parent records in the IEMS system.

## Endpoints

### Create Parent

- **POST** `/v1/parents/`
- **Roles:** `ADMIN`, `ACADEMIC_STAFF`, `PRINCIPAL`
- **Body:**  
    ```json
    {
        "id": "UUID",
        "student_id": "UUID",
        "father_name": "string (max 32)",
        "mother_name": "string (max 32)",
        "contact_no": "string (max 16)",
        "email_id": "email (max 32)"
    }
    ```
- **Responses:**
    - `201`: Success (empty)
    - `409`: Duplicate parent
    - `404`: Student not found

---

### Get Parent by ID

- **GET** `/v1/parents/<parent_id>`
- **Roles:** All except `STUDENT`
- **Response:**  
    ```json
    {
        "id": "UUID",
        "student_id": "UUID",
        "father_name": "string",
        "mother_name": "string",
        "contact_no": "string",
        "email_id": "email",
        "active": true
    }
    ```
    - `404`: Parent not found

---

### Get Parent by Student ID

- **GET** `/v1/parents/student/<student_id>`
- **Roles:** All except `PARENTS`
- **Response:** Same as above

---

### Update Parent

- **PUT** `/v1/parents/<parent_id>`
- **Roles:** `ADMIN`, `ACADEMIC_STAFF`, `PRINCIPAL`, `PARENTS`
- **Body:**  
    ```json
    {
        "father_name": "string (max 32, optional)",
        "mother_name": "string (max 32, optional)",
        "contact_no": "string (max 16, optional)",
        "email_id": "email (max 32, optional)"
    }
    ```
- **Responses:**
    - `200`: Success (empty)
    - `403`: Access denied
    - `404`: Parent not found
    - `409`: Duplicate parent

---

### Delete Parent

- **DELETE** `/v1/parents/<parent_id>`
- **Roles:** `ADMIN`, `ACADEMIC_STAFF`, `PRINCIPAL`
- **Response:**  
    - `200`: Success (empty)
    - `404`: Parent not found