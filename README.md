# CVMU3.0 IEMS - Integrated Educational Management System

CVMU Hackathon 3.0 project (IEMS) - A comprehensive educational management system built with Python/Sanic framework.

## Overview

IEMS is a complete educational management system designed to handle various aspects of academic institution management including student information, staff management, course scheduling, attendance tracking, fee management, and more.

## Features

### Core Modules

- **User Management** - Role-based access control (Admin, Principal, HOD, Teachers, Students, Parents)
- **Student Management** - Student profiles, enrollment, batch assignment
- **Staff Management** - Faculty and staff information management
- **Academic Management**
    - Batch and semester management
    - Subject and course management
    - Attendance tracking
    - Academic resources sharing
- **Administrative Features**
    - Fee management with payment tracking
    - Notice board system
    - Event management
    - Leave management
- **Advanced Features**
    - AI-powered document extraction (Aadhaar, academic results)
    - Placement tracking
    - Achievement records
    - External exam management
    - File management system

## Tech Stack

- **Backend**: Python with Sanic framework
- **Database**: PostgreSQL with UUID primary keys
- **Authentication**: PASETO based role-based access control
- **AI Integration**: Google Generative AI for document processing
- **Validation**: Pydantic schemas
- **Logging**: Structured logging with JSON output

## Getting Started

### Prerequisites

- Python 3.8+
- Rye
- PostgreSQL
- Google AI API key (for document processing features)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/shah-dhwanil/cvmu3.0_iems
   cd cvmu3.0_iems
   ```

2. Install dependencies
   ```bash
   rye sync
   ```

3. Set up environment variables (create `.env` file as shown below)    
    ```env
    # Server Configuration
    IEMS_SERVER_ENVIRONMENT = "DEV"|"PROD"

    # Key for PASETO Tokens
    IEMS_PASETO_SECRET_KEY = "..."

    #DATABASE URL
    IEMS_POSTGRES_DSN = "..."

    #GOOGLE GENERATIVE AI KEY
    IEMS_GOOGLE_API_KEY =".."
    ```

4. Set up the database
   ```bash
   # Run migrations
   rye run migration migrate
   ```

5. Start the server
   ```bash
   rye run dev
   ```

## API Endpoints & File Structure

The system provides RESTful APIs for all modules organized in a modular architecture:

### 🔐 Authentication & User Management
- **`/v1/auth`** - Authentication endpoints (login, logout, token management)
  - [`iems/auth/`](iems/auth/) - Authentication module
    - [`blueprint.py`](iems/auth/blueprint.py) - Route definitions
    - [`views.py`](iems/auth/views.py) - Request handlers
    - [`schemas.py`](iems/auth/schemas.py) - Request/response models
    - [`repository.py`](iems/auth/repository.py) - Database operations
    - [`middlewares.py`](iems/auth/middlewares.py) - Auth middleware

- **`/v1/users`** - User management operations
  - [`iems/users/`](iems/users/) - User management module
    - Standard module structure with CRUD operations for user accounts

### 👥 People Management
- **`/v1/students`** - Student operations (profiles, enrollment, academic records)
  - [`iems/students/`](iems/students/) - Student management module

- **`/v1/staff`** - Staff management (faculty, administrative staff)
  - [`iems/staffs/`](iems/staffs/) - Staff management module

- **`/v1/parents`** - Parent/guardian information and communications
  - [`iems/parents/`](iems/parents/) - Parent management module

### 📚 Academic Management
- **`/v1/subjects`** - Subject management and curriculum
  - [`iems/subjects/`](iems/subjects/) - Subject management module

- **`/v1/courses`** - Course management and scheduling
  - [`iems/courses/`](iems/courses/) - Course management module

- **`/v1/batch`** - Batch/class management
  - [`iems/batch/`](iems/batch/) - Batch management module

- **`/v1/semister`** - Semester management and academic calendar
  - [`iems/semister/`](iems/semister/) - Semester management module

- **`/v1/attendance`** - Attendance tracking and reports
  - [`iems/attendence/`](iems/attendence/) - Attendance management module

- **`/v1/resources`** - Academic resources sharing (lecture notes, books, materials)
  - [`iems/resources/`](iems/resources/) - Resource management module
    - Supports multiple resource types: lecture_notes, lab_manual, books, reference_material, syllabus, others
    - Role-based access (Students and Parents cannot create/modify resources)

### 🏢 Administrative Features
- **`/v1/fees`** - Fee management and payment tracking
  - [`iems/fees/`](iems/fees/) - Fee management module

- **`/v1/notices`** - Notice board and announcements
  - [`iems/notices/`](iems/notices/) - Notice management module

- **`/v1/events`** - Event management and calendar
  - [`iems/events/`](iems/events/) - Event management module

- **`/v1/leave`** - Leave application and approval system
  - [`iems/leave/`](iems/leave/) - Leave management module

### 🎯 Advanced Features
- **`/v1/achievements`** - Student achievement tracking
  - [`iems/achievements/`](iems/achievements/) - Achievement management module

- **`/v1/placements`** - Placement tracking and company interactions
  - [`iems/placements/`](iems/placements/) - Placement management module

- **`/v1/external_exams`** - External examination management
  - [`iems/external_exams/`](iems/external_exams/) - External exam management module

- **`/v1/files`** - File upload, storage, and retrieval system
  - [`iems/files/`](iems/files/) - File management module
    - Handles file uploads with UUID-based storage
    - Supports various file types with proper MIME type handling

## Application Architecture

### Core Structure
```
iems/
├── base/                    # Core application setup
│   ├── app.py              # Main Sanic application
│   ├── blueprints.py       # Blueprint registration
│   ├── middlewares.py      # Request/response middleware
│   ├── logging.py          # Structured logging setup
│   ├── postgres.py         # Database connection
│   ├── config.py           # Configuration management
│   └── decorators.py       # Custom decorators
├── [module]/               # Each API module follows this structure:
│   ├── blueprint.py        # Route definitions
│   ├── views.py           # Request handlers
│   ├── schemas.py         # Pydantic models
│   ├── repository.py      # Database operations
│   └── migrations/        # Database migrations
└── ...
```

### Standard Module Pattern
Each API module follows a consistent structure:

1. **`blueprint.py`** - Defines the Sanic blueprint with URL prefix and version
2. **`views.py`** - Contains route handlers with decorators for validation and authorization
3. **`schemas.py`** - Pydantic models for request/response validation
4. **`repository.py`** - Database access layer with CRUD operations
5. **`migrations/`** - SQL migration files for database schema

## Authentication
All protected endpoints require PASETO token authentication. Include the token in the Authorization header:
```
Authorization: Bearer <token>
```

## Role-based Access
The system supports the following roles with different access levels:
- **ADMIN** - Full system access
- **PRINCIPAL** - Institution-wide access
- **HOD** - Department-level access  
- **TEACHER** - Class and subject-level access
- **STUDENT** - Limited read access to own data
- **PARENTS** - Limited read access to child's data

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
