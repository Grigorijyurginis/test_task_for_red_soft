# Mentorship API

A Django REST API for managing mentorship relationships between users. Includes user registration, JWT authentication with token blacklist, user detail/update functionality, and mentor-mentee links.

## Clone repo

```bash
git clone https://github.com/Grigorijyurginis/test_task_for_red_soft.git
cd mentorship-api
```

## Before install

Use python 3.10

## Setup

1. Create venv
2. `pip install -r requirements.txt`
3. `python manage.py migrate`
4. `python manage.py runserver`

## Api 

1. POST `api/registration` - Register new user
2. POST `api/login` - Get JWT tokens
3. GET `api/users` - Get list of users
4. GET `api/users/<id>` - Retrieve user info
5. PATCH `api/users/<id>` - Update your own user info
6. POST `api/logout` - Blacklist refresh token
7. POST `api/token/refresh` - 	Refresh access token

## Authentication & Tokens

JWT authentication is used via djangorestframework-simplejwt.

Access Token Lifetime: 20 minutes

Refresh Token Lifetime: 1 hour

Use the access token in the Authorization header for all protected routes:

Authorization: Bearer your_access_token

## Use Api

All routes except `/registration` and `/login` require authentication.

### Register
POST /api/registration

Request Example

`{
      "username": "john",
      "password": "12345678",
      "email": "john@example.com",
      "phone": "+79999999999",
      "mentor_username": "alice"
}`

Email, phone, mentor is optional. Mentor must be a valid existing user, if provided.


### Login

Request Example

`{
  "username": "your_username",
  "password": "your_password"
}`

Successful Response

`{
    "refresh": "your token",
    "access": "your token"
}`

* The access token should be used in the Authorization header to access protected endpoints.

* The refresh token is used to obtain a new access token once the original expires.

### User List

GET /api/users

Response Example

`[
  {
    "username": "john",
    "mentor_username": "alice"
  },
  {
    "username": "bob",
    "mentor_username": null
  }
]`

### User Detail

GET /api/users/id

Response Example

`{
  "id": 2,
  "username": "john",
  "password": "********",  // hash and visible only to yourself
  "phone": "1234567890",
  "email": "john@example.com",
  "mentor_username": "alice",
  "mentees": ["mike", "emma"]
}`

### Update User

PATCH /api/users/user_id

Only the logged-in user can update their own data.

Request Example

`{
  "email": "new_email@example.com",
  "phone": "123-456-7890",
  "mentor": "bob",
  "password": "newpassword123"
}`

To remove a mentor, send an empty string:

`{
  "mentor": ""
}`

### Logout (Token Blacklisting)

POST /api/logout

Request Example

`{
  "refresh": "your_refresh_token"
}`

This blacklists the refresh token, so it can no longer be used.
