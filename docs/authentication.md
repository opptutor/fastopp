# Authentication System

This FastAPI application includes a comprehensive authentication system with both web-based and API authentication. We use a **hybrid approach** that combines:

- **[FastAPI Users](https://github.com/fastapi-users/fastapi-users)** for password hashing and user management
- **Custom JWT authentication** for API access
- **Custom session-based authentication** for the admin panel

## Admin Panel Authentication

The admin panel uses session-based authentication similar to Django's admin interface. **Authentication verifies users against the database** instead of using hardcoded credentials.

### Access Admin Panel

1. **Visit**: http://localhost:8000/admin/
2. **Login with any superuser account**:
   - Username: `admin@example.com` (or any other superuser email)
   - Password: `admin123` (or the actual password for that user)

### Features

- ✅ **Session-based authentication**
- ✅ **Secure password verification**
- ✅ **Superuser permission checking**
- ✅ **Database user lookup**
- ✅ **User management interface**

## API Authentication

The application provides JWT-based authentication for API access.

### Get Authentication Token

```bash
curl -X POST http://localhost:8000/login \
  -u "admin@example.com:admin123" \
  -H "Content-Type: application/json"
```

**Response**:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Use Authentication Token

```bash
curl -X GET http://localhost:8000/admin/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## Test Data

The application comes with pre-loaded test data for authentication testing:

### Users

- **Superuser**: `admin@example.com` / `admin123`
- **Test Users**: `john@example.com`, `jane@example.com`, `bob@example.com` / `test123`

## Implementation Details

### FastAPI Users Integration

The application uses FastAPI Users for:
- Password hashing and verification
- User model management
- Registration and login endpoints

### Custom JWT Authentication

JWT tokens are used for:
- API access authentication
- Stateless authentication for external clients
- Token-based session management

### Session-Based Admin Authentication

The admin panel uses:
- Database-backed session storage
- Secure cookie-based sessions
- User permission verification against database records 