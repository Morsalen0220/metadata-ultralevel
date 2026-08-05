#!/usr/bin/env python3
import os
import sys
import ctypes
import pikepdf
from pikepdf import Pdf

def strip_modify_date_completely(pdf_path):
    try:
        # Open PDF
        pdf = Pdf.open(pdf_path, allow_overwriting_input=True)

        # 1. Remove ModDate from Document Info Dictionary
        if '/ModDate' in pdf.docinfo:
            del pdf.docinfo['/ModDate']

        # Low-level check: Delete /ModDate key directly from Trailer Info dictionary if exists
        try:
            if '/Info' in pdf.trailer and '/ModDate' in pdf.trailer['/Info']:
                del pdf.trailer['/Info']['/ModDate']
        except Exception:
            pass

        # 2. Remove ModifyDate and MetadataDate from XMP Metadata Stream
        try:
            with pdf.open_metadata(set_pikepdf_as_editor=False) as meta:
                if 'xmp:ModifyDate' in meta:
                    del meta['xmp:ModifyDate']
                if 'xmp:MetadataDate' in meta:
                    del meta['xmp:MetadataDate']
        except Exception:
            pass

        # 3. Save WITHOUT generating a new ModDate
        pdf.save(pdf_path, fix_metadata_version=False)
        pdf.close()

        print(f"🔥 ModDate deleted from internal PDF metadata: {pdf_path}")

    except Exception as e:
        print(f"❌ Error processing {pdf_path}: {e}")

if __name__ == "__main__":
    pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("⚠️ Current folder does not contain any PDF files.")
    else:
        for pdf in pdf_files:
            strip_modify_date_completely(pdf)
        print("\n🎉 ModDate 1000% stripped successfully!")