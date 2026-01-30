#!/bin/bash
# Start script for TheBoard - runs backend and frontend

echo "Starting TheBoard..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with:"
    echo "  API_KEY=your_api_key"
    echo "  MODEL=your_model_name"
    echo ""
fi

# Start backend in background
echo "Starting backend server on http://127.0.0.1:8000..."
python run_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start frontend server
echo "Starting frontend server on http://127.0.0.1:8080..."
echo "Open http://127.0.0.1:8080 in your browser"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

cd frontend
python -m http.server 8080

# Cleanup on exit
kill $BACKEND_PID 2>/dev/null
