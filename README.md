# NeuroRecords - Neurology Medical Records System

NeuroRecords is a full-stack web application designed for managing neurology patient medical records. It allows for the importation and visualization of medical imaging studies (CT, MRI) from DICOM files.

## Features

- **Patient Management**: View and manage a list of patients.
- **DICOM Import**: Import medical studies by selecting local folders containing DICOM files.
- **Study Visualization**: View patient studies and series details.
- **Modern UI**: Built with Next.js and TailwindCSS for a responsive and clean interface.

## Technology Stack

- **Frontend**: Next.js (React), TailwindCSS, TypeScript
- **Backend**: Django, Django REST Framework
- **Database**: MongoDB (via Djongo)
- **DICOM Processing**: pydicom

## Prerequisites

- Python 3.8+
- Node.js 18+
- MongoDB (running locally on port 27017)

## Setup Instructions

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```
   The backend will run at `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will run at `http://localhost:3000` (or 3001 if 3000 is in use).

## Usage

1. Ensure MongoDB is running.
2. Start both backend and frontend servers.
3. Open your browser to the frontend URL.
4. Use the "Import Study" feature to load DICOM files from your local machine.
