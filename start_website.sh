#!/bin/bash

# Navigate to the correct directory
cd "$(dirname "$0")"

# Kill any existing Flask processes on port 5001
echo "Stopping any existing Flask processes..."
pkill -f "python3 app.py" 2>/dev/null || true

# Wait a moment for processes to stop
sleep 2

# Start the Flask app
echo "Starting your love story website..."
echo "Website will be available at: http://localhost:5001"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py 