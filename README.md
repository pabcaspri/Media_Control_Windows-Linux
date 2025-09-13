Remote PC Control with Flask
=============================

This project is a basic Flask web app that turns your phone into a remote control for your PC.
It is especially useful when you don’t have a TV remote or a Firestick, but still want to control
Netflix, YouTube, or any media from the couch.

Features
--------
- Volume up / down / mute
- Play / pause
- Forward / backward
- Lock screen
- Sleep PC

Requirements
------------
- Python 3.8 or higher
- Flask

On Windows you also need:
    pip install comtypes

On Linux you need:
    sudo apt install alsa-utils playerctl

How to run
----------
1. Clone this repository or download the files.
2. Install dependencies:\
   ```bash
       pip install flask
   ```
4. Run the server:
      ```bash
       python controlMain.py
   ```
6. Get your PC IP address (ipconfig on Windows, ifconfig on Linux).
7. From your phone (same WiFi), open:
       http://<your_pc_ip>:5000

Usage
-----
The web page will show 8 buttons in a grid:
- Backward / Forward
- Lock / Volume Up
- Sleep / Volume Down
- Play-Pause / Mute

Pressing a button will send the command to your PC.
