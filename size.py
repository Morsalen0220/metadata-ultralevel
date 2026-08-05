import os
import sys

def pad_pdf_to_exact_size(pdf_path, target_kb=66):
    """
    মেটাডেটা বা মডিফাই ডেট পরিবর্তন না করে শুধুমাত্র বাইনারি কমেন্ট প্যাডিং 
    যুক্ত করে সব PDF-কে হুবহু একটি নির্দিষ্ট সাইজে (যেমন: ৬৬ KB) নিয়ে আসবে।
    """
    target_bytes = int(target_kb * 1024)

    if not os.path.exists(pdf_path):
        return

    file_name = os.path.basename(pdf_path)
    current_bytes = os.path.getsize(pdf_path)

    # ১. যদি ফাইলের বর্তমান সাইজ টার্গেট সাইজের চেয়ে বড় হয়
    if current_bytes > target_bytes:
        print(f"[Warning] '{file_name}' ({current_bytes/1024:.2f} KB) is larger than target {target_kb} KB. Skipped (to avoid modifying metadata).")
        return

    # ২. যদি ফাইলের সাইজ ইতিমধ্যেই সমান হয়
    if current_bytes == target_bytes:
        print(f"[Skipped] '{file_name}' is already exactly {target_kb} KB.")
        return

    # ৩. ফাইলের শেষে নিরাপদ বাইনারি কমেন্ট প্যাডিং যুক্ত করা (মেটাডেটা অপরিবর্তিত থাকবে)
    try:
        padding_needed = target_bytes - current_bytes
        
        # %PADDING_ লেখার জন্য ৯ বাইট প্রয়োজন
        if padding_needed < 10:
            padding_data = b"\n%" + b"X" * (padding_needed - 2)
        else:
            padding_data = b"\n%PADDING_" + b"X" * (padding_needed - 11)

        with open(pdf_path, "ab") as f:
            f.write(padding_data)

        final_size = os.path.getsize(pdf_path) / 1024
        print(f"[Success] '{file_name}' adjusted to exactly {final_size:.2f} KB.")

    except Exception as e:
        print(f"[Error] Failed processing '{file_name}': {e}")


def process_folder(folder_path, target_kb=66):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist!")
        return

    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return

    print(f"Found {len(pdf_files)} PDF file(s). Target size: {target_kb} KB.\n")
    for file_name in pdf_files:
        full_path = os.path.join(folder_path, file_name)
        pad_pdf_to_exact_size(full_path, target_kb)


if __name__ == "__main__":
    # ব্যবহার: python script.py [ফোল্ডার_পাথ] [টার্গেট_সাইজ_KB]
    target_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # আপনি চাইলে টার্গেট সাইজ পরিবর্তন করতে পারেন (যেমন: 66)
    target_size_kb = float(sys.argv[2]) if len(sys.argv) > 2 else 66.0

    process_folder(target_folder, target_size_kb)