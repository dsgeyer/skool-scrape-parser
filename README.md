# Skool Data Parser

This Python script, `parse_skool_data.py`, is designed to process data scraped from Skool.com and transform it into a structured HTML file. The primary purpose is to make the scraped posts and their associated comments easily viewable in a web browser.

## Data Source

The data processed by this script is obtained using a scraper from Appify.com. Specifically, the `memo23/skool-posts-with-comments-scraper` actor is used to pull down all relevant post and comment data from Skool.com in a verbose JSON format.

## Functionality

The script performs the following actions:

1.  **Reads Input JSON**: It takes a JSON file (by default, `dataset_skool-posts-with-comments-scraper_2025-05-21_17-55-28-456.json`) as input. This file should contain the posts and comments scraped from Skool.com.
2.  **Parses Data**: It iterates through the posts and their nested comments.
3.  **Formats Content**: Text content is escaped for HTML safety, and newlines are converted to `<br>` tags for proper display.
4.  **Generates HTML**: It constructs an HTML document with a clean, readable structure. Posts are displayed with their titles, authors, dates, and content. Comments are nested under their respective posts, showing the commenter, date, and comment content. Replies to comments are also handled and displayed with appropriate indentation.
5.  **Outputs HTML File**: The final HTML content is written to an output file (by default, `skool_posts_formatted.html`).

## Requirements

-   Python 3

## Usage

1.  **Scrape Data**:
    *   Go to Appify.com and use the `memo23/skool-posts-with-comments-scraper` actor to scrape the desired Skool.com community.
    *   Download the resulting data as a JSON file.

2.  **Prepare Input File**:
    *   Place the downloaded JSON file in the same directory as the `parse_skool_data.py` script.
    *   By default, the script looks for a file named `dataset_skool-posts-with-comments-scraper_2025-05-21_17-55-28-456.json`. If your JSON file has a different name, you will need to update the `input_filename` variable within the `main()` function in the script.

3.  **Run the Script**:
    Open your terminal or command prompt, navigate to the directory containing the script and the JSON file, and execute the script using:
    ```bash
    python3 parse_skool_data.py
    ```

4.  **View Output**:
    *   After successful execution, an HTML file named `skool_posts_formatted.html` (by default) will be created in the same directory.
    *   Open this HTML file in any web browser to view the formatted posts and comments.

## Customization

-   **Input/Output Filenames**: You can change the default input JSON filename and the output HTML filename by modifying the `input_filename` and `output_filename` variables in the `main()` function of the `parse_skool_data.py` script.
-   **Styling**: The HTML output includes inline CSS for styling. You can modify the `<style>` section in the `html_output_parts` list within the `main()` function to change the appearance of the posts and comments. 