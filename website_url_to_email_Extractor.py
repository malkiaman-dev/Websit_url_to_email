# url_to_email_and_location_v2.py
# pip install requests beautifulsoup4

import csv
import re
import os
import requests
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

INPUT_CSV = "restaurant_data.csv"
OUTPUT_CSV = "restaurant_emails.csv"
PROGRESS_FILE = "progress_checkpoint.txt"

HEADERS = {"User-Agent": "Mozilla/5.0"}
EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def normalize_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if not url:
        return ""
    if not url.lower().startswith(("http://", "https://")):
        url = "https://" + url
    return url

def find_emails_in_soup(soup: BeautifulSoup) -> set:
    emails = set()

    # Visible text
    text = soup.get_text(" ", strip=True)
    emails.update(EMAIL_REGEX.findall(text))

    # Mailto links
    for a in soup.select('a[href^="mailto:"]'):
        href = a.get("href", "")
        addr = href.replace("mailto:", "").split("?")[0].strip()
        if addr:
            emails.add(addr)

    return emails

def try_fetch(url: str, timeout=10):
    try:
        return requests.get(url, timeout=timeout, headers=HEADERS, allow_redirects=True)
    except Exception:
        return None

def extract_contact_info(url: str):
    emails, location = set(), ""
    url = normalize_url(url)
    if not url:
        return "", ""

    resp = try_fetch(url)
    if not resp or not resp.ok:
        return "", ""

    soup = BeautifulSoup(resp.text, "html.parser")
    emails |= find_emails_in_soup(soup)

    text = soup.get_text(" ", strip=True)
    m = re.search(r"\b([A-Z][a-z]+(?:,?\s[A-Z][a-z]+){0,2})\s(?:USA|United States|US)?\b", text)
    if m:
        location = m.group(0)

    if not location:
        metas = " ".join([m.get("content", "") for m in soup.find_all("meta") if m.get("content")])
        m2 = re.search(r"[A-Z][a-z]+,\s[A-Z]{2}\b", metas)
        if m2:
            location = m2.group(0)

    if not emails:
        for path in ("/contact", "/contact-us", "/contactus", "/about"):
            c_url = urljoin(url, path)
            c_resp = try_fetch(c_url, timeout=8)
            if c_resp and c_resp.ok:
                c_soup = BeautifulSoup(c_resp.text, "html.parser")
                found = find_emails_in_soup(c_soup)
                if found:
                    emails |= found
                    c_text = c_soup.get_text(" ", strip=True)
                    m3 = re.search(r"[A-Z][a-z]+,\s[A-Z]{2}\b", c_text)
                    if m3 and not location:
                        location = m3.group(0)
                    break

    email = ", ".join(sorted(emails)) if emails else ""
    return email, location

def load_existing_pairs(path: str) -> set:
    pairs = set()
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pairs
    try:
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)
            for row in r:
                if len(row) >= 2:
                    name, email = row[0].strip(), row[1].strip()
                    if name and email:
                        pairs.add((name.lower(), email.lower()))
    except Exception:
        pass
    return pairs

def save_progress(index):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(index))

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def main():
    print("🔍 Starting extraction from websites...")

    already_written = load_existing_pairs(OUTPUT_CSV)
    resume_index = load_progress()

    with open(INPUT_CSV, newline="", encoding="utf-8") as infile, open(
        OUTPUT_CSV, "a", newline="", encoding="utf-8", buffering=1
    ) as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        name_col = next((h for h in reader.fieldnames if h and "name" in h.lower()), None)
        url_col = next((h for h in reader.fieldnames if h and "website" in h.lower()), None)
        address_col = next((h for h in reader.fieldnames if h and "address" in h.lower()), None)

        if not url_col:
            print("❌ No column found with 'website' in its name.")
            return

        if outfile.tell() == 0:
            writer.writerow(["Restaurant Name", "Email", "Location"])

        rows = list(reader)
        total_urls = len(rows)
        print(f"📊 Total URLs to process: {total_urls}")

        for idx, row in enumerate(rows):
            # Skip processed URLs
            if idx < resume_index:
                continue

            name = row.get(name_col, "").strip() if name_col else ""
            website = row.get(url_col, "").strip()
            base_location = row.get(address_col, "").strip() if address_col else ""

            if not website:
                continue

            print(f"\n➡️ [{idx+1}/{total_urls}] Visiting: {website}")

            email, detected_location = extract_contact_info(website)
            final_location = detected_location or base_location

            if email:
                key_pairs = [(name.lower(), e.strip().lower()) for e in email.split(",")]
                if any(k in already_written for k in key_pairs):
                    print("ℹ️ Already saved earlier. Skipping duplicate.")
                else:
                    writer.writerow([name, email, final_location])
                    outfile.flush()
                    try:
                        os.fsync(outfile.fileno())
                    except Exception:
                        pass
                    for k in key_pairs:
                        already_written.add(k)
                    print(f"✅ Saved: {name} -> {email}")
            else:
                print("⚠️ No email found.")

            save_progress(idx + 1)
            remaining = total_urls - (idx + 1)
            print(f"Progress: {idx+1}/{total_urls} completed | Remaining: {remaining}")
            time.sleep(2)

    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

    print("\n✅ Extraction completed successfully! Results saved in:", OUTPUT_CSV)

if __name__ == "__main__":
    main()
