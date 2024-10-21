
# Coderunner Agent System - Step-by-Step Implementation Guide

## Project Overview
This document provides a comprehensive, step-by-step guide to implementing a **Human-in-the-Loop Coderunner Agent System** using **Next.js** (Frontend) and **FastAPI** (Backend) based on SOLID principles and MVC architecture. We will also integrate GitHub Actions for CI/CD, and MkDocs for documentation.

### Target Environment: Mac M2 Pro (Development)
This guide is tailored for development on a Mac M2 Pro machine, avoiding Docker for the development environment.

## Prerequisites

Make sure you have the following tools installed:

- **Node.js** (for Next.js frontend)
- **Python 3.9+** (for FastAPI backend)
- **Git** (for version control)
- **MkDocs** (for documentation)
- **Pipenv** (or virtualenv for managing Python dependencies)
- **VSCode** (recommended for development)

## Project Folder Structure
We will use the following folder structure for the project:

```
root/
│
├── backend/                   # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Entry point for FastAPI
│   │   └── models/            # DB models or Pydantic models
│   │   └── routes/            # FastAPI routes (e.g., agent routes)
│   │   └── services/          # Business logic services (SOLID principles)
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # Next.js Frontend
│   ├── pages/                 # Next.js pages (MVC: View)
│   └── components/            # Reusable React components
│   └── services/              # API calls to FastAPI (MVC: Controller)
│   └── package.json           # JavaScript dependencies
│
├── .env                       # Environment variables for both frontend & backend
├── mkdocs.yml                 # MkDocs configuration for documentation
└── README.md                  # Project documentation
```

## Step 1: Set Up Backend (FastAPI)

1. **Create Virtual Environment**

    To manage Python dependencies, we’ll use **Pipenv** or **virtualenv**.

    ```bash
    cd backend
    pipenv install fastapi uvicorn
    ```

    If you're using `virtualenv`, you can do:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn
    ```

2. **Install Necessary Dependencies**

    ```bash
    pip install pydantic openai bs4 requests
    ```

3. **Create FastAPI Application**

    Create the FastAPI app in `backend/app/main.py`:

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Coderunner Agent API"}
    ```

4. **Run FastAPI Locally**

    Run the FastAPI server to test it:

    ```bash
    uvicorn app.main:app --reload
    ```

5. **Define the Agent Routes**

    Create a new file `backend/app/routes/agent.py` to handle agent-related routes:

    ```python
    from fastapi import APIRouter
    from coderunner import WebScraperAgent

    router = APIRouter()

    @router.post("/agents/run")
    async def run_agent():
        url = "https://example.com"
        agent = WebScraperAgent()
        result = await agent.run(url)
        return {"result": result}
    ```

## Step 2: Set Up Frontend (Next.js)

1. **Install Node.js and Create Next.js App**

    ```bash
    cd frontend
    npx create-next-app@latest .
    ```

2. **Set Up Pages and Components**

    Create a simple page `frontend/pages/index.js` to interact with the backend:

    ```jsx
    import { useState } from 'react';

    export default function HomePage() {
        const [output, setOutput] = useState("");

        const handleRunAgent = async () => {
            const res = await fetch('http://localhost:8000/agents/run', {
                method: 'POST',
                body: JSON.stringify({ task: 'code generation' })
            });
            const data = await res.json();
            setOutput(data.result);
        }

        return (
            <div>
                <button onClick={handleRunAgent}>Run Agent</button>
                <p>{output}</p>
            </div>
        );
    }
    ```

3. **Run Next.js Locally**

    ```bash
    npm run dev
    ```

4. **Connect Frontend to Backend**

    Ensure that the frontend can make API calls to the FastAPI backend running on port 8000.

## Step 3: Testing Methodology

1. **Backend Testing (FastAPI)**

    We will use `pytest` to test the backend.

    - Install `pytest`:

    ```bash
    pip install pytest
    ```

    - Create a test file `backend/tests/test_main.py`:

    ```python
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    def test_read_root():
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Coderunner Agent API"}
    ```

    - Run tests:

    ```bash
    pytest
    ```

2. **Frontend Testing (Next.js)**

    We will use `Jest` for unit testing React components.

    - Install Jest:

    ```bash
    npm install jest --save-dev
    ```

    - Add this to your `package.json`:

    ```json
    "scripts": {
      "test": "jest"
    }
    ```

    - Create a simple test `frontend/components/HomePage.test.js`:

    ```jsx
    import { render, screen } from '@testing-library/react';
    import HomePage from '../pages/index';

    test('renders button', () => {
      render(<HomePage />);
      const button = screen.getByText(/Run Agent/i);
      expect(button).toBeInTheDocument();
    });
    ```

    - Run tests:

    ```bash
    npm run test
    ```

## Step 4: CI/CD with GitHub Actions

1. **Create GitHub Action for Backend**

    Add a GitHub Action in `.github/workflows/backend.yml`:

    ```yaml
    name: Backend CI

    on: [push]

    jobs:
      test:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v2
        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: 3.9
        - name: Install dependencies
          run: |
            pip install -r backend/requirements.txt
        - name: Run tests
          run: |
            pytest
    ```

2. **Create GitHub Action for Frontend**

    Add a GitHub Action in `.github/workflows/frontend.yml`:

    ```yaml
    name: Frontend CI

    on: [push]

    jobs:
      test:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v2
        - name: Set up Node.js
          uses: actions/setup-node@v2
          with:
            node-version: '16'
        - name: Install dependencies
          run: |
            npm install
        - name: Run tests
          run: |
            npm run test
    ```

## Step 5: Documentation with MkDocs

1. **Install MkDocs and Material Theme**

    ```bash
    pip install mkdocs mkdocs-material
    ```

2. **Configure MkDocs**

    Add this to `mkdocs.yml`:

    ```yaml
    site_name: Coderunner Agent System
    theme:
      name: 'material'
    nav:
      - Home: index.md
      - API: api.md
    ```

3. **Deploy Documentation**

    Once configured, you can deploy the documentation using:

    ```bash
    mkdocs serve  # For local testing
    mkdocs gh-deploy  # For deployment to GitHub Pages
    ```

---

## Conclusion

This guide covers setting up a **FastAPI backend**, a **Next.js frontend**, a **CI/CD pipeline** with GitHub Actions, and **MkDocs** for documentation. Testing methodologies for both frontend and backend have also been detailed to ensure code quality.

