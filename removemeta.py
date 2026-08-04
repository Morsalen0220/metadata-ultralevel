import sys
import os
import fitz

def remove_metadata_from_file(pdf_path):
    if not os.path.exists(pdf_path):
        return

    file_name = os.path.basename(pdf_path)
    temp_path = os.path.join(os.path.dirname(pdf_path), f"temp_{file_name}")

    try:
        doc = fitz.open(pdf_path)

        # সব মেটাডেটা ফিল্ড খালি করে দেওয়া
        metadata = {
            "format": doc.metadata.get("format", ""),
            "title": "",
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "",
            "producer": "",
            "creationDate": "",
            "modDate": "",
            "trapped": ""
        }
        doc.set_metadata(metadata)

        # গার্বেজ কালেকশন ও স্ট্রিপসহ ক্লিন সেভ
        doc.save(temp_path, garbage=4, deflate=True)
        doc.close()

        # মূল ফাইলে ওভাররাইট
        os.replace(temp_path, pdf_path)
        print(f"[Success] Metadata cleared: '{file_name}'")

    except Exception as e:
        print(f"[Error] Failed on '{file_name}': {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def process_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Clearing metadata...\n")
    for file_name in pdf_files:
        full_path = os.path.join(folder_path, file_name)
        remove_metadata_from_file(full_path)

if __name__ == "__main__":
    # কমান্ড লাইনে ফোল্ডার দিলে সেটা নেবে, না দিলে বর্তমান ফোল্ডার প্রসেস করবে
    target_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    process_folder(target_folder)