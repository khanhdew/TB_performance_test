#!/bin/bash
echo "Starting script..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
read -r -p "1.Run subcriber 2.Run publisher " response
if [[ $response == 1 ]]; then
    python subscriber.py
elif [[ $response == 2 ]]; then
    python publisher.py
else
    echo "Invalid input"
fi
echo "Script completed"