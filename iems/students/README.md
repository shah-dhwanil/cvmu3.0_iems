# Students API

This module provides API endpoints and data models for managing student records in the IEMS system. It supports CRUD operations, batch/semester management, and document extraction using AI.

## Endpoints

### Create Student

- **POST** `/students/`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL
- **Body Schema:**  
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "gender": "M/F/O",
      "contact_no": "string",
      "email_id": "string",
      "batch_id": "uuid"
    }
    ```
- **Response Schema:**  
    `201 Created`
    ```json
    {
      "uid": "uuid",
      "enrollment_id": "string"
    }
    ```

### Get All Students

- **GET** `/students/`
- **Roles:** Not STUDENT or PARENTS
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "students": [
        {
          "id": "uuid",
          "enrollment_id": "string",
          "name": "string"
        }
      ]
    }
    ```

### Get Student by ID

- **GET** `/students/<student_id>`
- **Roles:** STUDENT, PARENTS
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "id": "uuid",
      "enrollment_id": "string",
      "first_name": "string",
      "last_name": "string",
      "gender": "M/F/O",
      "contact_no": "string",
      "email_id": "string",
      "batch_id": "uuid",
      "current_sem": "uuid"
    }
    ```
    or  
    `404 Not Found`

### Update Student

- **PUT** `/students/<student_id>`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL, STUDENT (self only)
- **Body Schema:** Partial or full student fields, e.g.:
    ```json
    {
      "first_name": "string",
      "contact_no": "string"
    }
    ```
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "id": "uuid",
      "enrollment_id": "string",
      "first_name": "string",
      "last_name": "string",
      "gender": "M/F/O",
      "contact_no": "string",
      "email_id": "string",
      "batch_id": "uuid",
      "current_sem": "uuid"
    }
    ```
    or  
    `404 Not Found`  
    or  
    `409 Conflict`

### Delete Student

- **DELETE** `/students/<student_id>`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "detail": "Student deleted"
    }
    ```
    or  
    `404 Not Found`

### Update Current Semester

- **PUT** `/students/current-sem`
- **Roles:** ADMIN, ACADEMIC_STAFF, PRINCIPAL
- **Body Schema:**  
    ```json
    {
      "branch_id": "uuid",
      "current_sem": "uuid"
    }
    ```
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "detail": "Current semester updated"
    }
    ```

### Get Students by Semester

- **GET** `/students/course/<student_id>`
- **Roles:** Not STUDENT or PARENTS
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "students": [
        {
          "id": "uuid",
          "enrollment_id": "string",
          "name": "string",
          "current_sem": "uuid"
        }
      ]
    }
    ```
    or  
    `404 Not Found`

### Extract Aadhaar Data

- **GET** `/students/extract_aadhaar/<uid>`
- **Description:** Extracts Aadhaar details from uploaded file using AI.
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "aadhaar_number": "string",
      "name": "string",
      "dob": "YYYY-MM-DD",
      "gender": "M/F/O"
    }
    ```

### Extract Result Data

- **GET** `/students/extract_result/<uid>`
- **Description:** Extracts marksheet details from uploaded file using AI.
- **Response Schema:**  
    `200 OK`
    ```json
    {
      "student_id": "uuid",
      "subjects": [
        {
          "name": "string",
          "marks": "number"
        }
      ],
      "total": "number",
      "result": "PASS/FAIL"
    }
    ```