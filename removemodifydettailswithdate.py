#!/usr/bin/env python3
import os, sys, datetime, time, warnings, ctypes
from ctypes import wintypes, byref, WinError
from pikepdf import Pdf
warnings.filterwarnings("ignore")

def set_creation_time_win(filepath, timestamp):
    try:
        handle = ctypes.windll.kernel32.CreateFileW(
            filepath, 0x40000000, 0x00000001 | 0x00000002, None, 3, 0, None
        )
        if handle == -1: return False
        epoch_diff = 11644473600
        ft = int((timestamp + epoch_diff) * 10000000)
        class FILETIME(ctypes.Structure):
            _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]
        filetime = FILETIME(ft & 0xFFFFFFFF, ft >> 32)
        res = ctypes.windll.kernel32.SetFileTime(handle, byref(filetime), None, None)
        ctypes.windll.kernel32.CloseHandle(handle)
        return res != 0
    except: return False

def process_pdf(pdf_path, custom_date):
    pdf_date_str = custom_date.strftime("D:%Y%m%d%H%M%S+00'00'")
    iso_str = custom_date.isoformat(timespec='microseconds') + 'Z'

    try:
        pdf = Pdf.open(pdf_path, allow_overwriting_input=True)
        pdf.docinfo['/CreationDate'] = pdf_date_str
        if '/ModDate' in pdf.docinfo: del pdf.docinfo['/ModDate']

        try:
            meta = pdf.open_metadata(set_pikepdf_as_editor=False)
            meta['xmp:CreateDate'] = iso_str
            if 'xmp:ModifyDate' in meta: del meta['xmp:ModifyDate']
            if 'xmp:MetadataDate' in meta: del meta['xmp:MetadataDate']
            meta.write()
        except: pass

        pdf.save(pdf_path, compress_streams=True, stream_decode_level=0)
        pdf.close()

        if os.name == 'nt':
            time.sleep(0.05)
            set_creation_time_win(pdf_path, custom_date.timestamp())

        print(f"✅ Updated: {pdf_path}")
    except Exception as e:
        print(f"❌ Error ({pdf_path}): {e}")

if __name__ == "__main__":
    # ১. তারিখ পার্স করা (যদি কমান্ডে তারিখ দেওয়া থাকে, না দিলে বর্তমান সময়)
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        custom_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc)
    else:
        custom_date = datetime.datetime.now(datetime.timezone.utc)

    # ২. বর্তমান ফোল্ডারের সব PDF খোঁজা ও আপডেট করা
    pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("⚠️ Current folder does not contain any PDF files.")
    else:
        print(f"📁 Processing {len(pdf_files)} PDF(s) with date: {custom_date}\n")
        for pdf in pdf_files:
            process_pdf(pdf, custom_date)
        print("\n🎉 All PDFs updated successfully!")
