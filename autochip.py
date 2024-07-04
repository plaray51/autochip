import pyautogui
import time
import logging
from flask import Flask, request, jsonify
from pywinauto.application import Application

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)

def locate_and_click(image_path, confidence=0.8, offset=(0, 0)):
    logging.info(f"Attempting to locate and click image: {image_path}")
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if location:
        adjusted_location = (location[0] + offset[0], location[1] + offset[1])
        logging.info(f"Found image: {image_path} at location: {location}, clicking at adjusted location: {adjusted_location}")
        pyautogui.moveTo(adjusted_location)
        time.sleep(0.5)
        pyautogui.click(adjusted_location)
        logging.info(f"Clicked on image: {image_path} at adjusted location: {adjusted_location}")
    else:
        logging.error(f"Image not found on screen: {image_path}")
        raise Exception(f"Image not found on screen: {image_path}")

def input_chips(chips):
    logging.info(f"Inputting chips: {chips}")
    for char in chips:
        if char.isdigit():
            locate_and_click(f'digit_{char}.png', confidence=0.9)
        elif char == '.':
            locate_and_click('decimal_point.png', confidence=0.9)
        elif char == 'x':
            locate_and_click('delete_button.png', confidence=0.9)
        time.sleep(0.1)

def clear_search_field():
    for _ in range(3):
        locate_and_click('blank_space.png', offset=(-175, 0))
        time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('backspace')
    time.sleep(1)

def activate_window(title):
    try:
        app = Application().connect(title_re=title)
        window = app.window(title_re=title)
        window.set_focus()
        return True
    except Exception as e:
        logging.error(f"Error activating window: {e}")
        return False

def distribute_chips(username, chips):
    logging.info("Activating ClubGG window")
    if not activate_window('ClubGG'):
        return False
    
    time.sleep(2)
    
    try:
        locate_and_click('search_field.png')
        pyautogui.write(username)
        pyautogui.press('enter')
        time.sleep(2)
        
        locate_and_click('member.png')
        time.sleep(2)
        
        locate_and_click('send_out_button.png')
        time.sleep(2)
        
        input_chips(chips)
        
        locate_and_click('confirm_send_out_button.png')
        time.sleep(2)
        
        clear_search_field()
        return True
    except Exception as e:
        logging.error(f"Error during chip distribution: {e}")
        return False

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        logging.info(f"Received webhook data: {data}")  # Log the received data
        
        username = data['data']['custom_fields']['ClubGG Username']
        product_title = data['data']['product_title']
        
        if "10" in product_title:
            chips = "10"
        elif "25" in product_title:
            chips = "25"
        elif "50" in product_title:
            chips = "50"
        elif "100" in product_title:
            chips = "100"
        else:
            logging.error(f"Invalid product title: {product_title}")
            return jsonify({"status": "error", "message": "Invalid product title"}), 400
        
        success = distribute_chips(username, chips)
        if success:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to distribute chips"}), 500
        
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return jsonify({"status": "error", "message": f"Missing key: {e}"}), 400
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000)