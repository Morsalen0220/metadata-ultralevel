import sys
import os
import subprocess
import fitz

def run_powershell_bypass(cmd):
    """ExecutionPolicy Bypass দিয়ে PowerShell চালানো"""
    full_cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", cmd]
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    return res.stdout.strip(), res.stderr.strip()

def get_source_os_dates(file_path):
    """Source ফাইলের আসল OS Timestamps বের করা"""
    abs_path = os.path.abspath(file_path)
    ps_cmd = (
        f'$item = Get-Item "{abs_path}"; '
        f'Write-Output $item.CreationTime.ToString("yyyy-MM-dd HH:mm:ss"); '
        f'Write-Output $item.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss"); '
        f'Write-Output $item.LastAccessTime.ToString("yyyy-MM-dd HH:mm:ss")'
    )
    stdout, _ = run_powershell_bypass(ps_cmd)
    lines = stdout.splitlines()
    if len(lines) >= 3:
        return lines[0], lines[1], lines[2]
    return None, None, None

def clone_pdf_exact(source_path, target_path):
    src_abs = os.path.abspath(source_path)
    tgt_abs = os.path.abspath(target_path)

    if not os.path.exists(src_abs) or not os.path.exists(tgt_abs):
        print("Error: Source or Target file does not exist!")
        return

    source_bytes = os.path.getsize(src_abs)
    target_dir = os.path.dirname(tgt_abs)
    source_filename = os.path.basename(src_abs)
    temp_path = os.path.join(target_dir, f"temp_cloned_{source_filename}")

    try:
        # ১. Source ফাইলের OS level Creation/Modified time নেওয়া
        c_time, m_time, a_time = get_source_os_dates(src_abs)

        # ২. Source PDF-এর Internal Metadata এবং Raw XMP নেওয়া
        src_doc = fitz.open(src_abs)
        src_metadata = src_doc.metadata
        src_xmp = src_doc.xref_xml_metadata()
        src_doc.close()

        # ৩. Target PDF-এ মেটাডেটা ট্রান্সফার
        tgt_doc = fitz.open(tgt_abs)
        
        # সোর্সে কোনো ফিল্ড না থাকলে বা None হলে জোরপূর্বক খালি স্ট্রিং ("") বসানো হবে
        clean_metadata = {
            "format": tgt_doc.metadata.get("format", ""),
            "title": src_metadata.get("title") or "",
            "author": src_metadata.get("author") or "",
            "subject": src_metadata.get("subject") or "",
            "keywords": src_metadata.get("keywords") or "",
            "creator": src_metadata.get("creator") or "",
            "producer": src_metadata.get("producer") or "",
            "creationDate": src_metadata.get("creationDate") or "",
            "modDate": src_metadata.get("modDate") or "",  # সোর্সে না থাকলে খালি হয়ে যাবে
            "trapped": src_metadata.get("trapped") or ""
        }
        tgt_doc.set_metadata(clean_metadata)

        # XMP Metadata সোর্সে থাকলে কপি করবে, না থাকলে টার্গেট থেকেও ক্লিয়ার করে দেবে
        if src_xmp and src_xmp.strip():
            tgt_doc.set_xml_metadata(src_xmp)
        else:
            tgt_doc.set_xml_metadata("")

        # গার্বেজ ক্লিন ও অপটিমাইজ সেভ
        tgt_doc.save(temp_path, garbage=4, deflate=True)
        tgt_doc.close()

        # ৪. Exact File Size (Bytes) মেলানো
        temp_bytes = os.path.getsize(temp_path)
        
        if temp_bytes < source_bytes:
            padding_needed = source_bytes - temp_bytes
            with open(temp_path, "ab") as f:
                # PDF Comment Padding
                f.write(b"\n%" + b"0" * (padding_needed - 2))
        elif temp_bytes > source_bytes:
            print(f"[Warning] Target PDF content is naturally larger ({temp_bytes} B) than Source ({source_bytes} B). Could not shrink content without corrupting PDF.")

        # ৫. ফাইল রিপ্লেস
        if os.path.exists(temp_path):
            os.replace(temp_path, tgt_abs)

        # ৬. Windows OS Timestamps (Created Date, Modified Date) জোরপূর্বক বসানো
        if c_time and m_time and a_time:
            ps_timestamps = (
                f'$tgt = Get-Item "{tgt_abs}"; '
                f'$tgt.CreationTime = "{c_time}"; '
                f'$tgt.LastWriteTime = "{m_time}"; '
                f'$tgt.LastAccessTime = "{a_time}";'
            )
            run_powershell_bypass(ps_timestamps)

        print(f"[Success] Processed: '{os.path.basename(tgt_abs)}'")
        print(f" -> Source Size: {source_bytes} bytes | Output Size: {os.path.getsize(tgt_abs)} bytes")
        print(f" -> Created Date: {c_time}")
        print(f" -> Modified Date: {m_time}")

    except Exception as e:
        print(f"[Error] Failed: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clone_advanced_pdf_attributes.py <source.pdf> <target.pdf>")
    else:
        clone_pdf_exact(sys.argv[1], sys.argv[2])