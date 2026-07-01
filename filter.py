import os
import shutil
import urllib.request
import json

SOURCE_URL = "https://raw.githubusercontent.com/keiyoushi/extensions/repo/index.min.json"
APK_BASE_URL = "https://raw.githubusercontent.com/keiyoushi/extensions/repo/apk/"

# --- CONFIGURATION ---
ALLOWED_PACKAGES = {
    "eu.kanade.tachiyomi.extension.en.weebcentral",
    "eu.kanade.tachiyomi.extension.all.mangadex",
    "eu.kanade.tachiyomi.extension.en.readallcomicscom"
}
# ---------------------

# Wipe existing apk folder to remove outdated versions
if os.path.exists("apk"):
    shutil.rmtree("apk")
os.makedirs("apk")

try:
    print("Fetching original Keiyoushi index...")
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        extensions_list = json.loads(response.read().decode('utf-8'))
    
    filtered_list = []
    for item in extensions_list:
        pkg_name = item.get("pkg")
        
        if pkg_name in ALLOWED_PACKAGES:
            apk_filename = item.get("apk")
            
            # Download the APK directly into our folder
            print(f"Downloading {apk_filename}...")
            apk_url = APK_BASE_URL + apk_filename
            urllib.request.urlretrieve(apk_url, os.path.join("apk", apk_filename))
            
            print(f"Keeping allowed package: {pkg_name}")
            filtered_list.append(item)
            
    # Save the cleaned, minified file
    with open("index.min.json", "w", encoding="utf-8") as f:
        json.dump(filtered_list, f, ensure_ascii=False, separators=(',', ':'))
        
    print(f"Done! Saved {len(filtered_list)} extensions and their APKs.")

except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
