# Attendance API

This module provides endpoints and repository logic for managing student attendance in courses. It is part of the IEMS system.

## Endpoints

All endpoints are prefixed with `/attendence/v1`.

### Mark Attendance

- **POST** `/attendence/v1/mark`
- **Roles:** `TEACHER`, `ADMIN`
- **Body:**  
    ```json
    {
        "course_id": "UUID",
        "class_time": "datetime",
        "present_student_ids": ["UUID", ...],
        "absent_student_ids": ["UUID", ...]
    }
    ```
- **Response:**  
    `200 OK` on success.

---

### Get Attendance by Course and Time

- **GET** `/attendence/v1/course/<course_id>/<class_time>`
- **Roles:** `TEACHER`
- **Response:**  
    ```json
    {
        "attendence_records": [
            {
                "id": "UUID",
                "student_id": "UUID",
                "present": true,
                "dont_care": false,
                "class_time": "datetime"
            }
        ]
    }
    ```

---

### Get Attendance by Student

- **GET** `/attendence/v1/student/<student_id>`
- **Roles:** Any (students can only access their own data)
- **Response:**  
    ```json
    {
        "attendence_records": [
            {
                "course_id": "UUID",
                "course_name": "string",
                "course_code": "string",
                "present_no": 0,
                "dont_care_no": 0,
                "total_no": 0
            }
        ]
    }
    ```

---

### Get Student Attendance by Course

- **GET** `/attendence/v1/course/<course_id>/<student_id>`
- **Response:**  
    Same as "Get Attendance by Course and Time".

---

### Update Attendance

- **PATCH** `/attendence/v1/<attendence_id>`
- **Roles:** `TEACHER`
- **Body:**  
    ```json
    {
        "id": "UUID",
        "present": true
    }
    ```
- **Response:**  
    `200 OK` on success, `404` if not found.

---

## Data Model

- **attendence**
    - `id`: UUID (PK)
    - `course_id`: UUID (FK)
    - `student_id`: UUID (FK)
    - `class_time`: TIMESTAMP
    - `present`: BOOLEAN
    - `dont_care`: BOOLEAN (default: false)
