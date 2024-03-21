# Dash Formula 1 Companion

This repository contains a Dash application for tracking live Formula 1 data. With this app, users can visualize live F1 data including positions, track layout, pace, and laps.

## Setup

### Prerequisites

- Python 3 installed on your system. If not installed, download and install Python from python.org.

### Setting Up Python Virtual Environment

To keep dependencies isolated, it's recommended to use a Python virtual environment. Follow these steps to set up the virtual environment:

1. Clone this repository to your local machine:

    git clone https://github.com/your-username/dash-formula1-companion.git

2. Navigate to the repository directory:

    cd dash-formula1-companion

3. Create a Python virtual environment named "venv":

    python3 -m venv venv

4. Activate the virtual environment:

    On macOS and Linux:

    source venv/bin/activate

    On Windows:

    venv\Scripts\activate

### Installing Dependencies

Once you've set up the virtual environment, install the required packages using pip:

    pip install -r requirements.txt

This will install all the necessary packages specified in the "requirements.txt" file.

## Running the Application

After setting up the virtual environment and installing dependencies, you can run the Dash application using the following command:

    python main.py

This will start the Dash server, and you should see output indicating that the server is running. By default, the server will be accessible at `http://127.0.0.1:8050/` in your web browser.

To stop the server, press `Ctrl + C` in the terminal.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

