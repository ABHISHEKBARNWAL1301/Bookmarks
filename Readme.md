## User Registration API

This API allows new users to create an account by registering with a unique username and password. Passwords are securely hashed before being stored in the database.

### Endpoint

`POST /signup`

### Request Body

- **username** (string): The desired username for the user account. Must be unique.
- **password** (string): The password for the user account. This password will be hashed before storage for security purposes.

### Example Request

```json
{
  "username": "example_user",
  "password": "secure_password"
}
```


Response:
On successful registration, a confirmation message is returned with the registered username.

### Example Response:

```json
{
  "msg": "User created successfully",
  "username": "example_user"
}
```