# Slicer
Written by Moez Dawood (mdawood@bcm.edu)

Access requires you to be on BCM WiFi or BCM VPN

## Purpose
The point of this application is to allow analysts to filter and download 'slices' of WGS data. Since the number of variants in a genome (typically greater than 5 million) far exceeds the number of allowable rows (typically 1 million rows) in conventional spreadsheet softwares (eg Excel), this interface allows the user to parse the variants found in a genome down to 50,000 variants or less. Further, to keep this interface quick and efficient, the files available for each genome in the dropdown menu have been filtered to only contain variants found at a population allele frequency of 0.01 or less in gnomAD v3.

How to use the slicer:

1. Using the dropdown menus, filter the chosen file based on available annotations. To learn more about each annotation, please reference the Glossary: https://tinyurl.com/SlicerGlossary

2. Click the Count button. This count tells you how many variants would remain after implementing the set filter criteria. The Filter button will only show up if the count is less than 50,000 variants.

3. If the number of remaining variants exceeds 50,000, you will be prompted to redo the filter criteria.

4. If the number of remaining variants is less than 50,000, a zip file containing a csv file of the remaining variants and a txt file of the filter criteria should be automatically downloaded.

Please note counting and/or filtering may take up to a few minutes especially if the criteria does not filter out many variants.


## Python 

Before beginning, Python must be installed on your system. You can check if Python 3 is installed by running the following command in your terminal or command prompt:
```
python3 --version
```
If Python 3 is not installed, you can download and install it from the oficial Python website (https://www.python.org/downloads/).


## Installation Instructions

### Step 1: Clone the Repository
To begin, clone the WGSSlicer repository using the following command:
```
git clone https://github.com/MoezDawood/WGSSlicer.git
```

### Step 2: Navigate to the project directory
Once the repository is cloned, move into the project directory:
```
cd WGSSlicer  
```

### Step 3: Install required dependencies
Once inside the project directory, install the required dependencies using the requirements.txt file:
```
pip install -r requirements.txt
```

### Step 4: Run the application
Now that the dependencies are installed, you can run the WGSSlicer script using Streamlit:
```
streamlit run WGS_Slicer_v1.py
```
