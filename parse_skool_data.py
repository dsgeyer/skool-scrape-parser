// python3 parse_skool_data.py

import json
import html

def format_content_to_html(text_content):
    """Escapes HTML special characters in text and replaces newlines with <br> tags."""
    if not text_content:
        return ""
    escaped_content = html.escape(text_content)
    return escaped_content.replace('\n', '<br>\n')

def process_comment_html(comment_data, level=0):
    """Recursively processes a comment and its children to generate HTML.

    Args:
        comment_data (dict): The comment object from the JSON.
        level (int): The nesting level of the comment (for indentation).

    Returns:
        str: HTML representation of the comment and its replies.
    """
    comment_html_parts = []
    comment_post = comment_data.get('post', {})
    user = comment_post.get('user', {})
    metadata = comment_post.get('metadata', {})

    author_fn = user.get('firstName', 'N/A')
    author_ln = user.get('lastName', '')
    author = f"{author_fn} {author_ln}".strip()
    date = comment_post.get('created_at', 'N/A')
    content = metadata.get('content', 'No content')

    formatted_content = format_content_to_html(content)
    
    style = f"margin-left: {20 * level}px;" if level > 0 else ""

    comment_html_parts.append(f"""
    <div class="comment {'reply' if level > 0 else ''}" style="{style}">
        <p class="author-date"><strong>Comment by:</strong> {html.escape(author)} <strong>on:</strong> {html.escape(date)}</p>
        <div class="content">{formatted_content}</div>
    """)

    children = comment_data.get('children', [])
    if children:
        comment_html_parts.append('<div class="replies">')
        for child_comment_data in children:
            comment_html_parts.append(process_comment_html(child_comment_data, level + 1))
        comment_html_parts.append('</div>')

    comment_html_parts.append("</div>")
    return "".join(comment_html_parts)

def main():
    """Main function to parse JSON data and generate HTML."""
    input_filename = 'dataset_skool-posts-with-comments-scraper_2025-05-21_17-55-28-456.json'
    output_filename = 'skool_posts_formatted.html'
    posts_data = []

    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_filename}'. Ensure it's a valid JSON file.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    html_output_parts = ["""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skool Posts and Comments</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.7; margin: 0; padding: 0; background-color: #eef1f5; color: #333; }
        .container { max-width: 900px; margin: 20px auto; padding: 20px; background-color: #fff; box-shadow: 0 0 15px rgba(0,0,0,0.1); border-radius: 8px; }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        .post { background-color: #fff; border: 1px solid #d1d9e0; margin-bottom: 25px; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .post h2 { color: #3498db; margin-top: 0; margin-bottom: 8px; font-size: 1.8em; }
        .author-date { font-size: 0.95em; color: #7f8c8d; margin-bottom: 15px; border-bottom: 1px solid #ecf0f1; padding-bottom: 10px; }
        .author-date strong { color: #555; }
        .content { margin-bottom: 20px; font-size: 1.05em; color: #4a4a4a; }
        .content br { margin-bottom: 8px; } /* Add space after <br> */
        .comments-section { margin-top: 25px; padding-top: 20px; border-top: 2px solid #bdc3c7; }
        .comments-section h3 { margin-top: 0; color: #34495e; font-size: 1.4em; margin-bottom: 15px; }
        .comment { background-color: #f8f9fa; border: 1px solid #e0e6ed; padding: 15px; margin-bottom: 12px; border-radius: 6px; position: relative; }
        .comment.reply { background-color: #e9edf2; }
        .comment .author-date { font-size: 0.9em; margin-bottom: 8px; padding-bottom: 5px; border-bottom-style: dashed; }
        .comment .content { font-size: 1em; }
        .replies { margin-top: 12px; padding-left: 25px; border-left: 3px solid #ced4da; }
    </style>
</head>
<body>
    <div class="container">
    <h1>Skool Posts and Comments</h1>
"""]

    for item in posts_data:
        metadata = item.get('metadata', {})
        user = item.get('user', {})

        post_title = metadata.get('title', 'No Title')
        post_content_raw = metadata.get('content', 'No Content')
        post_author_fn = user.get('firstName', 'N/A')
        post_author_ln = user.get('lastName', '')
        post_author = f"{post_author_fn} {post_author_ln}".strip()
        post_date = item.get('createdAt', 'N/A')

        post_content_formatted = format_content_to_html(post_content_raw)

        html_output_parts.append(f"""
    <div class="post">
        <h2>{html.escape(post_title)}</h2>
        <p class="author-date"><strong>Posted by:</strong> {html.escape(post_author)} <strong>on:</strong> {html.escape(post_date)}</p>
        <div class="content">{post_content_formatted}</div>
""")

        comments = item.get('comments', [])
        if comments:
            html_output_parts.append("""
        <div class="comments-section">
            <h3>Comments:</h3>
""")
            for comment_data in comments:
                html_output_parts.append(process_comment_html(comment_data, level=0))
            html_output_parts.append("""
        </div>""") # End comments-section

        html_output_parts.append("""
    </div>""") # End post

    html_output_parts.append("""
    </div> <!-- End container -->
</body>
</html>
""")
    
    final_html = "".join(html_output_parts)

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Successfully parsed data and wrote HTML to '{output_filename}'")
    except IOError:
        print(f"Error: Could not write to output file '{output_filename}'. Check permissions.")
    except Exception as e:
        print(f"An unexpected error occurred while writing the file: {e}")

if __name__ == '__main__':
    main() 