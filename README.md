# Capture_Motion
Requirement - Inbuilt camera/ External Webcam

This is a python based motion detection system using openCV and tkinter. Inititally it is set to use inbuilt device camera. External webcam also can be connected.
Run this python file first.
At first capture a static frame. Now after capturing this, you can start a session to detect change. It will compare the captured frame with current frame.
If any change is detected, it will make a square around the object.
For every appearance of object, current date and time will be stored.
You can also save this time duration of captured motion in a csv format (default)
After saving, open it to view motion duration plot.
