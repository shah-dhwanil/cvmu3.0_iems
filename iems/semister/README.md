# Semester API

This module provides API endpoints and repository logic for managing semesters in the IEMS system.

## Endpoints

All endpoints are prefixed with `/v1/semister`.

### Create Semester

- **POST /**  
    Create a new semester.
    - **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
    - **Request Body:**  
        ```json
        {
            "batch_id": "UUID",
            "sem_no": 1,
            "ongoing": true
        }
        ```
    - **Responses:**
        - `200 OK`: `{ "id": "UUID" }`
        - `404 Not Found`: Batch not found

### Get Semester by ID

- **GET /<semister_id>**  
    Retrieve a semester by its ID.
    - **Roles:** All except `PARENTS`
    - **Responses:**
        - `200 OK`: Semester details
        - `404 Not Found`: Semester not found

### Get Semesters by Branch

- **GET /branch/<branch_id>**  
    List all semesters for a given branch.
    - **Roles:** All except `STUDENT`, `PARENTS`
    - **Responses:**
        - `200 OK`: List of semesters

### Update Semester

- **PATCH /<semister_id>**  
    Update an existing semester.
    - **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
    - **Request Body:**  
        ```json
        {
            "batch_id": "UUID (optional)",
            "sem_no": 1,
            "ongoing": true
        }
        ```
    - **Responses:**
        - `200 OK`: Empty response
        - `404 Not Found`: Semester not found

### Delete Semester

- **DELETE /<semister_id>**  
    Soft-delete a semester (sets `active` to `false`).
    - **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
    - **Responses:**
        - `200 OK`: Empty response
        - `404 Not Found`: Semester not found