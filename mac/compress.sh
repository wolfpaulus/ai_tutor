#!/usr/bin/env bash
# Compress the client folder into a zip file. 
# This package will be downloaded by the notebook instances.
cd ./client
zip ../package.zip ./ai_tutor.py ./setup.py
cd ..
