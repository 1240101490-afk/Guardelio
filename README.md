# Guardelio — Web-Based Security Incident Training and Simulation System

Guardelio is a web-based cybersecurity training platform designed to help students practice incident response and improve cybersecurity decision-making through simulated security incidents.

Students can explore different incident scenarios, analyze situations, select response actions, and follow branching scenario paths based on their decisions. The system provides scoring, feedback, and progress tracking to support learning.

## Features

- **User Authentication:** Registration, login, and JWT-based authentication.
- **Student Dashboard:** Access training scenarios and track learning progress.
- **Incident Categories:** Malware Infection, Phishing and Social Engineering, DDoS and Network Disruption, Data Breach and Exfiltration, Insider Threats, and Network Intrusion.
- **Interactive Simulations:** Practice simulated cybersecurity incidents in a safe environment.
- **Decision-Based Branching:** Scenario progression depends on the student's selected decisions.
- **Scoring and Feedback:** Evaluate decisions and provide performance feedback.
- **Progress and History:** Review previous sessions and training progress.
- **Admin Management:** Manage users, scenarios, categories, steps, and related content.

## Technologies Used

### Frontend
- React.js
- Tailwind CSS
- JavaScript

### Backend
- Python
- Django
- Django REST Framework
- REST APIs
- JSON Web Token (JWT) Authentication

### Database
- MySQL

## System Workflow

1. The student registers or logs in.
2. The student opens the dashboard and selects an incident category.
3. The student reviews the scenario and starts the simulation.
4. The student analyzes the incident and selects a response option.
5. The simulation engine determines the next step based on the selected decision.
6. The system calculates the score and provides feedback.
7. The student reviews the final result and progress.

**Workflow:** Login → Dashboard → Scenario Selection → Incident Analysis → Decision → Next Step → Score and Feedback → Final Result

## System Architecture

Guardelio follows a layered web application architecture:

- **Presentation Layer:** React.js and Tailwind CSS provide the user interface.
- **API Layer:** Django REST Framework handles communication between the frontend and backend.
- **Business Logic Layer:** Processes simulation decisions, branching logic, scoring, and feedback.
- **Data Layer:** MySQL stores application data, including users, scenarios, steps, options, and progress.

## Installation and Setup

### Prerequisites

Install the following software before running the project:

- Python
- Node.js and npm
- MySQL Server
- Git (optional)

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

If you already have the project files, open a terminal in the project directory instead.

### 2. Backend Setup

Open a terminal in the backend directory.

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install the backend dependencies using the project's existing requirements file:

```bash
pip install -r requirements.txt
```

Configure the database credentials and other required environment variables according to your project configuration.

Create the MySQL database if it does not already exist, and ensure the Django database settings match your MySQL configuration.

Run database migrations:

```bash
python manage.py migrate
```

Start the backend development server:

```bash
python manage.py runserver
```

### 3. Frontend Setup

Open another terminal in the frontend directory.

Install the dependencies:

```bash
npm install
```

Start the frontend using the command configured in the project's `package.json`. For a typical Vite-based React project, use:

```bash
npm run dev
```

For other React setups, the appropriate start command may differ.

### 4. Access the Application

Open the local frontend URL displayed in the terminal.

The Django development server typically runs at:

```text
http://127.0.0.1:8000/
```

The frontend and backend must be configured to communicate through the correct API URL.

## Project Structure

The exact directory structure depends on the implementation.

A typical structure may look like this:

```text
Guardelio/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── ...
├── README.md
└── ...
```

## Intended Users

- **Students:** Practice incident response and improve decision-making.
- **Administrators:** Manage users and training scenarios.

## Project Objective

The main objective of Guardelio is to provide a safe, interactive learning environment where students can develop incident response skills through simulated cybersecurity scenarios without interacting with real cyberattacks.

## Future Enhancements

Potential future improvements include:

- Expanding the incident scenario library.
- Adding OWASP Top 10 security training scenarios.
- Introducing more detailed performance analytics.
- Developing advanced cybersecurity training labs.

## Disclaimer

Guardelio is an educational training and simulation platform. Its scenarios are simulated and intended for learning purposes; the system is not a replacement for a production Security Operations Center (SOC) or a real incident response platform.