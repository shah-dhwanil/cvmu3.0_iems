# Events API

This module provides RESTful endpoints for managing events in the IEMS system.

## Endpoints

### Create Event

- **POST** `/v1/events/`
- **Body:**  
    ```json
    {
        "tile": "string",
        "description": "string (optional)",
        "date": "YYYY-MM-DD",
        "start_time": "HH:MM:SS",
        "end_time": "HH:MM:SS",
        "location": "string (optional)",
        "docs_id": "UUID (optional)"
    }
    ```
- **Response:**  
    `200 OK`  
    ```json
    { "id": "UUID" }
    ```

### Get Event

- **GET** `/v1/events/<event_id>`
- **Response:**  
    `200 OK`  
    ```json
    {
        "id": "UUID",
        "tile": "string",
        "description": "string",
        "date": "YYYY-MM-DD",
        "start_time": "HH:MM:SS",
        "end_time": "HH:MM:SS",
        "location": "string",
        "docs_id": "UUID"
    }
    ```
    `404 Not Found`  
    ```json
    { "error": "event_not_found", "message": "Event not found" }
    ```

### Get All Events

- **GET** `/v1/events/`
- **Response:**  
    `200 OK`  
    ```json
    {
        "events": [
            {
                "id": "UUID",
                "tile": "string",
                "description": "string",
                "date": "YYYY-MM-DD",
                "start_time": "HH:MM:SS",
                "end_time": "HH:MM:SS",
                "location": "string",
                "docs_id": "UUID"
            }
        ]
    }
    ```

### Update Event

- **PATCH** `/v1/events/<event_id>`
- **Body:** (any subset of event fields)
- **Response:**  
    `200 OK`  
    ```json
    {}
    ```
    `404 Not Found`  
    ```json
    { "error": "event_not_found", "message": "Event not found" }
    ```

### Delete Event

- **DELETE** `/v1/events/<event_id>`
- **Response:**  
    `200 OK`  
    ```json
    {}
    ```
    `404 Not Found`  
    ```json
    { "error": "event_not_found", "message": "Event not found" }
    ```