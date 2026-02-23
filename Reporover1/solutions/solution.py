import os
from bs4 import BeautifulSoup

def extract_html_code_block(file_path):
    """Extracts HTML code block from a file and returns it as a string."""
    with open(file_path, 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup.prettify()

def save_as_index_html(html_content):
    """Saves the given HTML content to an index.html file."""
    with open('index.html', 'w') as f:
        f.write(html_content)

def check_title_tag(file_path):
    """Checks if the <title> tag of a webpage contains 'Weather Dashboard'."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        title_tag = soup.find('title')
        return 'Weather Dashboard' in title_tag.text
    except Exception as e:
        print(f"Error checking title tag: {e}")
        return False

def main():
    readme_file_path = 'README.md'
    index_html_file_path = 'index.html'

    # Extract HTML code block from README.md and save it to index.html
    html_content = extract_html_code_block(readme_file_path)
    save_as_index_html(html_content)

    # Check if the <title> tag of the webpage contains 'Weather Dashboard'
    result = check_title_tag(index_html_file_path)
    if result:
        print("Test passed: The <title> tag contains 'Weather Dashboard'.")
        exit(0)
    else:
        raise Exception("Test failed: The <title> tag does not contain 'Weather Dashboard'.")

if __name__ == "__main__":
    main()