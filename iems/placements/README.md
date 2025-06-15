# Placements API

This module provides API endpoints for managing student placements in the IEMS system.

## Endpoints

### Create Placement
- **POST** `/v1/placements/`
- **Roles Allowed:** All except `PARENTS`
- **Body:**  
    ```json
    {
        "student_id": "UUID",
        "company_name": "string",
        "role": "string",
        "package": "decimal",
        "status": "offered|accepted|rejected", // optional
        "letter_uid": "UUID" // optional
    }
    ```
- **Response:**  
    ```json
    { "id": "UUID" }
    ```

### Create Placement by Enrollment
- **POST** `/v1/placements/enrollment`
- **Roles Allowed:** All except `PARENTS`
- **Body:**  
    ```json
    {
        "enroll_id": "string",
        "company_name": "string",
        "role": "string",
        "package": "decimal",
        "status": "offered|accepted|rejected", // optional
        "letter_uid": "UUID" // optional
    }
    ```
- **Response:**  
    ```json
    { "id": "UUID" }
    ```

### Get Placement by ID
- **GET** `/v1/placements/<placement_id>`
- **Roles Allowed:** All
- **Response:** Placement details or 404 if not found.

### Get All Placements
- **GET** `/v1/placements/`
- **Roles Allowed:** All except `PARENTS`
- **Response:**  
    ```json
    {
        "placements": [
            {
                "id": "UUID",
                "first_name": "string",
                "enrollment_id": "string",
                "company_name": "string",
                "package": "float",
                "status": "offered|accepted|rejected",
                "letter_uid": "UUID"
            }
        ]
    }
    ```

### Get Placements by Student
- **GET** `/v1/placements/student/<student_id>`
- **Roles Allowed:** All except `PARENTS`
- **Response:** List of placements for the student.

### Update Placement Status
- **POST** `/v1/placements/status/<placement_id>`
- **Roles Allowed:** `STUDENT`
- **Body:**  
    ```json
    { "status": "offered|accepted|rejected" }
    ```
- **Response:** Empty or 404 if not found.

### Update Placement
- **PATCH** `/v1/placements/<placement_id>`
- **Roles Allowed:** All except `PARENTS`
- **Body:**  
    ```json
    {
        "company_name": "string",
        "role": "string",
        "package": "float",
        "letter_uid": "UUID"
    }
    ```
- **Response:** Empty or 404 if not found.

### Delete Placement
- **DELETE** `/v1/placements/<placement_id>`
- **Roles Allowed:** All except `PARENTS`
- **Response:** Empty or 404 if not found.
