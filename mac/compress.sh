#!/usr/bin/env bash
# Compress the ai_tutor.py and setup.py folder into a zip file. 
# This package will be downloaded by the notebook instances. Like so:
# ! pip install https://raw.githubusercontent.com/wolfpaulus/ai_tutor/main/package.zip > NUL
cd ./src
zip ../package.zip ./ai_tutor.py ./setup.py
cd ..
