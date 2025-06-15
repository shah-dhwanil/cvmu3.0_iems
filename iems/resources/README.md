# Resources API

This module provides endpoints and data models for managing educational resources such as lecture notes, lab manuals, books, and more.

## Endpoints

### Create Resource

- **POST** `/v1/resources/`
- **Roles Allowed:** All except `STUDENT`, `PARENTS`
- **Body:**  
    ```json
    {
        "subject_id": "UUID",
        "title": "string",
        "shared_by": "UUID (optional)",
        "type": "lecture_notes | lab_manual | books | reference_material | syllabus | others",
        "docs_id": "UUID"
    }
    ```
- **Response:**  
    ```json
    { "id": "UUID" }
    ```

---

### Get Resource by ID

- **GET** `/v1/resources/<resource_id>`
- **Response:**  
    ```json
    {
        "id": "UUID",
        "subject_id": "UUID",
        "title": "string",
        "shared_by": "UUID",
        "type": "lecture_notes | lab_manual | books | reference_material | syllabus | others",
        "docs_id": "UUID",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
    ```
    Returns resource details or 404 if not found.

---

### Get Resources by Subject

- **GET** `/v1/resources/subject/<subject_id>`
- **Response:**  
    ```json
    [
        {
            "id": "UUID",
            "subject_id": "UUID",
            "title": "string",
            "shared_by": "UUID",
            "type": "lecture_notes | lab_manual | books | reference_material | syllabus | others",
            "docs_id": "UUID",
            "created_at": "datetime",
            "updated_at": "datetime"
        },
        ...
    ]
    ```
    List of resources for the subject.

---

### Get Resources by Staff

- **GET** `/v1/resources/staff/<staff_id>`
- **Response:**  
    ```json
    [
        {
            "id": "UUID",
            "subject_id": "UUID",
            "title": "string",
            "shared_by": "UUID",
            "type": "lecture_notes | lab_manual | books | reference_material | syllabus | others",
            "docs_id": "UUID",
            "created_at": "datetime",
            "updated_at": "datetime"
        },
        ...
    ]
    ```
    List of resources shared by the staff member.

---

### Update Resource

- **PATCH** `/v1/resources/<resource_id>`
- **Roles Allowed:** All except `STUDENT`, `PARENTS`
- **Body:**  
    ```json
    {
        "title": "string",
        "type": "lecture_notes | lab_manual | books | reference_material | syllabus | others"
    }
    ```
- **Response:**  
    Empty or 404 if not found.

---

### Delete Resource

- **DELETE** `/v1/resources/<resource_id>`
- **Roles Allowed:** All except `STUDENT`, `PARENTS`
- **Response:**  
    Empty or 404 if not found.
