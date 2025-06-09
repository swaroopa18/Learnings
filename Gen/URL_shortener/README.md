# URL Shortener

A full-stack URL shortener application built with Flask and React, featuring Material-UI for a modern user interface.

## Features

- Shorten long URLs to 6-character alphanumeric codes
- View a list of all shortened URLs with creation timestamps
- Automatic redirection from short URLs to original URLs
- Copy shortened URLs to clipboard
- Modern Material-UI interface
- SQLite database for storing URLs
- Responsive design

## Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask server:
   ```bash
   python app.py
   ```

The backend server will run on http://localhost:5000

### Frontend Setup

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
   npm start
   ```

The frontend application will run on http://localhost:3000

## Usage

1. Open your browser and go to http://localhost:3000
2. Enter a long URL in the input field
3. Click "Shorten URL" to generate a shortened version
4. View all shortened URLs in the table below
5. Use the action buttons to:
   - Copy the shortened URL to clipboard
   - Open the shortened URL in a new tab

## API Endpoints

- `POST /api/shorten`: Create a shortened URL
  - Request body: `{ "url": "https://example.com" }`
  - Response: `{ "original_url": "https://example.com", "short_url": "http://localhost:5000/abc123", "created_at": "2023-05-20T12:00:00Z" }`

- `GET /api/urls`: List all shortened URLs
  - Response: `[{ "original_url": "https://example.com", "short_url": "http://localhost:5000/abc123", "created_at": "2023-05-20T12:00:00Z" }]`

- `GET /<short_code>`: Redirect to original URL
  - Redirects to the original URL if found
  - Returns 404 if not found

## Technologies Used

- Backend:
  - Python
  - Flask
  - SQLAlchemy
  - SQLite

- Frontend:
  - React
  - Material-UI
  - React Icons 