# BSD 3-Clause License

# Copyright (c) 2024, MoezDawood

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#streamlitwgstest57.py

import streamlit as st
import paramiko
import pandas as pd
from datetime import datetime
import re
import time
import os
import base64

# Set page configuration to wide mode
st.set_page_config(layout="wide")

# Function to establish SSH connection and list files in the directory
def list_csv_files_in_directory(host, username, password, directory):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(f"ls {directory}")
        files = stdout.read().decode().splitlines()

        client.close()
        # Filter files to only include those ending in .csv
        csv_files = [file for file in files if file.endswith('.csv')]
        return csv_files
    except Exception as e:
        st.error(f"Failed to connect or list files: {e}")
        return None

# Function to generate shell-compatible filter expression
def generate_shell_filter_expression(fields):
    expressions = []
    for field in fields:
        if field['field']:
            if field['operator'] in ['greater than', 'less than', 'equal to']:
                op = {'greater than': '>', 'less than': '<', 'equal to': '==' }[field['operator']]
                expressions.append(f"(${field['field']} {op} {field['value']})")
            elif field['operator'] in ['contains', 'does not contain']:
                if field['operator'] == 'contains':
                    expressions.append(f"(${field['field']}.str.contains('{field['value']}'))")
                else:
                    expressions.append(f"(~${field['field']}.str.contains('{field['value']}'))")
    return " & ".join(expressions)

# Function to execute a command with progress bar
def execute_command_with_progress(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    progress = st.progress(0)
    while not stdout.channel.exit_status_ready():
        time.sleep(0.1)
        progress.progress(50)  # Update progress bar to 50% while the command is running
    progress.progress(100)  # Update progress bar to 100% when the command is finished
    return stdout, stderr

def validate_input(value, expected_type):
    if expected_type == 'int':
        try:
            int(value)
            return True
        except ValueError:
            return False
    elif expected_type == 'float':
        try:
            float(value)
            return True
        except ValueError:
            return False
    elif expected_type == 'str':
        return isinstance(value, str)
    return False

def download_file(ssh_client, remote_path, local_path):
    try:
        sftp = ssh_client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        return True
    except Exception as e:
        st.error(f"Failed to download file: {e}")
        return False

def serve_file_for_download(local_path):
    """Serve the file for automatic download."""
    with open(local_path, 'rb') as f:
        data = f.read()
        b64 = base64.b64encode(data).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(local_path)}">Download ZIP file</a>'
        st.markdown(href, unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("SLICER")
    st.write("Written by Moez Dawood (mdawood@bcm.edu)")
    st.write("Access requires you to be on BCM WiFi or BCM VPN")
    st.write("The point of this application is to allow analysts to filter and download 'slices' of WGS data. Since the number of variants in a genome (typically greater than 5 million) far exceeds the number of allowable rows (typically 1 million rows) in conventional spreadsheet softwares (eg Excel), this interface allows the user to parse the variants found in a genome down to 20,000 variants or less. Further, to keep this interface quick and efficient, the files available for each genome in the dropdown menu have been filtered to only contain variants found at a population allele frequency of 0.01 or less in gnomAD v3.")
    st.write("How to use the slicer:")
    st.write("1. Using the dropdown menus, filter the chosen file based on available annotations. To learn more about each annotation, please reference the Glossary: https://tinyurl.com/SlicerGlossary")
    st.write("2. Click the Count button. This count tells you how many variants would remain after implementing the set filter criteria. The Filter button will only show up if the count is less than 20,000 variants.")
    st.write("3. If the number of remaining variants exceeds 20,000, you will be prompted to redo the filter criteria.")
    st.write("4. If the number of remaining variants is less than 20,000, a zip file containing a csv file of the remaining variants and a txt file of the filter criteria should be automatically downloaded.")
    st.write("Please note counting and/or filtering may take up to a few minutes especially if the criteria does not filter out many variants.")


    # Load the annotatedcsvheaders CSV file
    csv_headers_df = pd.read_csv("annotatedcsvheaders.csv")

    # Extract fields from the CSV
    csv_fields = csv_headers_df['CSVHeaders'].tolist()
    field_types = dict(zip(csv_headers_df['CSVHeaders'], csv_headers_df['Type']))
    field_descriptions = dict(zip(csv_headers_df['CSVHeaders'], csv_headers_df['BriefDescription']))

    # Default values for host and directory
    host = "10.66.4.211"
    maindirectory = "/storage/lupski/var/log/shiny-server/WGSslicer/final/annotatedwgsmaffilter"
    temp_directory = "/storage/lupski/var/log/shiny-server/WGSslicer/final/temp"
    
    # Session state to keep track of login status and fields
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'fields' not in st.session_state:
        st.session_state.fields = []
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'password' not in st.session_state:
        st.session_state.password = ""
    if 'variant_count' not in st.session_state:
        st.session_state.variant_count = None

    # Login page
    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username and password:
                files = list_csv_files_in_directory(host, username, password, maindirectory)
                if files is not None:
                    st.session_state.logged_in = True
                    st.session_state.files = files
                    st.session_state.username = username
                    st.session_state.password = password
                    st.experimental_rerun()
            else:
                st.error("Please fill in all fields")
    else:
        # Post-login page
        st.success("Login successful!")
        st.write("You are now accessing the WGS Slicer.")

        if 'files' in st.session_state:
            selected_file = st.selectbox(
                "Select CSV file",
                st.session_state.files,
                index=0,
                help="Start typing to search for the intended CSV file",
            )
            if selected_file:
                st.write(f"You selected: {selected_file}")

                # Display fields for filtering
                used_fields = [field_data['field'] for field_data in st.session_state.fields if field_data['field']]

                for i, field_data in enumerate(st.session_state.fields):
                    available_fields = [""] + [field for field in csv_fields if field not in used_fields or field == field_data['field']]
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                    with col1:
                        selected_field = st.selectbox(
                            f"Select field {i+1}",
                            options=available_fields,
                            index=available_fields.index(field_data['field']) if field_data['field'] else 0,
                            help="Select a field from the CSV file",
                            format_func=lambda x: "" if x == "" else f"{x} ({field_descriptions[x]})",
                            key=f"selectbox_{i}"
                        )
                    with col2:
                        if selected_field:
                            field_type = field_types[selected_field]
                            if field_type in ['int', 'float']:
                                value = st.text_input(
                                    f"Enter value for {selected_field} ({field_type})",
                                    value=field_data['value'] if field_data['value'] else "",
                                    key=f"value_input_{i}"
                                )
                                operator = st.selectbox(
                                    f"Select operator for {selected_field}",
                                    options=['greater than', 'less than', 'equal to'],
                                    index=field_data.get('operator_index', 0),
                                    key=f"operator_{i}"
                                )
                                operator_index = ['greater than', 'less than', 'equal to'].index(operator)
                            else:
                                value = st.text_input(
                                    f"Enter value for {selected_field} ({field_type})",
                                    value=field_data['value'] if field_data['value'] else "",
                                    key=f"value_input_{i}"
                                )
                                operator = st.selectbox(
                                    f"Select operator for {selected_field}",
                                    options=['contains', 'does not contain'],
                                    index=field_data.get('operator_index', 0),
                                    key=f"operator_{i}"
                                )
                                operator_index = ['contains', 'does not contain'].index(operator)

                            if value and not validate_input(value, field_type):
                                st.error(f"Invalid value for {field_type}. Please enter a valid {field_type}.")

                            st.session_state.fields[i] = {
                                'field': selected_field, 
                                'value': value, 
                                'operator': operator,
                                'operator_index': operator_index
                            }
                    with col4:
                        if st.button(f"Remove", key=f"remove_{i}"):
                            del st.session_state.fields[i]
                            st.experimental_rerun()

                if st.button("Add Field"):
                    st.session_state.fields.append({'field': "", 'value': "", 'operator': None, 'operator_index': 0})
                    st.experimental_rerun()

                # Count variants based on filters
                if st.button("Count Variants"):
                    try:
                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh_client.connect(host, username=st.session_state.username, password=st.session_state.password)

                        # Build filter expression for server-side processing
                        filter_expression = generate_shell_filter_expression(st.session_state.fields)

                        # Use temp folder to save intermediate results on the server
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"{timestamp}_filtered.csv"
                        output_path = f"{temp_directory}/{output_filename}"

                        # Collect filter inputs to pass as arguments to filter.py, now including the column type from csv_headers_df
                        filter_args = []
                        for field_data in st.session_state.fields:
                            if field_data['field'] and field_data['value']:
                                field_type = field_types[field_data['field']]  # Extract field type from the annotated CSV
                                filter_args.extend([field_data['field'], field_type.lower(), field_data['operator'].replace(' ', '_'), field_data['value']])

                        # Command to run the filter.py script on the server with the collected arguments, now with field type included
                        filter_command = f"python3 /storage/lupski/var/log/shiny-server/WGSslicer/final/filter.py {maindirectory}/{selected_file} {output_path} " + " ".join(filter_args)
                       
                        print(filter_command)
                        
                        # Execute the filter.py script remotely
                        stdout, stderr = execute_command_with_progress(ssh_client, filter_command)                       
                        stdout.channel.recv_exit_status()  # Wait for the command to finish
                        output_raw = stdout.read()
                        
                        output_str = output_raw.decode('utf-8').strip()
                        output = output_str.split("\n")                        

                        csvfile_path = output[0]
                        txtfile_path = output[1]
                        variant_count = int(output[2])
                        
                        # if len(output) < 3:
                        #     print(f"Expected 3 lines of output but received {len(output)}. Output: {output}")
                        # else:
                        #     csvfile_path = output[0]
                        #     txtfile_path = output[1]
                        #     variant_count = int(output[2])
                        #     zipfile_path = output[3]
                        
                        st.session_state.variant_count = variant_count

                        st.write(f"Number of remaining variants: {variant_count}")

                        if variant_count > 20000:
                            st.warning("Redo filtering so that the remaining variant count is 20,000 or less.")
                        else:
                            zipfile_path = output[3]

                            # Automatically trigger download of the zip file if the variant count is less than 20,000
                            st.success(f"Variant count is below 20,000. Downloading ZIP file...")

                            local_zip_path = os.path.join(os.getcwd(), os.path.basename(zipfile_path))

                            if download_file(ssh_client, zipfile_path, local_zip_path):
                                # Serve the file for download
                                serve_file_for_download(local_zip_path)

                        ssh_client.close()

                    except Exception as e:
                        st.error(f"Failed to count variants: {e}")

if __name__ == "__main__":
    main()


