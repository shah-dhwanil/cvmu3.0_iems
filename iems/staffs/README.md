# Staff API

This module provides API endpoints for managing staff members in the IEMS system.

## Endpoints

### Create Staff

- **POST** `/v1/staff/`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL
- **Request Body:**
    ```json
    {
      "id": "UUID (required)",
      "first_name": "string (max 32)",
      "last_name": "string (max 32)",
      "contact_no": "string (max 16)",
      "email_id": "string (email, max 32)",
      "qualification": "string (optional)",
      "experience": "string (optional)"
    }
    ```
- **Response Schema:**
    - `201 Created`
      ```json
      {
        "id": "UUID",
        "first_name": "string",
        "last_name": "string",
        "contact_no": "string",
        "email_id": "string",
        "qualification": "string",
        "experience": "string",
        "active": true
      }
      ```
    - `409 Conflict`
      ```json
      { "error": "duplicate_staff" }
      ```
    - `404 Not Found`
      ```json
      { "error": "user_not_found" }
      ```

---

### Get All Staff

- **GET** `/v1/staff/`
- **Response Schema:**
    ```json
    {
      "staff_members": [
        {
          "id": "UUID",
          "name": "string"
        }
      ]
    }
    ```

---

### Get Staff by ID

- **GET** `/v1/staff/<staff_id>`
- **Response Schema:**
    - `200 OK`
      ```json
      {
        "id": "UUID",
        "first_name": "string",
        "last_name": "string",
        "contact_no": "string",
        "email_id": "string",
        "qualification": "string",
        "experience": "string",
        "active": true
      }
      ```
    - `404 Not Found`
      ```json
      { "error": "staff_not_found" }
      ```

---

### Update Staff

- **PUT** `/v1/staff/<staff_id>`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL, TEACHER, ACCOUNT_STAFF, HOD
- **Request Body:**  
    - Any updatable staff fields (see create)
- **Response Schema:**
    - `200 OK`
      ```json
      {
        "id": "UUID",
        "first_name": "string",
        "last_name": "string",
        "contact_no": "string",
        "email_id": "string",
        "qualification": "string",
        "experience": "string",
        "active": true
      }
      ```
    - `404 Not Found`
      ```json
      { "error": "staff_not_found" }
      ```
    - `409 Conflict`
      ```json
      { "error": "duplicate_staff" }
      ```
    - `403 Forbidden`
      ```json
      { "error": "forbidden" }
      ```

---

### Delete Staff

- **DELETE** `/v1/staff/<staff_id>`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL
- **Response Schema:**
    - `200 OK`
      ```json
      { "message": "Staff deleted successfully" }
      ```
    - `404 Not Found`
      ```json
      { "error": "staff_not_found" }
      ```

