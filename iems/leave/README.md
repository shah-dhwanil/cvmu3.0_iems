# Leave Management API

This module provides endpoints for managing student leave requests in the IEMS system.

## Endpoints

### Create Leave Request

- **POST** `/v1/leave/`
- **Roles:** `STUDENT`, `ADMIN`
- **Body:**  
    ```json
    {
        "student_id": "UUID",
        "from_date": "YYYY-MM-DD",
        "to_date": "YYYY-MM-DD",
        "reason": "string",
        "document_id": "UUID (optional)"
    }
    ```
- **Response:**  
    ```json
    { "id": "UUID" }
    ```

---

### Get Leave by ID

- **GET** `/v1/leave/<leave_id>`
- **Response:**  
    ```json
    {
        "id": "UUID",
        "student_id": "UUID",
        "student_name": "string",
        "from_date": "YYYY-MM-DD",
        "to_date": "YYYY-MM-DD",
        "reason": "string",
        "status": "submitted|declined_counciller|approved_counciller|declined_hod|approved",
        "document_id": "UUID or null"
    }
    ```

---

### Get Leaves by Student

- **GET** `/v1/leave/student/<student_id>`
- **Roles:** `STUDENT`
- **Response:**  
    ```json
    {
        "leaves": [ /* Array of Get Leave response objects */]
    }
    ```

---

### Get Pending Leaves (HOD/Teacher)

- **GET** `/v1/leave/pending`
- **Roles:** `HOD`, `TEACHER`
- **Response:**  
    ```json
    {
        "leaves": [/* Array of Get Leave response objects */]
    }
    ```

---

### Update Leave

- **PATCH** `/v1/leave/<leave_id>`
- **Body:**  
    ```json
    {
        "from": "YYYY-MM-DD (optional)",
        "to": "YYYY-MM-DD (optional)",
        "reason": "string (optional)",
        "document_id": "UUID (optional)"
    }
    ```
- **Response:**  
    - `{}` on success

---

### Update Leave Status

- **PATCH** `/v1/leave/<leave_id>/status`
- **Roles:** `TEACHER`, `HOD`, `ADMIN`
- **Body:**  
    ```json
    { "accepted": true|false }
    ```
- **Response:**  
    - `{}` on success

---

### Delete Leave

- **DELETE** `/v1/leave/<leave_id>`
- **Response:**  
    - `{}` on success

---

## Error Responses

- **404 Not Found:**  
    ```json
    {
        "error": "leave_not_found",
        "message": "Leave not found"
    }
    ```
