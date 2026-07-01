import urllib.request
import json

# URL of the official Keiyoushi repo index
SOURCE_URL = "https://raw.githubusercontent.com/keiyoushi/extensions/repo/index.min.json"

# --- CONFIGURATION ---
# Add ONLY the exact package names ("pkg") you want to KEEP
ALLOWED_PACKAGES = {
    "eu.kanade.tachiyomi.extension.en.weebcentral",
    "eu.kanade.tachiyomi.extension.en.mangadex",
    "eu.kanade.tachiyomi.extension.en.readallcomicscom"
}
# ---------------------

try:
    print("Fetching original Keiyoushi index...")
    req = urllib.request.Request(SOURCE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        extensions_list = json.loads(response.read().decode('utf-8'))
    
    # Keep ONLY allowed items
    filtered_list = []
    for item in extensions_list:
        pkg_name = item.get("pkg")
        
        if pkg_name in ALLOWED_PACKAGES:
            print(f"Keeping allowed package: {pkg_name}")
            filtered_list.append(item)
            
    # Save the cleaned, minified file
    with open("index.min.json", "w", encoding="utf-8") as f:
        json.dump(filtered_list, f, ensure_ascii=False, separators=(',', ':'))
        
    print(f"Done! Remaining extensions: {len(filtered_list)}")

except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
