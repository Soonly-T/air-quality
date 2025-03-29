#!/bin/bash

# Replace 'script_name.py' with the name of your Python script
SCRIPT_NAME="bot.py"


# Check if the script is running
if pgrep -f "$SCRIPT_NAME" > /dev/null
then
    echo "The script $SCRIPT_NAME is running."
    
else
    echo "The script $SCRIPT_NAME is not running."
    source ./air-quality/bin/activate
    python3 ./$SCRIPT_NAME &
    echo "The script $SCRIPT_NAME has been started."

fi
