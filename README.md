# 📧 Website URL to Email Extractor

A Python automation tool that visits business websites, extracts **email addresses** and detects **location information** automatically.

This script is perfect for:

* Lead generation
* Cold outreach campaigns
* Email list building
* Business contact discovery

---

## 🚀 Overview

The **Website URL to Email Extractor** reads website URLs from a CSV file, visits each website, and searches for:

* Contact email addresses
* Business location / city
* Additional contact details from pages like:

  * `/contact`
  * `/contact-us`
  * `/contactus`
  * `/about`

The extracted data is saved into a new CSV file.

---

## ✨ Features

### 🔍 Email Extraction

Finds emails from:

* Visible page text
* `mailto:` links
* Contact pages
* About pages

Example:

```text
info@restaurant.com
support@restaurant.com
hello@business.com
```

---

### 📍 Location Detection

Attempts to detect business location from:

* Page content
* Meta tags
* Contact page content

Example:

```text
Raleigh, NC
Charlotte, NC
New York, NY
```

---

### 💾 Resume Support

If the script stops unexpectedly, it resumes from the last processed row using a checkpoint file.

File used:

```bash
progress_checkpoint.txt
```

---

### ♻️ Duplicate Prevention

Avoids saving duplicate:

* Business names
* Email combinations

---

### 📊 CSV Input / Output

Input file:

```bash
restaurant_data.csv
```

Output file:

```bash
restaurant_emails.csv
```

---

## 🛠️ Tech Stack

Built with:

* **Python**
* **Requests**
* **BeautifulSoup4**
* **CSV**
* **Regex**
* **OS / Time / urllib**

---

## 📁 Project Structure

```bash
website-url-to-email/
│
├── website_url_to_email.py      # Main script
├── restaurant_data.csv          # Input file
├── restaurant_emails.csv        # Output file
├── progress_checkpoint.txt      # Resume progress file
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd website-url-to-email
```

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## ▶️ Usage

Run the script:

```bash
python website_url_to_email.py
```

---

## 🔧 Configuration

Inside the script you can modify:

### Input CSV

```python
INPUT_CSV = "restaurant_data.csv"
```

---

### Output CSV

```python
OUTPUT_CSV = "restaurant_emails.csv"
```

---

### Progress File

```python
PROGRESS_FILE = "progress_checkpoint.txt"
```

---

## 📄 Input CSV Format

Example:

```csv
Restaurant Name,Website,Address
ABC Cafe,https://abccafe.com,Raleigh NC
XYZ Bakery,https://xyzbakery.com,Charlotte NC
```

---

## 📊 Output CSV Format

Example:

```csv
Restaurant Name,Email,Location
ABC Cafe,info@abccafe.com,Raleigh NC
XYZ Bakery,support@xyzbakery.com,Charlotte NC
```

---

## ⚠️ Notes

* Some websites may block bots or scraping attempts.
* Not all websites display public email addresses.
* Email extraction depends on website structure.
* Be respectful and follow legal/ethical scraping practices.

---

## 🚀 Future Improvements

Possible upgrades:

* Extract phone numbers
* Extract social media links
* Multi-threading for faster processing
* Proxy support / anti-blocking
* Export to Excel

---

## 🤝 Contributing

Contributions are welcome.

To contribute:

1. Fork the repository
2. Create a branch
3. Make your changes
4. Submit a pull request

---

## 💡 Author

Developed by **Malki Aman**.
