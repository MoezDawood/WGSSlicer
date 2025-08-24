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

#streamlitwgstest60.py

import streamlit as st
import paramiko
import pandas as pd
from datetime import datetime
import re
import time
import os
import base64
import zipfile
import json
import glob

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
            if field['field'].lower() == 'hugo' and field.get('is_multi_value', False):
                # Handle multi-value hugo field with OR logic
                gene_names = field.get('gene_list', [])
                if gene_names:
                    gene_expressions = []
                    for gene in gene_names:
                        gene = gene.strip()
                        if gene:
                            gene_expressions.append(f"(${field['field']}.str.contains('{gene}'))")
                    if gene_expressions:
                        expressions.append(f"({' | '.join(gene_expressions)})")
            elif field['operator'] in ['greater than', 'less than', 'equal to']:
                op = {'greater than': '>', 'less than': '<', 'equal to': '==' }[field['operator']]
                expressions.append(f"(${field['field']} {op} {field['value']})")
            elif field['operator'] in ['contains', 'does not contain']:
                if field['operator'] == 'contains':
                    expressions.append(f"(${field['field']}.str.contains('{field['value']}'))")
                else:
                    expressions.append(f"(~${field['field']}.str.contains('{field['value']}'))")
    return " & ".join(expressions)

# Function to execute a command with progress bar
def execute_command_with_progress(ssh_client, command, progress_container=None):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    if progress_container:
        progress = progress_container.progress(0)
        while not stdout.channel.exit_status_ready():
            time.sleep(0.1)
            progress.progress(50)  # Update progress bar to 50% while the command is running
        progress.progress(100)  # Update progress bar to 100% when the command is finished
    else:
        while not stdout.channel.exit_status_ready():
            time.sleep(0.1)
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

def serve_file_for_download(local_path, label="Download ZIP file"):
    """Serve the file for automatic download."""
    with open(local_path, 'rb') as f:
        data = f.read()
        b64 = base64.b64encode(data).decode('utf-8')
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(local_path)}">{label}</a>'
        st.markdown(href, unsafe_allow_html=True)

def create_combined_zip(file_paths, zip_name):
    """Create a combined ZIP file from multiple individual ZIP files."""
    with zipfile.ZipFile(zip_name, 'w') as combined_zip:
        for file_path in file_paths:
            if os.path.exists(file_path):
                combined_zip.write(file_path, os.path.basename(file_path))
    return zip_name

def save_filter_set(filter_name, fields):
    """Save current filter configuration to a JSON file."""
    try:
        # Get the current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = f"SavedSlicerFilterSet_{filter_name}.json"
        filepath = os.path.join(script_dir, filename)
        
        # Prepare filter data
        filter_data = {
            'filter_name': filter_name,
            'created_date': datetime.now().isoformat(),
            'fields': fields
        }
        
        # Save to JSON file
        with open(filepath, 'w') as f:
            json.dump(filter_data, f, indent=2)
        
        return True, filepath
    except Exception as e:
        return False, str(e)

def load_saved_filter_sets():
    """Load all saved filter sets from the script directory."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        pattern = os.path.join(script_dir, "SavedSlicerFilterSet_*.json")
        filter_files = glob.glob(pattern)
        
        saved_filters = {}
        for file_path in filter_files:
            try:
                with open(file_path, 'r') as f:
                    filter_data = json.load(f)
                    filter_name = filter_data.get('filter_name', os.path.basename(file_path))
                    saved_filters[filter_name] = filter_data
            except Exception as e:
                st.warning(f"Could not load filter file {os.path.basename(file_path)}: {e}")
        
        return saved_filters
    except Exception as e:
        st.error(f"Error loading saved filters: {e}")
        return {}

def load_filter_set(filter_data):
    """Load a filter set into session state."""
    if 'fields' in filter_data:
        st.session_state.fields = filter_data['fields']
        return True
    return False

def parse_gene_list(gene_input):
    """Parse gene names from various input formats."""
    if not gene_input:
        return []
    
    # Split by common delimiters and clean up
    genes = re.split(r'[,;\n\r\t]+', gene_input)
    cleaned_genes = []
    
    for gene in genes:
        gene = gene.strip()
        if gene:
            cleaned_genes.append(gene)
    
    return cleaned_genes

def format_gene_list_for_display(gene_list):
    """Format gene list for display in UI."""
    if not gene_list:
        return ""
    return ", ".join(gene_list)

# Streamlit app
def main():
    st.title("SLICER v60 - Multi-Gene Search Enhancement")
    st.write("Written by Moez Dawood (mdawood@bcm.edu)")
    st.write("Access requires you to be on BCM WiFi or BCM VPN")
    st.write("The point of this application is to allow analysts to filter and download 'slices' of WGS data. Since the number of variants in a genome (typically greater than 5 million) far exceeds the number of allowable rows (typically 1 million rows) in conventional spreadsheet softwares (eg Excel), this interface allows the user to parse the variants found in a genome down to 50,000 variants or less. Further, to keep this interface quick and efficient, the files available for each genome in the dropdown menu have been filtered to only contain variants found at a population allele frequency of 0.01 or less in gnomAD v3.")
    st.write("How to use the slicer:")
    st.write("1. Using the multi-select dropdown, choose multiple CSV files to process with the same filter criteria.")
    st.write("2. Optionally load a saved filter set, or create new filter criteria using the dropdown menus based on available annotations. To learn more about each annotation, please reference the Glossary: https://tinyurl.com/SlicerGlossary")
    st.write("3. **NEW:** For the 'hugo' field (gene names), you can now enter multiple gene names separated by commas, semicolons, or new lines. The filter will match rows containing ANY of the specified genes.")
    st.write("4. Save your filter criteria for future use with the 'Save Filters' button.")
    st.write("5. Click the Count button. This will process each selected file individually and show you how many variants would remain after implementing the set filter criteria for each file.")
    st.write("6. The Filter button will only show up if ALL selected files have variant counts less than 50,000.")
    st.write("7. If any file has more than 50,000 remaining variants, you will be prompted to redo the filter criteria.")
    st.write("8. If all files have less than 50,000 remaining variants, individual ZIP files for each processed file will be available for download, plus a combined ZIP file containing all results.")
    st.write("Please note counting and/or filtering may take up to a few minutes especially if the criteria does not filter out many variants.")

    # Load the annotatedcsvheaders CSV file
    try:
        csv_headers_df = pd.read_csv("annotatedcsvheaders.csv")
        # Extract fields from the CSV
        csv_fields = csv_headers_df['CSVHeaders'].tolist()
        field_types = dict(zip(csv_headers_df['CSVHeaders'], csv_headers_df['Type']))
        field_descriptions = dict(zip(csv_headers_df['CSVHeaders'], csv_headers_df['BriefDescription']))
    except FileNotFoundError:
        st.error("annotatedcsvheaders.csv file not found. Please ensure it's in the same directory as this script.")
        st.stop()

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
    if 'file_results' not in st.session_state:
        st.session_state.file_results = {}
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'show_save_dialog' not in st.session_state:
        st.session_state.show_save_dialog = False

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
                    st.rerun()
            else:
                st.error("Please fill in all fields")
    else:
        # Post-login page
        st.success("Login successful!")
        st.write("You are now accessing the WGS Slicer.")

        if 'files' in st.session_state:
            # Multi-select for CSV files
            selected_files = st.multiselect(
                "Select CSV files to process (you can select multiple files)",
                st.session_state.files,
                help="Start typing to search for files. All selected files will be processed with the same filter criteria.",
            )
            
            if selected_files:
                st.write(f"You selected {len(selected_files)} file(s):")
                for file in selected_files:
                    st.write(f"• {file}")

                # Load saved filter sets section
                st.subheader("🔄 Load Saved Filter Set (Optional)")
                saved_filters = load_saved_filter_sets()
                
                if saved_filters:
                    filter_options = [""] + list(saved_filters.keys())
                    selected_filter = st.selectbox(
                        "Choose a saved filter set to load:",
                        options=filter_options,
                        help="Select a previously saved filter configuration to automatically populate the fields below."
                    )
                    
                    if selected_filter:
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if st.button("Load Selected Filter Set"):
                                if load_filter_set(saved_filters[selected_filter]):
                                    st.success(f"✅ Loaded filter set: {selected_filter}")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to load filter set")
                        
                        with col2:
                            if selected_filter in saved_filters:
                                filter_info = saved_filters[selected_filter]
                                st.info(f"📅 Created: {filter_info.get('created_date', 'Unknown')}")
                                st.info(f"🔧 Contains {len(filter_info.get('fields', []))} filter criteria")
                else:
                    st.info("No saved filter sets found. Create and save filter criteria below to reuse them later.")

                # Display fields for filtering
                used_fields = [field_data['field'] for field_data in st.session_state.fields if field_data['field']]

                st.subheader("🔍 Filter Criteria (will be applied to all selected files)")
                
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
                            
                            # Special handling for 'hugo' field
                            if selected_field.lower() == 'hugo':
                                st.write("🧬 **Multi-Gene Search**")
                                gene_input = st.text_area(
                                    f"Enter gene names (one per line or separated by commas/semicolons):",
                                    value=format_gene_list_for_display(field_data.get('gene_list', [])),
                                    height=100,
                                    key=f"hugo_input_{i}",
                                    help="Enter multiple gene names like: BRCA1, BRCA2, TP53 or one per line"
                                )
                                
                                gene_list = parse_gene_list(gene_input)
                                
                                if gene_list:
                                    st.write(f"**Genes to search:** {', '.join(gene_list[:5])}{'...' if len(gene_list) > 5 else ''}")
                                    st.write(f"**Total genes:** {len(gene_list)}")
                                
                                # Store multi-value hugo data
                                st.session_state.fields[i] = {
                                    'field': selected_field,
                                    'value': gene_input,  # Store original input
                                    'gene_list': gene_list,  # Store parsed list
                                    'is_multi_value': True,
                                    'operator': 'multi_contains',
                                    'operator_index': 0
                                }
                                
                            elif field_type in ['int', 'float']:
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
                                
                                if value and not validate_input(value, field_type):
                                    st.error(f"Invalid value for {field_type}. Please enter a valid {field_type}.")

                                st.session_state.fields[i] = {
                                    'field': selected_field, 
                                    'value': value, 
                                    'operator': operator,
                                    'operator_index': operator_index,
                                    'is_multi_value': False
                                }
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
                                    'operator_index': operator_index,
                                    'is_multi_value': False
                                }
                    with col4:
                        if st.button(f"Remove", key=f"remove_{i}"):
                            del st.session_state.fields[i]
                            st.rerun()

                # Filter management buttons
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Add Field"):
                        st.session_state.fields.append({'field': "", 'value': "", 'operator': None, 'operator_index': 0, 'is_multi_value': False})
                        st.rerun()
                
                with col2:
                    # Only show Save Filters button if there are active filters
                    active_filters = [f for f in st.session_state.fields if f.get('field') and (f.get('value') or f.get('gene_list'))]
                    if active_filters and st.button("💾 Save Filters"):
                        st.session_state.show_save_dialog = True
                        st.rerun()

                # Save filter dialog
                if st.session_state.show_save_dialog:
                    with st.expander("💾 Save Current Filter Set", expanded=True):
                        filter_name = st.text_input(
                            "Enter a name for this filter set:",
                            placeholder="e.g., BRCA_Panel_Genes",
                            help="This name will be used to identify and load this filter set later."
                        )
                        
                        col1, col2, col3 = st.columns([1, 1, 2])
                        with col1:
                            if st.button("Save") and filter_name:
                                # Validate filter name
                                if re.match(r'^[a-zA-Z0-9_-]+$', filter_name):
                                    success, result = save_filter_set(filter_name, st.session_state.fields)
                                    if success:
                                        st.success(f"✅ Filter set '{filter_name}' saved successfully!")
                                        st.session_state.show_save_dialog = False
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Failed to save filter set: {result}")
                                else:
                                    st.error("❌ Filter name can only contain letters, numbers, hyphens, and underscores.")
                        
                        with col2:
                            if st.button("Cancel"):
                                st.session_state.show_save_dialog = False
                                st.rerun()

                # Count variants based on filters for all selected files
                if st.button("🔢 Count Variants for All Selected Files"):
                    st.session_state.file_results = {}
                    st.session_state.processing_complete = False
                    
                    try:
                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh_client.connect(host, username=st.session_state.username, password=st.session_state.password)

                        # Build filter expression for server-side processing
                        filter_expression = generate_shell_filter_expression(st.session_state.fields)

                        # Collect filter inputs to pass as arguments to filter.py
                        filter_args = []
                        for field_data in st.session_state.fields:
                            if field_data['field']:
                                if field_data.get('is_multi_value', False) and field_data['field'].lower() == 'hugo':
                                    # Handle multi-value hugo field
                                    gene_list = field_data.get('gene_list', [])
                                    if gene_list:
                                        field_type = field_types[field_data['field']]
                                        # Pass multiple genes as a pipe-separated string
                                        gene_string = '|'.join(gene_list)
                                        filter_args.extend([field_data['field'], field_type.lower(), 'multi_contains', gene_string])
                                elif field_data.get('value'):
                                    field_type = field_types[field_data['field']]
                                    filter_args.extend([field_data['field'], field_type.lower(), field_data['operator'].replace(' ', '_'), field_data['value']])

                        st.write(f"Processing {len(selected_files)} files with the same filter criteria...")
                        
                        # Process each file individually
                        for idx, selected_file in enumerate(selected_files):
                            st.write(f"Processing file {idx + 1} of {len(selected_files)}: {selected_file}")
                            
                            # Create progress container for this file
                            progress_container = st.container()
                            
                            # Use temp folder to save intermediate results on the server
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_filename = f"{timestamp}_{selected_file.replace('.csv', '')}_filtered.csv"
                            output_path = f"{temp_directory}/{output_filename}"

                            # Command to run the filter.py script on the server
                            # Properly escape arguments that might contain special characters
                            escaped_args = []
                            for arg in filter_args:
                                if '|' in str(arg) or ' ' in str(arg):
                                    escaped_args.append(f"'{arg}'")
                                else:
                                    escaped_args.append(str(arg))
                            filter_command = f"python3 /storage/lupski/var/log/shiny-server/WGSslicer/final/filter.py {maindirectory}/{selected_file} {output_path} " + " ".join(escaped_args)
                           
                            # Execute the filter.py script remotely
                            stdout, stderr = execute_command_with_progress(ssh_client, filter_command, progress_container)
                            stdout.channel.recv_exit_status()  # Wait for the command to finish
                            output_raw = stdout.read()
                            
                            output_str = output_raw.decode('utf-8').strip()
                            output = output_str.split("\n")

                            if len(output) >= 3:
                                csvfile_path = output[0]
                                txtfile_path = output[1]
                                variant_count = int(output[2])
                                
                                # Store results for this file
                                result = {
                                    'csvfile_path': csvfile_path,
                                    'txtfile_path': txtfile_path,
                                    'variant_count': variant_count,
                                    'status': 'success'
                                }
                                
                                if len(output) >= 4:
                                    result['zipfile_path'] = output[3]
                                
                                st.session_state.file_results[selected_file] = result
                                st.write(f"✅ {selected_file}: {variant_count} variants remaining")
                            else:
                                st.session_state.file_results[selected_file] = {
                                    'status': 'error',
                                    'error': 'Unexpected output from filter script'
                                }
                                st.write(f"❌ {selected_file}: Error processing file")

                        st.session_state.processing_complete = True
                        ssh_client.close()

                    except Exception as e:
                        st.error(f"Failed to process files: {e}")

                # Display results if processing is complete
                if st.session_state.processing_complete and st.session_state.file_results:
                    st.subheader("📊 Processing Results")
                    
                    all_under_limit = True
                    successful_files = []
                    
                    for file_name, result in st.session_state.file_results.items():
                        if result['status'] == 'success':
                            variant_count = result['variant_count']
                            if variant_count > 50000:
                                st.warning(f"🔴 {file_name}: {variant_count} variants (exceeds 50,000 limit)")
                                all_under_limit = False
                            else:
                                st.success(f"🟢 {file_name}: {variant_count} variants (within limit)")
                                successful_files.append(file_name)
                        else:
                            st.error(f"❌ {file_name}: Processing failed")
                            all_under_limit = False

                    if not all_under_limit:
                        st.warning("⚠️ Some files exceed the 50,000 variant limit. Please adjust your filter criteria.")
                    else:
                        st.success("🎉 All files are within the 50,000 variant limit! Ready for download.")
                        
                        # Download section
                        if successful_files:
                            st.subheader("📥 Download Results")
                            
                            try:
                                ssh_client = paramiko.SSHClient()
                                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                ssh_client.connect(host, username=st.session_state.username, password=st.session_state.password)
                                
                                downloaded_files = []
                                
                                # Download individual files
                                for file_name in successful_files:
                                    result = st.session_state.file_results[file_name]
                                    if 'zipfile_path' in result:
                                        zipfile_path = result['zipfile_path']
                                        local_zip_path = os.path.join(os.getcwd(), f"{file_name.replace('.csv', '')}_filtered.zip")
                                        
                                        if download_file(ssh_client, zipfile_path, local_zip_path):
                                            downloaded_files.append(local_zip_path)
                                            st.write(f"📥 Individual download for {file_name}:")
                                            serve_file_for_download(local_zip_path, f"Download {file_name.replace('.csv', '')}_filtered.zip")
                                
                                # Create combined ZIP file
                                if len(downloaded_files) > 1:
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    combined_zip_name = f"combined_results_{timestamp}.zip"
                                    combined_zip_path = os.path.join(os.getcwd(), combined_zip_name)
                                    
                                    create_combined_zip(downloaded_files, combined_zip_path)
                                    st.write("📦 Combined download (all results):")
                                    serve_file_for_download(combined_zip_path, f"Download {combined_zip_name}")
                                
                                ssh_client.close()
                                
                            except Exception as e:
                                st.error(f"Failed to download files: {e}")

if __name__ == "__main__":
    main()
