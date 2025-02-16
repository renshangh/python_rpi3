#!/bin/bash

# Navigate to the project directory
cd /home/pi/python_rpi

# Add all changes to git
git add .

# Commit the changes with a message
git commit -m "Sync changes with GitHub"

# Push the changes to the remote repository
git push origin main
```
