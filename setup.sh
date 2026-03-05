#!/bin/bash
set -m
echo "Setting up 3D Word Cloud..."

# Backend
echo "Setting up backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Frontend
echo "Setting up frontend..."
cd frontend
npm install
cd ..

# Start servers
echo "Starting servers..."

cd backend
source venv/bin/activate
uvicorn main:app --host localhost --port 8000 --reload 2>&1 | sed 's/^/[backend] /' &
BACKEND_PID=$!
cd ..

cd frontend
npm run dev 2>&1 | sed 's/^/[frontend] /' &
FRONTEND_PID=$!
cd ..

echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait