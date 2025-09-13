from flask import Flask, render_template_string
import os
import platform
import ctypes  # needed for Windows virtual key presses



app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Control</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <style>
    body {
        margin: 0;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #0b0f14;
        font-family: system-ui, sans-serif;
    }
    .grid {
        display: grid;
        grid-template-columns: 1fr 1fr;  /* 2 columns */
        grid-template-rows: repeat(4, 1fr); /* 4 rows */
        gap: 16px;
        width: 90vw;
        height: 85vh;
    }
    form {
        margin: 0;
        height: 100%;
    }
    button {
        width: 100%;
        height: 100%;
        background: #1a2430;
        color: #e6edf3;
        border: none;
        border-radius: 16px;
        font-size: clamp(1rem, 2.5vw, 1.5rem);
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        -webkit-tap-highlight-color: transparent;
        transition: transform 0.1s ease, background 0.2s ease;
    }
    button:active {
        transform: scale(0.95);
        background: #243344;
    } </style>
</head>
<body>

 <div class="grid">
    <form action="/backward" method="post">
      <button>⬅ Backward</button>
    </form>
    <form action="/forward" method="post">
      <button>Forward ➡</button>
    </form>
    <form action="/lock" method="post">
      <button>🔒 Lock</button>
    </form>
    <form action="/up" method="post">
      <button>🔊 Vol +</button>
    </form>
    <form action="/sleep" method="post">
      <button>😴 Sleep</button>
    </form>
    <form action="/down" method="post">
      <button>🔉 Vol -</button>
    </form>
    <form action="/playpause" method="post">
      <button>⏯ Play / Pause</button>
    </form>
    <form action="/mute" method="post">
      <button>🔇 Mute</button>
    </form>
  </div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

# Volume routes
@app.route("/up", methods=["POST"])
def up():
    control_action("up")
    return home()

@app.route("/down", methods=["POST"])
def down():
    control_action("down")
    return home()

@app.route("/mute", methods=["POST"])
def mute():
    control_action("mute")
    return home()

# Media route
@app.route("/playpause", methods=["POST"])
def playpause():
    control_action("playpause")
    return home()

# Media Forward
@app.route("/forward", methods=["POST"])
def forward():
    control_action("forward")
    return home()

# Media backward
@app.route("/backward", methods=["POST"])
def backward():
    control_action("backward")
    return home()

@app.route("/lock", methods=["POST"])
def lock():
    if platform.system() == "Windows":
        ctypes.windll.user32.LockWorkStation()
    return home()

@app.route("/sleep", methods=["POST"])
def sleep():
    if platform.system() == "Windows":
        ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
    return home()

def control_action(action: str):
    system = platform.system()

    if system == "Windows":
        # Virtual key codes
        VK_VOLUME_MUTE       = 0xAD
        VK_VOLUME_DOWN       = 0xAE
        VK_VOLUME_UP         = 0xAF
        VK_MEDIA_PLAY_PAUSE  = 0xB3
        VK_FORWARD_KEY  = 0x27
        VK_BACKWARD_KEY = 0x25


        KEYEVENTF_EXTENDEDKEY = 0x0001
        KEYEVENTF_KEYUP       = 0x0002

        def press_vk(vk):
            ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_EXTENDEDKEY, 0)
            ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

        if action == "up":
            press_vk(VK_VOLUME_UP)
        elif action == "down":
            press_vk(VK_VOLUME_DOWN)
        elif action == "mute":
            press_vk(VK_VOLUME_MUTE)
        elif action == "playpause":
            press_vk(VK_MEDIA_PLAY_PAUSE)
        elif action == "forward":
            press_vk(VK_FORWARD_KEY)
        elif action == "backward":
            press_vk(VK_BACKWARD_KEY)
            

    elif system == "Linux":
        # Requires: sudo apt install alsa-utils (for amixer) and optionally playerctl
        if action == "up":
            os.system("amixer set Master 5%+")
        elif action == "down":
            os.system("amixer set Master 5%-")
        elif action == "mute":
            os.system("amixer set Master toggle")
        elif action == "playpause":
            os.system("playerctl play-pause")  # install with: sudo apt install playerctl

if __name__ == "__main__":
    # Access from phone: http://<your_PC_IP>:5000
    app.run(host="0.0.0.0", port=5000)