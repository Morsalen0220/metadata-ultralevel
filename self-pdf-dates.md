
# PDF Custom Date Setter (Internal Metadata & Windows Timestamps)

এই স্ক্রিপ্টটি কোনো নির্দেশিত তারিখ (`YYYY-MM-DD HH:MM:SS`) অনুযায়ী নির্দিষ্ট ফোল্ডারের সমস্ত PDF ফাইলের অভ্যন্তরীণ মেটাডেটা (CreationDate ও ModDate) এবং Windows OS Level-এর টাইমেস্ট্যাম্প (Created, Modified, and Accessed Date) একই সময়ে পরিবর্তন করে দেয়[cite: 3]।



## 🚀 কীভাবে ব্যবহার করবেন (Usage)

### ১. কোথায় ব্যবহার করবেন (Prerequisites)
- **কোথায় রান করবেন:** Windows Command Prompt (CMD) বা PowerShell-এ[cite: 3]।
- **প্রয়োজনীয় ডিপেনডেন্সি:** আপনার সিস্টেমে Python এবং `pymupdf` ইনস্টল থাকতে হবে[cite: 3]।

```cmd
pip install pymupdf

```

### ২. ব্যবহারের команд (Copy-Paste Commands)

#### বর্তমান ফোল্ডারের সব PDF-এ তারিখ সেট করতে:

```cmd
python set_pdf_dates.py "2024-05-15 10:30:00"

```

#### নির্দিষ্ট কোনো ফোল্ডারের সব PDF-এ তারিখ সেট করতে:

```cmd
python set_pdf_dates.py "2024-05-15 10:30:00" "C:\path\to\your\pdf_folder"

```

---

## 🧹 কি কি রিমুভ ও পরিবর্তন হয়? (Changes & Cleaning)

### কি কি রিমুভ/ক্লিন হয়:

* **Old Internal Timestamps:** PDF-এর পুরোনো সৃষ্টির তারিখ (CreationDate) ও মডিফাই তারিখ (ModDate) মুছে নতুন ইনপুট দেওয়া তারিখ বসানো হয়।


* **Unused Garbage Data:** `garbage=4` এবং `deflate=True` ব্যবহারের ফলে মেটাডেটা আপডেটের সময় PDF-এর অভ্যন্তরীণ অতিরিক্ত অপ্রয়োজনীয় ডাটা স্ট্রাকচার ক্লিন হয়ে যায়।



### কি কি পরিবর্তন হয়:

* **PDF Internal Metadata:** `creationDate` এবং `modDate` উভয় ফিল্ডেই আপনার ইনপুট দেওয়া তারিখটি PDF নির্দিষ্ট ফরম্যাটে (`D:YYYYMMDDHHmmss`) সেট হয়ে যায়।


* **Windows File System Dates:** PowerShell ব্যবহারের মাধ্যমে Windows File Explorer Properties-এ দেখানো **Created Date**, **Modified Date**, এবং **Accessed Date** একসাথে পরিবর্তন হয়ে ইনপুট দেওয়া তারিখে রূপ নেয়।


* **Original File Overwrite:** ফাইল প্রসেস করে নিরাপদভাবে মূল ফাইলটির ওপরেই ওভাররাইট (Replace) করা হয়।



---

## 📝 সংক্ষিপ্ত ফিচার তালিকা

| ফিচার | বিবরণ |
| --- | --- |
| **Dual-Level Sync** | PDF মেটাডেটা এবং Windows OS ফাইল তারিখ একসাথে সিঙ্ক করে।

 |
| **Batch Folder Process** | একসাথে ফোল্ডারের সব `.pdf` ফাইলে নির্দিষ্ট তারিখ প্রয়োগ করে।

 |
| **Clean Compression** | ফাইল সেভ করার সময় গার্বেজ ডাটা ক্লিন ও ডিফ্লেট করে।

 |
| **Custom Timestamp** | যেকোনো সাল, তারিখ ও সময় প্রদান করার সুবিধা দেয়।

 |

```

```
