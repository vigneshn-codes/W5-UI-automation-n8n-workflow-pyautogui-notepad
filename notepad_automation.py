from flask import Flask, request, jsonify
import os
import pyautogui
import time
import subprocess

app = Flask(__name__)

FILE_NAME = "dateTime_update.txt"

def open_file():
    subprocess.Popen(["open", "-a", "TextEdit", FILE_NAME])
    time.sleep(2)

def focus_editor():
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.click(screenWidth / 2, screenHeight / 2)
    time.sleep(0.5)

def move_to_end():
    pyautogui.hotkey('command', 'down')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.3)

def save_and_close():
    pyautogui.hotkey('command', 's')
    time.sleep(0.5)

    pyautogui.hotkey('command', 'q')
    time.sleep(1)

    # Handle save popup if appears
    pyautogui.press('return')

def update_datetime(datetime_value):
    if not os.path.exists(FILE_NAME):
        open(FILE_NAME, "w").close()

    open_file()
    focus_editor()
    move_to_end()

    pyautogui.write('\n')
    pyautogui.write(datetime_value, interval=0.05)

    save_and_close()

# ✅ API endpoint
@app.route('/update-datetime', methods=['POST'])
def api_update():
    data = request.json
    datetime_value = data.get("datetime")

    if not datetime_value:
        return jsonify({"error": "Missing datetime"}), 400

    try:
        update_datetime(datetime_value)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)