# ForgeAI API Documentation

## Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.forgeai.com/api/v1
```

## Authentication

All protected endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <supabase_access_token>
```

---

## Endpoints

### System

#### `GET /health`

Health check endpoint.

**Response** `200 OK`:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development"
}
```

---

### Authentication

#### `POST /api/v1/auth/register`

Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response** `201 Created`:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "avatar_url": null
  }
}
```

#### `POST /api/v1/auth/login`

Login with email and password.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response** `200 OK`: Same as register response.

#### `POST /api/v1/auth/logout`

🔒 **Requires Authentication**

Logout the current user.

**Response** `200 OK`:
```json
{
  "message": "Logged out successfully"
}
```

#### `GET /api/v1/auth/me`

🔒 **Requires Authentication**

Get current user profile.

**Response** `200 OK`:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "avatar_url": null
}
```

---

### Documents

#### `POST /api/v1/documents/upload`

🔒 **Requires Authentication**

Upload a document (PDF, DOCX, TXT, XLSX).

**Request**: `multipart/form-data`
- `file`: The document file (max 50MB)

**Response** `201 Created`:
```json
{
  "id": "uuid",
  "filename": "stored-name.pdf",
  "original_filename": "report.pdf",
  "file_type": "pdf",
  "file_size": 1024000,
  "status": "uploaded",
  "message": "Document uploaded successfully. Processing will begin shortly."
}
```

#### `GET /api/v1/documents`

🔒 **Requires Authentication**

List all documents for the current user.

#### `GET /api/v1/documents/{id}`

🔒 **Requires Authentication**

Get document details.

#### `DELETE /api/v1/documents/{id}`

🔒 **Requires Authentication**

Delete a document and all its chunks.

#### `GET /api/v1/documents/{id}/status`

🔒 **Requires Authentication**

Get document processing status.

---

### Chat

#### `POST /api/v1/chat/sessions`

🔒 **Requires Authentication**

Create a new chat session.

#### `GET /api/v1/chat/sessions`

🔒 **Requires Authentication**

List all chat sessions.

#### `GET /api/v1/chat/sessions/{id}`

🔒 **Requires Authentication**

Get a chat session with all messages.

#### `POST /api/v1/chat/sessions/{id}/messages`

🔒 **Requires Authentication**

Send a message and receive an AI response.

#### `DELETE /api/v1/chat/sessions/{id}`

🔒 **Requires Authentication**

Delete a chat session and all messages.

---

## Interactive API Docs

When running in development, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
