# Kaas App

This is a full-stack application with a Next.js frontend and a Python backend.

## Prerequisites

- Node.js (v14 or later)
- npm (v6 or later)
- Python (v3.7 or later)
- pip (Python package manager)

## Installation

### Frontend

1. Navigate to the frontend directory:
   ```
   cd kaas-frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```

### Backend

1. Navigate to the backend directory:
   ```
   cd kaas-backend
   ```

2. It's recommended to create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Before you can log in, you need to create a user. You can do this by sending a POST request to the /users/ endpoint. You can use a tool like cURL or Postman to do this. Here's an example using cURL:

curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{"username": "admin", "password": "a", "is_admin": true}'
This will create an admin user with the username "admin" and password "a".

### Frontend

1. In the `kaas-frontend` directory, run:
   ```
   npm run dev
   ```
   This will start the development server, typically on `http://localhost:3000`.

### Backend

1. In the `kaas-backend` directory, run:
   ```
   python main.py
   ```
   This will start the backend server.

## Additional Configuration

- Make sure both frontend and backend are running simultaneously for the full functionality of the app.
- If you need to modify any environment variables or API endpoints, check the following files:
  - Frontend: `kaas-frontend/.env` (create if it doesn't exist)
  - Backend: Check `kaas-backend/main.py` for any configuration settings

## Troubleshooting

- If you encounter any issues with dependencies, make sure you're using the correct versions of Node.js and Python.
- Check the console output for both frontend and backend for any error messages.

For more detailed information about the project structure and components, refer to the source code documentation.