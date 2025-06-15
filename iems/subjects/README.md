# Subjects API

This module provides RESTful endpoints for managing academic subjects in the IEMS system.

## Endpoints

### Create Subject

- **POST** `/v1/subjects/`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
- **Request Body:**
    ```json
    {
        "code": "string (max 16)",
        "name": "string (max 64)",
        "credits": "integer (1-10)"
    }
    ```
- **Response:**
    ```json
    {
        "id": "uuid"
    }
    ```

---

### Get Subject

- **GET** `/v1/subjects/<subject_id>`
- **Response:**
    ```json
    {
        "id": "uuid",
        "code": "string",
        "name": "string",
        "credits": "integer"
    }
    ```
- **404 Response:**
    ```json
    {
        "error": "subject_not_found",
        "message": "Subject not found"
    }
    ```

---

### Get All Subjects

- **GET** `/v1/subjects/`
- **Response:**
    ```json
    {
        "subjects": [
            {
                "id": "uuid",
                "code": "string",
                "name": "string",
                "credits": "integer"
            }
        ]
    }
    ```

---

### Update Subject

- **PATCH** `/v1/subjects/<subject_id>`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
- **Request Body:**
    ```json
    {
        "id": "uuid",
        "code": "string (max 16)",
        "name": "string (max 64)",
        "credits": "integer (1-10)"
    }
    ```
- **Response:** Empty object `{}` on success  
- **404 Response:** Same as Get Subject

---

### Delete Subject

- **DELETE** `/v1/subjects/<subject_id>`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
- **Response:** Empty object `{}` on success  
- **404 Response:** Same as Get Subject