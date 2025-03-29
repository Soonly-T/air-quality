#!/bin/bash

# Replace 'script_name.py' with the name of your Python script
SCRIPT_NAME="bot.py"

# Infinite loop to keep the script running
while true; do
    # Check if the script is running
    if pgrep -f "$SCRIPT_NAME" > /dev/null
    then
        echo "The script $SCRIPT_NAME is already running."
    else
        echo "Starting $SCRIPT_NAME..."
        source ./air-quality/bin/activate
        python3 ./$SCRIPT_NAME &
        echo "The script $SCRIPT_NAME has been started."
    fi

    # Wait for 5 minutes before checking again
    sleep 300
done
