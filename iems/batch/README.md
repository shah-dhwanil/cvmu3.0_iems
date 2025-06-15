# Batch API

This module provides API endpoints for managing academic batches in the IEMS system. It supports creating, retrieving, updating, and deleting batch records, as well as batch creation for all branches in a given year.

## Endpoints

### Create a Batch

- **POST** `/v1/batch/`
- **Roles:** ADMIN, PRINCIPAL, ACADEMIC_STAFF
- **Body:**  
    ```json
    {
        "branch": "string",
        "year": 2024,
        "hod_id": "uuid",
        "counciller_id": "uuid",
        "active": true
    }
    ```
- **Response:**  
    ```json
    { "id": "uuid" }
    ```

### Create Batches for All Branches in a Year

- **POST** `/v1/batch/create_all/<year:int>`
- **Roles:** ADMIN, PRINCIPAL
- **Response:**  
    ```json
    { "ids": [{ "id": "uuid" }, ...] }
    ```

### Get Batch by ID

- **GET** `/v1/batch/<batch_id:uuid>`
- **Response:**  
    ```json
    {
        "id": "uuid",
        "branch": "string",
        "year": 2024,
        "hod_id": "uuid",
        "counciller_id": "uuid"
    }
    ```

### Get Batches by Year

- **GET** `/v1/batch/<year:int>`
- **Roles Not Allowed:** STUDENT, PARENTS
- **Response:**  
    ```json
    {
        "batches": [
            {
                "id": "uuid",
                "branch": "string",
                "year": 2024,
                "hod_id": "uuid",
                "counciller_id": "uuid"
            }
        ]
    }
    ```

### Get Batch by Branch and Year

- **GET** `/v1/batch/<branch_name:str>/<year:int>`
- **Roles Not Allowed:** STUDENT, PARENTS
- **Response:**  
    Same as "Get Batch by ID"

### Update Batch

- **PATCH** `/v1/batch/<batch_id:uuid>`
- **Roles:** ADMIN, PRINCIPAL, ACADEMIC_STAFF
- **Body:**  
    Partial or full fields of batch (see CreateBatchRequest)
- **Response:**  
    Empty object `{}`

### Delete (Deactivate) Batch

- **DELETE** `/v1/batch/<batch_id:uuid>`
- **Roles:** ADMIN, PRINCIPAL, ACADEMIC_STAFF
- **Response:**  
    Empty object `{}`

## Error Responses

- **404 Not Found:**  
    ```json
    {
        "error": "batch_not_found",
        "message": "Batch not found"
    }
    ```
