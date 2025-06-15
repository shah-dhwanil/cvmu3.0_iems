# Notices API

This module provides endpoints for managing notices in the IEMS system. It supports creating, retrieving, updating, and deleting notices, as well as filtering by target audience and batch.

## Endpoints

### Create Notice

- **POST** `/v1/notices/`
- **Roles Allowed:** Staff, HOD, Admin (not Student/Parents)
- **Body:**  
    ```json
    {
        "title": "string (max 32)",
        "description": "string",
        "target_audience": "string (optional)",
        "batch_id": "UUID (optional)",
        "docs_id": "UUID (optional)"
    }
    ```
- **Response:**  
    ```json
    { "id": "UUID" }
    ```

---

### Get Notice by ID

- **GET** `/v1/notices/<notice_id>`
- **Response:**  
    ```json
    {
        "id": "UUID",
        "created_by": "UUID",
        "title": "string",
        "description": "string",
        "target_audience": "string (optional)",
        "batch_id": "UUID (optional)",
        "docs_id": "UUID (optional)"
    }
    ```

---

### Get All Notices

- **GET** `/v1/notices/`
- **Response:**  
    ```json
    {
        "notices": [ ... ]
    }
    ```

---

### Get Notices by Batch

- **GET** `/v1/notices/batch/<batch_id>`
- **Roles Allowed:** Student
- **Response:**  
    ```json
    {
        "notices": [ ... ]
    }
    ```

---

### Get Notices by Target Audience

- **GET** `/v1/notices/target/<target_audience>`
- **Response:**  
    ```json
    {
        "notices": [ ... ]
    }
    ```

---

### Update Notice

- **PATCH** `/v1/notices/<notice_id>`
- **Roles Allowed:** Staff, HOD, Admin (not Student/Parents)
- **Body:**  
    ```json
    {
        "title": "string (optional, max 32)",
        "description": "string (optional)",
        "target_audience": "string (optional)",
        "batch_id": "UUID (optional)",
        "docs_id": "UUID (optional)"
    }
    ```
- **Response:**  
    - 200: Success  
    - 404: Notice not found

---

### Delete Notice

- **DELETE** `/v1/notices/<notice_id>`
- **Roles Allowed:** Staff, HOD, Admin (not Student/Parents)
- **Response:**  
    - 200: Success  
    - 404: Notice not found

