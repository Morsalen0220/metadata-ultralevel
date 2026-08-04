import os
import sys
import fitz

def adjust_pdf_size(pdf_path, min_kb=60, max_kb=67):
    min_bytes = min_kb * 1024
    max_bytes = max_kb * 1024
    target_bytes = 64 * 1024  # ৬০ থেকে ৬৭ KB-এর মাঝামাঝি টার্গেট (৬৪ KB)

    if not os.path.exists(pdf_path):
        return

    current_size = os.path.getsize(pdf_path)

    # যদি সাইজ ইতিমধ্যেই ৬০ থেকে ৬৭ KB-এর মধ্যে থাকে
    if min_bytes <= current_size <= max_bytes:
        print(f"[Skipped] '{os.path.basename(pdf_path)}' is already {current_size/1024:.2f} KB.")
        return

    temp_path = f"temp_{os.path.basename(pdf_path)}"

    try:
        # ১. যদি ফাইল ৬৭ KB-এর চেয়ে বড় হয়, PyMuPDF দিয়ে কম্প্রেস/ক্লিন করার চেষ্টা করা
        if current_size > max_bytes:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            metadata["modDate"] = ""  # ModifyDate ক্লিয়ার রাখা
            doc.set_metadata(metadata)
            doc.save(temp_path, garbage=4, deflate=True)
            doc.close()
        else:
            # যদি ফাইল ৬০ KB-এর ছোট হয়, সাধারণ কপি তৈরি করা
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            metadata["modDate"] = ""
            doc.set_metadata(metadata)
            doc.save(temp_path)
            doc.close()

        temp_size = os.path.getsize(temp_path)

        # ২. যদি সাইজ ৬০ KB (min_bytes)-এর কম হয়, নিরাপদ Binary Padding যুক্ত করা
        if temp_size < min_bytes:
            padding_needed = target_bytes - temp_size
            with open(temp_path, "ab") as f:
                # PDF স্পেসিফিকেশন অনুযায়ী নিরাপদ কমেন্ট প্যাডিং
                f.write(b"\n%PADDING_" + b"X" * (padding_needed - 11))

        # ৩. মূল ফাইলে ওভাররাইট করা
        os.replace(temp_path, pdf_path)
        final_size = os.path.getsize(pdf_path) / 1024
        print(f"[Success] '{os.path.basename(pdf_path)}' adjusted to {final_size:.2f} KB.")

    except Exception as e:
        print(f"[Error] Failed processing '{os.path.basename(pdf_path)}': {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

def process_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Processing...\n")
    for file_name in pdf_files:
        full_path = os.path.join(folder_path, file_name)
        adjust_pdf_size(full_path)

if __name__ == "__main__":
    # বর্তমান ফোল্ডার অথবা কমান্ড লাইনে দেওয়া ফোল্ডার প্রসেস করবে
    target_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    process_folder(target_folder)