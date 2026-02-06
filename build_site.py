import pandas as pd
import os
import shutil

# 1. Update this with your "Published as CSV" link from Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSjyLEY2kIFUvpkUxicEmzGnmxS47TAUMhLOfoKV5L0WzGMMekkjlLWsjG2-AcCk1W-2w_9a4LkjfKI/pub?output=csv"
TEMPLATE_FILE = "template.html"
OUTPUT_DIR = "products"

def build():
    # Load the data
    try:
        df = pd.read_csv(SHEET_URL)
    except Exception as e:
        print(f"Error loading sheet: {e}")
        return

    # Load the skeleton
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        skeleton = f.read()

    # Clear out old auto-generated products to keep it clean
   # if os.path.exists(OUTPUT_DIR):
    #    shutil.rmtree(OUTPUT_DIR)
    #os.makedirs(OUTPUT_DIR)

    for index, row in df.iterrows():
        # Create a folder for each product (The "Slug")
        slug = str(row['slug']).strip().lower().replace(" ", "-")
        product_path = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(product_path, exist_ok=True)

        # Replace placeholders
        page_content = skeleton
        page_content = page_content.replace('{{PRODUCT_TITLE}}', str(row['title']))
        page_content = page_content.replace('{{REVIEW_TEXT}}', str(row['review']))
        page_content = page_content.replace('{{AMAZON_LINK}}', str(row['amazon_url']))
        page_content = page_content.replace('{{IMAGE_1}}', str(row['img1']))
        page_content = page_content.replace('{{IMAGE_2}}', str(row['img2']))
        page_content = page_content.replace('{{IMAGE_3}}', str(row['img3']))

        # Save as index.html inside the product folder
        with open(os.path.join(product_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page_content)
        
        print(f"✅ Generated: /{OUTPUT_DIR}/{slug}/")

if __name__ == "__main__":
    build()
