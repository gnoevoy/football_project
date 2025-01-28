# Web Scraping

**Aim:**  
Scrape data from RGOL and upload it to Google Cloud Storage.

**Result:**  
- Structured CSV files  
- 2 folders containing content images

<br>

## Workflow
1. **Scrape Product Links:**  
   - Scrape links for balls and boots products.  
   - Store the links in a JSON file.
2. **Scrape Product Data:**  
   - Extract detailed product data and images.  
   - Store images in a folder and data in CSV files.
3. **Data Cleaning & Transformation:**  
   - Clean and transform raw scraped data into a structured format.
4. **Upload to Google Cloud:**  
   - Upload cleaned data and images to Google Cloud Storage.

<br>

## Notes:
-  Testing wasn't used in this project. However, `try-except` blocks were implemented to handle errors and notify the user, without interrupting the process.
- The `data` folder is excluded in the `.gitignore` file to prevent uploading large files, such as images and CSV files, to GitHub.

<br>

## Folder Structure

| Folder                        | File                                |
|-------------------------------|-------------------------------------|
| **data**                       | `data/cleaned_data`                |
|                               | `data/product_images`              |
|                               | `data/raw_data`                    |
|                               | `data/scraped_links.json`          |
| **helper_functions**           | `helper_functions/links_helpers.py`|
|                               | `helper_functions/products_helpers.py`|
| **scripts**                    | `scripts/data_cleaning.ipynb`      |
|                               | `scripts/get_links.py`             |
|                               | `scripts/get_products_data.py`     |
|                               | `scripts/upload_to_cloud.py`       |