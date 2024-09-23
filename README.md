# WGSSlicer

WGSSlicer is a tool designed to slice and download excerpts of annotated Whole Genome Sequencing (WGS) files.

## Prerequisites

- Python 3 must be installed on your system.

### Check if Python is installed:

You can check if Python 3 is installed by running the following command in your terminal or command prompt:

```bash
python3 --version
If Python 3 is not installed, you can download and install it from the official Python website.

Installation Instructions
Step 1: Clone the repository
To begin, clone the WGSSlicer repository using the following command:

bash
Copy code
git clone https://github.com/MoezDawood/WGSSlicer.git
Step 2: Navigate to the project directory
Once the repository is cloned, move into the project directory:

bash
Copy code
cd WGSSlicer
Step 3: Create a virtual environment (optional but recommended)
It's a good practice to create a virtual environment to manage dependencies. You can create and activate a virtual environment with the following commands:

bash
Copy code
# Create a virtual environment
python3 -m venv env

# Activate the virtual environment (Linux/Mac)
source env/bin/activate

# Activate the virtual environment (Windows)
.\env\Scripts\activate
Step 4: Install the required dependencies
Once inside the project directory (and optional virtual environment), install the required dependencies using the requirements.txt file:

bash
Copy code
pip install -r requirements.txt
Step 5: Run the application
Now that the dependencies are installed, you can run the WGSSlicer script using Streamlit:

bash
Copy code
streamlit run WGS_Slicer_v1.py
Step 6: Deactivate the virtual environment (if used)
After running the script, you can deactivate the virtual environment with the following command:

bash
Copy code
deactivate
Usage
WGSSlicer allows you to select and download specific portions of annotated WGS files for further analysis. After running the application, you can interact with the interface via a web browser and choose which sections of your WGS file to slice and download.
