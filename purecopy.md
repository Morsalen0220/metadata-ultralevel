```markdown
# PDF Attributes & Metadata Exact Cloner

এই স্ক্রিপ্টটি একটি সোর্স PDF ফাইলের (`source.pdf`) সমস্ত অভ্যন্তরীণ মেটাডেটা, কাস্টম XMP প্যাকেজ, বাইনারি ফাইল সাইজ এবং Windows ফাইল সিস্টেমের টাইমেস্ট্যাম্প (Created/Modified/Accessed Date) কপি করে অবিকলভাবে একটি টার্গেট PDF ফাইলে (`target.pdf`) ক্লোন করে। সোর্স ফাইলে কোনো মেটাডেটা বা মডিফাই ডেট না থাকলে, টার্গেট ফাইল থেকেও তা সম্পূর্ণ মুছে ফেলে একদম অবিকল অবস্থা তৈরি করে।

---

## 🚀 কীভাবে ব্যবহার করবেন (Usage)

### ১. কোথায় ব্যবহার করবেন (Prerequisites)
- **কোথায় রান করবেন:** Windows Command Prompt (CMD) বা PowerShell (পছন্দনীয়: Run as Administrator)।
- **প্রয়োজনীয় ডিপেনডেন্সি:** আপনার সিস্টেমে Python এবং `pymupdf` ইনস্টল থাকতে হবে[cite: 2]।

```cmd
pip install pymupdf

```

### ২. ব্যবহারের কমান্ড (Copy-Paste Commands)

#### যেকোনো দুই ফাইলে ক্লোন করতে:

```cmd
python clone_advanced_pdf_attributes.py source.pdf target.pdf

```

#### নির্দিষ্ট পাথ/ফোল্ডারের ফাইল ক্লোন করতে:

```cmd
python clone_advanced_pdf_attributes.py "C:\path\to\source.pdf" "C:\path\to\target.pdf"

```

---

## 🧹 কি কি রিমুভ ও পরিবর্তন হয়? (Changes & Cleaning)

### কি কি রিমুভ/ক্লিন হয়:

* **Target's Old Metadata & Revision History:** `garbage=4` প্রয়োগের মাধ্যমে টার্গেট ফাইলের নিজস্ব সমস্ত আগের মেটাডেটা ও হিস্ট্রি সম্পূর্ণ ডিলেট হয়ে যায়।


* **Unused Target Metadata Fields:** সোর্স ফাইলে যে ফিল্ডগুলো (যেমন `modDate`, `creationDate`, `author`, `title` ইত্যাদি) নেই, সেগুলো টার্গেট থেকেও জোরপূর্বক মুছে ফাঁকা (`""`) করে দেওয়া হয়।


* **Mismatched XMP Data:** সোর্স ফাইলে XMP ডাটা না থাকলে টার্গেটের অতিরিক্ত XMP মেটাডেটা সম্পূর্ণ ক্লিয়ার হয়ে যায়।



### কি কি সোর্স থেকে কপি ও সিনক্রোনাইজ হয়:

* **PDF Internal Info Metadata:** Title, Author, Subject, Keywords, Creator, Producer, CreationDate, ModDate।


* **Raw XMP XML Metadata:** সোর্স ফাইলের কাস্টম XMP স্ট্রিম টার্গেটে হুবহু ট্রান্সফার হয়।


* **Exact Byte-Level File Size:** সোর্স ফাইলের সমান সাইজ বানানোর জন্য সেফ PDF কমেন্ট প্যাডিং (`%000...`) যোগ করে হুবহু বাইনারি সাইজ মেলানো হয়।


* **Windows OS Level Timestamps:** PowerShell Execution Policy Bypass এর মাধ্যমে Windows OS-এর Creation Time, Last Write Time (Modified Date), এবং Last Access Time সেকেন্ড পর্যন্ত সোর্সের সাথে এক করে দেওয়া হয়।



---

## 📝 সংক্ষিপ্ত ফিচার তালিকা

| ফিচার | বিবরণ |
| --- | --- |
| **Exact Sync** | সোর্সে যা নেই তা মুছে সোর্সের অবিকল অবস্থায় টার্গেটকে রূপান্তর করে।

 |
| **OS Timestamps Copy** | Windows-এর Created, Modified ও Accessed তারিখ পরিবর্তন করে।

 |
| **XMP Stream Copy** | কাস্টম XMP XML প্যাকেট হুবহু কপি ও সিঙ্ক করে।

 |
| **Exact Size Padding** | বাইট-টু-বাইট সোর্স ফাইলের সমান ফাইল সাইজ নিশ্চিত করে।

 |

```

```