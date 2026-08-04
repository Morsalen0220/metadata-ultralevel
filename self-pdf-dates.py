import sys
import os
import time
from datetime import datetime
import fitz

def set_custom_dates(pdf_path, target_date_str):
    """
    target_date_str Format: "YYYY-MM-DD HH:MM:SS"
    Example: "2024-05-15 10:30:00"
    """
    if not os.path.exists(pdf_path):
        return

    file_name = os.path.basename(pdf_path)
    temp_path = os.path.join(os.path.dirname(pdf_path), f"temp_{file_name}")

    # ১. তারিখের ফরম্যাট পার্স করা
    dt = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")
    
    # PDF Internal Metadata Format: D:YYYYMMDDHHmmSS
    pdf_date_format = dt.strftime("D:%Y%m%d%H%M%S")

    try:
        # ২. PDF Open & Set Internal Metadata
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        
        # নির্দিষ্ট তারিখ সেট করা
        metadata["creationDate"] = pdf_date_format
        metadata["modDate"] = pdf_date_format
        
        doc.set_metadata(metadata)
        doc.save(temp_path, garbage=4, deflate=True)
        doc.close()

        # মূল ফাইলে ওভাররাইট
        os.replace(temp_path, pdf_path)

        # ৩. Windows File System (OS Level) Modified and Access Date পরিবর্তন করা
        mod_time_epoch = time.mktime(dt.timetuple())
        os.utime(pdf_path, (mod_time_epoch, mod_time_epoch))

        print(f"[Success] Dates set to '{target_date_str}' for: '{file_name}'")

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

    print(f"Found {len(pdf_files)} PDF file(s). Setting dates to '{target_date_str}'...\n")
    for file_name in pdf_files:
        full_path = os.path.join(folder_path, file_name)
        set_custom_dates(full_path, target_date_str)

if __name__ == "__main__":
    # ব্যবহার করার নিয়ম: python set_pdf_dates.py "YYYY-MM-DD HH:MM:SS"
    # উদাহরণ: python set_pdf_dates.py "2024-05-15 10:30:00"
    
    if len(sys.argv) < 2:
        print('Usage: python set_pdf_dates.py "YYYY-MM-DD HH:MM:SS"')
        print('Example: python set_pdf_dates.py "2024-05-15 10:30:00"')
    else:
        custom_date = sys.argv[1]
        folder = sys.argv[2] if len(sys.argv) > 2 else "."
        process_folder(folder, custom_date)