import requests
import bs4
import pandas as pd
import os
import urllib.request
from urllib.error import HTTPError

if not os.path.exists('images'):
    os.makedirs('images')

#request the NY Yankees Wikipedia Page
url = "https://en.wikipedia.org/wiki/New_York_Yankees"
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, "html.parser")

## SCRAPE IMAGES ##

# get image from <figure> tags (main images)
image_links = []
images = soup.select("img")
for img in images:
    src = img.get("src")
    if src and "upload.wikimedia.org" in src:
        image_links.append(f"https:{src}")

        

# dowload images to folder
for index, url in enumerate(image_links):
    file_name = f'img_{index}.jpg'
    file_path = f'images/{file_name}'
    print(f"Downloading {file_name} from {url}")
    try:
        urllib.request.urlretrieve(url, file_path)
    except HTTPError as err:
        print(f"Failed to download {url} with error code: {err.code}")

print(f"Found {len(image_links)} image links.")
for i, link in enumerate(image_links[:5]):  # Print a preview
    print(f"{i+1}: {link}")



## SCRAPE SECITON HEADINGS ##
# extract all headings
headings = []
for heading in soup.select(".mw-heading3"):
    headings.append(heading.text.strip())

#save headings to CSV
headings_df = pd.DataFrame({"headings": headings})
headings_df.to_csv("yankees_headings.csv", index=False)
print("Saved headings to 'yankees_headings.csv'")


## SCRAPE TEXT ##
# extract text
paragraphs = []
for para in soup.select("p"):
    text = para.get_text().strip()
    if text:
        paragraphs.append(text)


#save paragraphs to csv
paragraphs_df = pd.DataFrame({"paragraphs": paragraphs})
paragraphs_df.to_csv("yankees_paragraphs.csv", index=False)
print("Saved paragraphs to 'yankees_paragraphs.csv'")

print()