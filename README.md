# AutoChip

This project is an automation tool built using Python, Flask, and PyAutoGUI. It was created as a fun project to automate the distribution of virtual chips when a purchase is made on Sellix.

## Project Overview

The AutoChip project automates the process of distributing virtual chips to users. It leverages webhooks from Sellix, a Python Flask server, and PyAutoGUI for GUI automation. The tool uses image recognition to click the buttons in the correct order to distribute chips when someone buys chips from your Sellix store.

## Features

- **Automated Chip Distribution**: Automatically distributes chips based on purchases made on Sellix.
- **Webhooks Integration**: Listens to Sellix webhooks to trigger the automation.
- **GUI Automation**: Uses PyAutoGUI to interact with the ClubGG application.
- **Image Recognition**: Clicks buttons in the correct order using image recognition to ensure accurate chip distribution.

## Video Demonstration

You can watch a video demonstration of the project [here](https://youtu.be/bpaSTHyfeMo).

## Instructions

1. **Setup Python Environment**:
    - Ensure you have Python installed on your system.
    - Install the required packages:
        ```sh
        pip install pyautogui pywinauto flask
        ```

2. **Configure Logging**:
    - The script uses Python's logging module for logging information.

3. **Run the Flask Server**:
    - Save the provided Python script as `app.py`.
    - Run the Flask server:
        ```sh
        python app.py
        ```

4. **Setup Ngrok**:
    - Download and install [Ngrok](https://ngrok.com/).
    - Run Ngrok to tunnel the Flask server:
        ```sh
        ngrok http 5000
        ```
    - Copy the Ngrok URL provided (e.g., `http://your-ngrok-url.ngrok.io`).

5. **Webhook Configuration**:
    - In your Sellix account, set up a webhook to point to your Ngrok URL (e.g., `http://your-ngrok-url.ngrok.io/webhook`).

6. **Distributing Chips**:
    - When a purchase is made on Sellix, the webhook will trigger the automation script.
    - The script will locate and interact with the ClubGG application using image recognition to distribute the specified amount of chips.

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request.
