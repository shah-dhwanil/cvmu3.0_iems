# Files API

This module provides endpoints for uploading and retrieving files in the IEMS system.

## Endpoints

### Upload a File

- **URL:** `/v1/files/`
- **Method:** `POST`
- **Request:**
    - Form-data with key `file_upload` (one or more files)
- **Response:**
    - `200 OK` with JSON: `{ "id": "<uuid>" }`
    - `400 Bad Request` if no file is uploaded

### Download a File

- **URL:** `/v1/files/<uuid>`
- **Method:** `GET`
- **Response:**
    - Returns the file as an attachment if found
    - `404 Not Found` if file does not exist
