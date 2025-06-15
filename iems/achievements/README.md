# Achievements API

This module provides RESTful API endpoints for managing student achievements in the IEMS system.

## Endpoints

### Create Achievement

- **POST** `/v1/achievements/`
- **Roles:** STUDENT
- **Request Body:**
    ```json
    {
        "name": "string (max 32 chars)",
        "type": "academic | sports | cultural | other",
        "pos": "participation | first | second | third | others",
        "docs_id": "UUID (optional)"
    }
    ```
- **Response:** 
    ```json
    { "id": "UUID" }
    ```

---

### Get Achievement by ID

- **GET** `/v1/achievements/<achievement_id>`
- **Response:**
    ```json
    {
        "id": "UUID",
        "student_id": "UUID",
        "name": "string",
        "type": "academic | sports | cultural | other",
        "pos": "participation | first | second | third | others",
        "docs_id": "UUID or null"
    }
    ```

---

### Get Achievements by Student

- **GET** `/v1/achievements/student/<student_id>`
- **Response:**
    ```json
    {
        "achievements": [ ...Achievement objects... ]
    }
    ```
- **Note:** Students can only access their own achievements.

---

### Update Achievement

- **PATCH** `/v1/achievements/<achievement_id>`
- **Roles:** STUDENT
- **Request Body:**
    ```json
    {
        "name": "string (max 32 chars)",
        "type": "academic | sports | cultural | other",
        "pos": "participation | first | second | third | others",
        "docs_id": "UUID"
    }
    ```
- **Response:** Empty object `{}` on success.

---

### Delete Achievement

- **DELETE** `/v1/achievements/<achievement_id>`
- **Roles:** STUDENT
- **Response:** Empty object `{}` on success.

---

## Error Responses

- **404 Not Found**
    ```json
    {
        "error": "achievement_not_found",
        "message": "Achievement not found"
    }
    ```
- **403 Forbidden**
    ```json
    {
        "error": "access_denied",
        "message": "Access denied"
    }
    ```

## Data Model

- **Achievement**
    - `id`: UUID
    - `student_id`: UUID
    - `name`: string (max 32)
    - `type`: enum (`academic`, `sports`, `cultural`, `other`)
    - `pos`: enum (`participation`, `first`, `second`, `third`, `others`)
    - `docs_id`: UUID (optional)
    - `created_at`: timestamp
