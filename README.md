# Hospital Backend System Test

> Django Backend api for Hospital Backend System Test.
> ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg) > ![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)

## Requirements (Prerequisites)

Tools and packages required to successfully install this project.
For example:

- Python 3.7 and up [Install](https://python.org)
- Postgres 14.0 and up [Install](https://postgres.com/)

## Installation (DEVELOPMENT SETUP)

- Create a .env file in root directory to override all environmental variables

- You can also set the variable as system variables

A step by step list of commands.

`$ git clone project-ul`

`$ python3 -m venv env`

`$ source env/bin/activate`

`$ pip install -r requirements.txt`

`$ python manage.py migrate`

`$ python manage.py runserver`

`$ redis-server`

`$ celery -A core  worker -l info`

`$ celery -A core beat -l info`

---

## DOCUMENTATION

A secure backend system for hospitals to manage user signups, patient-doctor assignments, doctor notes, and dynamic task scheduling. Uses a **live LLM** to extract actionable steps from notes and **Celery Beat** for scheduling reminders. Ensures sensitive data is protected with end-to-end encryption.

---

## Design Justification

### **Authentication**

- **Django's built-in authentication**: Secure, well-tested, and integrates seamlessly with Django REST Framework.
- **Password hashing**: Uses Django's default hashing (PBKDF2) for secure password storage.

### **Encryption**

- **End-to-end encryption**: Django's `signing` module encrypts patient notes, ensuring only the patient and doctor can access them.
- **Data integrity**: Prevents tampering with notes.

### **Scheduling Strategy**

- **Celery with Celery Beat**: Handles dynamic task scheduling and periodic reminders.
  - **Reminders**: Sends timely reminders for actionable tasks (e.g., daily medication).
  - **Resilience**: Automatically reschedules missed reminders (e.g., if a patient misses a daily medication reminder).
  - **Periodic Tasks**: Runs the `check_pending_reminders` task every 5 minutes to ensure no reminders are missed.

### **LLM Integration**

- **Live LLM (e.g., Google Gemini Flash)**: Extracts actionable steps from doctor notes.
  - **Checklist**: Immediate one-time tasks (e.g., buy medication).
  - **Plan**: Scheduled tasks (e.g., take medication daily for 7 days).
- **Dynamic Updates**: New notes cancel existing tasks and create new ones based on the latest instructions.

### **Data Storage**

- **PostgreSQL**: Reliable, scalable, and integrates well with Django.
- **ActionableTask model**: Stores task details (type, status, scheduling) for checklists and plans.

---

## Key Features

1. **User Management**:

   - Signup as patient or doctor.
   - Role-based access control.

2. **Patient-Doctor Assignment**:

   - Patients choose from available doctors.
   - Doctors view their assigned patients.

3. **Doctor Notes & Actionable Steps**:

   - Encrypted note submission.
   - **LLM Integration**: Extracts actionable steps:
     - **Checklist**: Immediate tasks (e.g., buy medication).
     - **Plan**: Scheduled tasks (e.g., take medication daily for 7 days).
   - **Dynamic Scheduling**: Reminders are scheduled and rescheduled if missed.

4. **API Endpoints**:
   - User signup and authentication.
   - Patient doctor selection.
   - Doctor note submission and task retrieval.

---

## Example Workflow

1. **Patient Signs Up**:

   - Registers and selects a doctor.

2. **Doctor Submits Notes**:

   - Submits a note (e.g., "Take medication daily for 7 days").

3. **LLM Processes Notes**:

   - Extracts actionable steps:
     - **Checklist**: Buy medication.
     - **Plan**: Take medication daily for 7 days.

4. **Celery Beat Schedules Reminders**:

   - Sends daily reminders to the patient.
   - Reschedules reminders if the patient misses a check-in.

5. **Patient Checks In**:
   - Marks a task as completed, and the system moves to the next reminder.

---
