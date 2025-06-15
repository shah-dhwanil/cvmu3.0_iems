# Users API

This module provides endpoints and data models for managing users in the IEMS system.

## Endpoints

### Create User

- **POST** `/v1/users/`
- **Roles:** `admin`, `principal`
- **Body:**  
    ```json
    {
        "username": "string (max 32 chars)",
        "password": "string (min 8 chars)",
        "role": "RoleEnum",
        "active": true
    }
    ```
- **Responses:**
    - `200`: `{ "id": "UUID" }`
    - `409`: `{ "error_slug": "duplicate_username", "error": "...", "context": {} }`

---

### Get User

- **GET** `/v1/users/<user_id>`
- **Roles:**  
    - `student`: can only access own user
    - others: unrestricted
- **Responses:**
    - `200`:  
        ```json
        {
            "id": "UUID",
            "username": "string",
            "role": "RoleEnum",
            "active": true
        }
        ```
    - `404`: `{}`

---

### Update User Role

- **PATCH** `/v1/users/<user_id>/role`
- **Roles:** `admin`, `principal`
- **Body:**  
    ```json
    { "role": "RoleEnum" }
    ```
- **Responses:**
    - `200`: `{}`
    - `404`: `{}`

---

### Update User Password

- **PATCH** `/v1/users/<user_id>/password`
- **Roles:**  
    - `student`, `teacher`: can only update own password
    - others: unrestricted
- **Body:**  
    ```json
    { "password": "string (min 8 chars)" }
    ```
- **Responses:**
    - `200`: `{}`
    - `404`: `{}`

---

### Delete User

- **DELETE** `/v1/users/<user_id>`
- **Roles:** `admin`, `principal`
- **Responses:**
    - `200`: `{}`
    - `404`: `{}`

---

## RoleEnum

- `admin`
- `principal`
- `hod`
- `academic_staff`
- `teacher`
- `student`
- `parents`
- `account_staff`
- `others`
