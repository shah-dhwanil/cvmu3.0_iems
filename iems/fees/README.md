# Fees API

This module provides endpoints for managing student fees, including creation, retrieval, updating, deletion, and status management.

## Endpoints

### Create Fees

- **POST** `/v1/fees/`
- **Roles:** ADMIN, PRINCIPAL, ACCOUNT_STAFF, STUDENT

#### Request Body

```json
{
    "date": "YYYY-MM-DD",
    "student_id": "string",
    "type": "tution_fees | exam_fees | card_fees | others",
    "payment_type": "cheque | upi | neft | rtgs | others",
    "transaction_id": "string (max 128 chars)",
    "amount": float,
    "docs_uuid": "UUID (optional)",
    "status": "PENDING"
}
```

#### Response

```json
{
    "id": "UUID",
    "recipt_id": int
}
```

---

### Get Fees by ID

- **GET** `/v1/fees/<fees_id>`

#### Response

```json
{
    "id": "UUID",
    "recipt_id": int,
    "date": "YYYY-MM-DD",
    "student_id": "UUID",
    "enrollment_id": "string",
    "type": "tution_fees | exam_fees | card_fees | others",
    "payment_type": "cheque | upi | neft | rtgs | others",
    "transaction_id": "string",
    "amount": float,
    "docs_uuid": "UUID or null",
    "status": "PENDING | ACCEPTED | REJECTED"
}
```

---

### Get Fees by Student

- **GET** `/v1/fees/student/<student_id>`

#### Response

```json
{
    "fees": [ /* Array of Get Fees by ID response objects */ ]
}
```

---

### Update Fees

- **PATCH** `/v1/fees/<fees_id>`
- **Roles:** ADMIN, PRINCIPAL, ACCOUNT_STAFF

#### Request Body

```json
{
    "date": "YYYY-MM-DD",
    "type": "tution_fees | exam_fees | card_fees | others",
    "payment_type": "cheque | upi | neft | rtgs | others",
    "transaction_id": "string (max 128 chars)",
    "amount": float
}
```

#### Response

```json
{}
```

---

### Delete Fees

- **DELETE** `/v1/fees/<fees_id>`
- **Roles:** ADMIN, PRINCIPAL, ACCOUNT_STAFF

#### Response

```json
{}
```

---

### Get Pending Fees

- **GET** `/v1/fees/pending/`
- **Roles:** ADMIN, PRINCIPAL, ACCOUNT_STAFF

#### Response

```json
{
    "fees": [ /* Array of Get Fees by ID response objects */ ]
}
```

---

### Update Fees Status

- **PATCH** `/v1/fees/<fees_id>/status`
- **Roles:** ADMIN, PRINCIPAL, ACCOUNT_STAFF

#### Request Body

```json
{
    "accepted": true | false
}
```

#### Response

```json
{}
```

---

## Error Responses

### Fees Not Found

```json
{
    "error": "fees_not_found",
    "message": "Fees record not found"
}
```