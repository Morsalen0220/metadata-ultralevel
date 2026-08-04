import sys
import os
import subprocess
from datetime import datetime
import fitz

def set_windows_file_dates(file_path, dt):
    """
    PowerShell ব্যবহার করে Windows OS level-এর
    CreationTime, LastWriteTime (Modified), এবং LastAccessTime পরিবর্তন করা
    """
    date_str = dt.strftime("%m/%d/%Y %H:%M:%S")
    powershell_cmd = (
        f'$(Get-Item "{file_path}").CreationTime = "{date_str}"; '
        f'$(Get-Item "{file_path}").LastWriteTime = "{date_str}"; '
        f'$(Get-Item "{file_path}").LastAccessTime = "{date_str}"'
    )
    subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True, check=True)

def set_custom_dates(pdf_path, target_date_str):
    """
    target_date_str Format: "YYYY-MM-DD HH:MM:SS"
    Example: "2024-05-15 10:30:00"
    """
    if not os.path.exists(pdf_path):
        return

    abs_pdf_path = os.path.abspath(pdf_path)
    file_name = os.path.basename(abs_pdf_path)
    temp_path = os.path.join(os.path.dirname(abs_pdf_path), f"temp_{file_name}")

    try:
        dt = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")
        pdf_date_format = dt.strftime("D:%Y%m%d%H%M%S")

        # ১. PDF-এর ভেতরের মেটাডেটা আপডেট করা (CreationDate & ModifyDate)
        doc = fitz.open(abs_pdf_path)
        metadata = doc.metadata
        
        metadata["creationDate"] = pdf_date_format
        metadata["modDate"] = pdf_date_format
        
        doc.set_metadata(metadata)
        doc.save(temp_path, garbage=4, deflate=True)
        doc.close()

        # ২. মূল ফাইলটি ওভাররাইট করা
        os.replace(temp_path, abs_pdf_path)

        # ৩. Windows OS-এর Created Date, Modified Date & Access Date একসাথে পরিবর্তন করা
        set_windows_file_dates(abs_pdf_path, dt)

        print(f"[Success] Internal & Windows Created/Modified dates set to '{target_date_str}' for: '{file_name}'")

    except Exception as e:
        print(f"[Error] Failed processing '{file_name}': {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def process_folder(folder_path, target_date_str):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Setting all dates to '{target_date_str}'...\n")
    for file_name in pdf_files:
        full_path = os.path.join(folder_path, file_name)
        set_custom_dates(full_path, target_date_str)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python set_pdf_dates.py "YYYY-MM-DD HH:MM:SS"')
        print('Example: python set_pdf_dates.py "2024-05-15 10:30:00"')
    else:
        custom_date = sys.argv[1]
        folder = sys.argv[2] if len(sys.argv) > 2 else "."
        process_folder(folder, custom_date)
