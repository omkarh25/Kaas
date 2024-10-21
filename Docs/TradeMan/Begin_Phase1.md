Day 1 (October 11th): Setting Up the Infrastructure and Backend Services

Server Setup:

Set up Coolify as the server infrastructure.

Configure the server environment, including creating necessary virtual environments and setting up system dependencies.

Ensure Docker is installed and properly configured for container orchestration.

Verify network configurations and firewall settings to allow secure access to the server.

Containerization:

Prepare Docker Environment:

Install Docker and Docker Compose on the server.

Create Dockerfiles for the FastAPI backend and PyQT frontend components.

Containerize Backend and Frontend:

Write Docker configurations to containerize FastAPI for backend processing.

Create a Docker configuration for PyQT that can interact with the backend.

Container Orchestration:

Use Docker Compose to set up multi-container applications, ensuring all dependencies are linked and functioning.

Testing Containers:

Run initial containers locally to ensure they build and run without errors before deploying to the server.

Backend Development:

Setting Up FastAPI:

Set up the basic FastAPI application structure, including routing, middleware, and error handling.

Create a Git repository and configure version control to ensure proper tracking of changes.

Accounts Present Module:

Implement the "Accounts Present" endpoint that allows users to view their financial accounts.

Define API contracts for the "Accounts Present" module to ensure smooth frontend-backend communication.

User Story: As a user, I want to view all my current accounts in one place so that I can have a consolidated view of my financial obligations.

Database Configuration:

PostgreSQL Setup:

Install PostgreSQL on the server, ensuring it is secured with proper authentication.

Create a new database for AccQT to store financial data.

Table Creation:

Define and create tables for accounts, transactions, goals, and other relevant financial data.

Establish relationships between tables (e.g., linking transactions to specific accounts).

Testing Database Connection:

Connect FastAPI to PostgreSQL and verify read/write operations for testing database integrity.

Data Validation:

Define Pydantic Models:

Create Pydantic models for account and transaction data, specifying the expected data types and validation rules.

Validation Testing:

Write unit tests to ensure that all Pydantic models validate incoming data correctly.

Test edge cases, such as invalid or missing data fields, to verify robustness.

Error Handling:

Implement error handling mechanisms within FastAPI for invalid data submissions, providing meaningful error messages to guide users.