# Courses API

This module provides RESTful endpoints for managing courses in the IEMS system. It supports creating, retrieving, updating, and deleting courses, as well as querying courses by teacher or student.

## Endpoints

### Create Course

- **POST** `/courses/`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
- **Body:**  
    ```json
    {
        "sem_id": "UUID",
        "subject_id": "UUID",
        "taught_by": "UUID"
    }
    ```
- **Response:**  
    ```json
    {
        "id": "UUID"
    }
    ```

---

### Get Course by ID

- **GET** `/courses/<course_id>`
- **Response:**  
    ```json
    {
        "id": "UUID",
        "sem_id": "UUID",
        "subject_id": "UUID",
        "taught_by": "UUID"
    }
    ```
- **404:**  
    ```json
    {
        "error": "course_not_found",
        "message": "Course not found"
    }
    ```

---

### Get Courses by Teacher

- **GET** `/courses/teacher/<teacher_id>`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`, `TEACHER`
- **Response:**  
    ```json
    {
        "courses": [
            {
                "id": "UUID",
                "name": "string",
                "sem_id": "UUID",
                "branch": "string",
                "year": 1
            }
        ]
    }
    ```

---

### Get Courses by Student

- **GET** `/courses/student/<student_id>`
- **Not Allowed:** `PARENTS`
- **Response:**  
    ```json
    {
        "courses": [
            {
                "id": "UUID",
                "name": "string",
                "by": "UUID"
            }
        ]
    }
    ```

---

### Update Course

- **PATCH** `/courses/<course_id>`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
- **Body:**  
    ```json
    {
        "sem_id": "UUID",
        "subject_id": "UUID",
        "taught_by": "UUID"
    }
    ```
- **Response:**  
    Empty object (`{}`) on success  
    404 error if not found

---

### Delete Course

- **DELETE** `/courses/<course_id>`
- **Roles:** `ADMIN`, `PRINCIPAL`, `ACADEMIC_STAFF`
- **Response:**  
    Empty object (`{}`) on success  
    404 error if not found

---
