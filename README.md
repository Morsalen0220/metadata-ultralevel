```markdown
# Comprehensive PDF Utility Scripts Suite

এই সুইটটিতে PDF ফাইলের মেটাডেটা, সাইজ, টাইমেস্ট্যাম্প (Created/Modified Date) এবং কাস্টম অ্যাট্রিবিউটস ম্যানিপুলেট করার জন্য ৪টি পাইথন স্ক্রিপ্ট রয়েছে।

---

## 📌 ফাইলসমূহের সংক্ষিপ্ত বিবরণ

1. **`pdfsize-adjust.py`**: PDF ফাইলের সাইজ ৬০ KB থেকে ৬৭ KB (টার্গেট ৬৪ KB)-এর মধ্যে এডজাস্ট করে এবং `modDate` মুছে ফেলে[cite: 1]।
2. **`purecopy.py`**: একটি সোর্স PDF-এর সমস্ত মেটাডেটা, কাস্টম XMP, ফাইল সাইজ ও Windows টাইমেস্ট্যাম্প অবিকল টার্গেট PDF-এ ক্লোন করে[cite: 2]।
3. **`self-pdf-dates.py`**: ফোল্ডারের সব PDF-এর অভ্যন্তরীণ মেটাডেটা তারিখ এবং Windows OS-এর টাইমেস্ট্যাম্প নির্দেশিত নির্দিষ্ট তারিখে সেট করে[cite: 3]।
4. **`removemetadatawithmodified.py`**: PDF-এর অভ্যন্তরীণ সমস্ত স্ট্যান্ডার্ড মেটাডেটা এবং রিভিশন হিস্ট্রি সম্পূর্ণ ক্লিয়ার/ওয়াইপ করে[cite: 4]।

---

## 🚀 পরিবেশ ও ডিপেনডেন্সি (Prerequisites)

- **অপারেটিং সিস্টেম:** Windows OS (PowerShell ও File System-এর কমান্ডের জন্য প্রযোজ্য)।
- **টার্মিনাল:** Command Prompt (CMD) বা PowerShell (পছন্দনীয়: Run as Administrator)।
- **ডিপেনডেন্সি ইনস্টলেশন:**
  ```cmd
  pip install pymupdf

```

---

## 🛠️ স্ক্রিপ্টসমূহের বিস্তারিত ও ব্যবহারের নির্দেশিকা

### ১. `pdfsize-adjust.py` (PDF Size Adjuster & ModDate Stripper)

ফোল্ডারের সব PDF স্ক্যান করে সাইজ ৬০–৬৭ KB বানিয়ে দেয় এবং `modDate` মুছে ফেলে।

#### ব্যবহারের কমান্ড:

* **বর্তমান ফোল্ডারে:**
```cmd
python pdfsize-adjust.py

```


* **নির্দিষ্ট ফোল্ডারে:**
```cmd
python pdfsize-adjust.py "C:\path\to\your\pdf_folder"

```



#### পরিবর্তন ও রিমুভাল:

* **রিমুভ:** PDF মেটাডেটা থেকে `modDate` মুছে ফাঁকা করা হয় এবং ৬৭ KB-এর বড় ফাইলে `garbage=4` দিয়ে অতিরিক্ত ডাটা ক্লিন করা হয়।


* **পরিবর্তন:** < 60 KB ফাইলগুলোকে বাইনারি কমেন্ট প্যাডিং (`%PADDING_...`) দিয়ে ৬৪ KB করা হয় এবং > 67 KB ফাইলগুলোকে কম্প্রেস করা হয়।



---

### ২. `purecopy.py` (Exact Attribute & Metadata Cloner)

একটি সোর্স PDF থেকে মেটাডেটা, XMP, সাইজ ও Windows টাইমেস্ট্যাম্প হুবহু টার্গেট PDF-এ ক্লোন করে।

#### ব্যবহারের কমান্ড:

```cmd
python purecopy.py source.pdf target.pdf

```

#### পরিবর্তন ও রিমুভাল:

* **রিমুভ:** সোর্স ফাইলে যে মেটাডেটা নেই (যেমন `modDate` না থাকলে), তা টার্গেট থেকেও ক্লিয়ার করে দেওয়া হয়। টার্গেটের পুরনো ইতিহাস ক্লিয়ার হয়।


* **পরিবর্তন:** PDF Info dictionary, XMP XML, Exact byte size padding এবং Windows Created/Modified/Accessed Date সোর্সের অবিকল বানানো হয়।



---

### ৩. `self-pdf-dates.py` (Custom Date Setter)

আপনার ইনপুট দেওয়া তারিখ (`YYYY-MM-DD HH:MM:SS`) অনুযায়ী PDF-এর অভ্যন্তরীণ মেটাডেটা এবং Windows OS টাইমেস্ট্যাম্প সিঙ্ক করে।

#### ব্যবহারের কমান্ড:

* **বর্তমান ফোল্ডারে:**
```cmd
python self-pdf-dates.py "2024-05-15 10:30:00"

```


* **নির্দিষ্ট ফোল্ডারে:**
```cmd
python self-pdf-dates.py "2024-05-15 10:30:00" "C:\path\to\your\pdf_folder"

```



#### পরিবর্তন ও রিমুভাল:

* **রিমুভ:** পুরনো তৈরির ও মডিফাই করার তারিখ মুছে যায় এবং `garbage=4` দিয়ে ফাইল ক্লিন হয়।


* **পরিবর্তন:** PDF মেটাডেটার `creationDate` ও `modDate` এবং Windows OS-এর Created, Modified, ও Access Date একসাথে ইনপুট তারিখে সেট হয়।



---

### ৪. `removemetadatawithmodified.py` (Complete Metadata Stripper)

PDF-এর সমস্ত অভ্যন্তরীণ মেটাডেটা ফিল্ড এক ক্লিকে মুছে সাফ করে দেয়।

#### ব্যবহারের কমান্ড:

* **বর্তমান ফোল্ডারে:**
```cmd
python removemetadatawithmodified.py

```


* **নির্দিষ্ট ফোল্ডারে:**
```cmd
python removemetadatawithmodified.py "C:\path\to\your\pdf_folder"

```



#### পরিবর্তন ও রিমুভাল:

* **রিমুভ:** Title, Author, Subject, Keywords, Creator, Producer, CreationDate, ModDate সহ সব স্ট্যান্ডার্ড ফিল্ড মুছে ফাঁকা (`""`) করা হয়।


* **পরিবর্তন:** `garbage=4` ও `deflate=True` ব্যবহারে অপ্রয়োজনীয় রিভিশন হিস্ট্রি ডিলেট হয়ে ফাইল স্ট্রাকচার ক্লিন ও অপটিমাইজড হয়।



---

## 📝 এক নজরে সামারি টেবিল

| স্ক্রিপ্ট | মূল কাজ | প্রসেসিং স্কোপ | মূল মেটাডেটা অ্যাকশন |
| --- | --- | --- | --- |
| **`pdfsize-adjust.py`** | ফাইল সাইজ ৬০–৬৭ KB করা

 | পুরো ফোল্ডার

 | `modDate` মুছে ফেলা হয়

 |
| **`purecopy.py`** | সোর্স থেকে মেটাডেটা/টাইম ক্লোন করা

 | ২ টি নির্দিষ্ট ফাইল

 | সোর্সের অবিকল সিঙ্ক করা হয়

 |
| **`self-pdf-dates.py`** | কাস্টম সময় ও তারিখ বসানো

 | পুরো ফোল্ডার

 | মেটাডেটা ও OS টাইম সিঙ্ক করা হয়

 |
| **`removemetadatawithmodified.py`** | মেটাডেটা সম্পূর্ণ মুছে ফেলা

 | পুরো ফোল্ডার

 | সব মেটাডেটা ফাঁকা (`""`) করা হয়

 |

```

```
