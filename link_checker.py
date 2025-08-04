import os
import re

def find_markdown_files(directories):
    markdown_files = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".md") or file.endswith(".mdx"):
                    markdown_files.append(os.path.join(root, file))
    return markdown_files

def find_links(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Regex to find markdown links: [text](link)
    link_pattern = re.compile(r"\[.*?\]\((.*?)\)")
    return link_pattern.findall(content)

def check_links(markdown_files):
    broken_links = {}
    for file_path in markdown_files:
        links = find_links(file_path)
        for link in links:
            if not link.startswith("http") and not link.startswith("#") and not link.startswith("mailto:"):
                # It's an internal link
                link_path = os.path.join(os.path.dirname(file_path), link)
                if not os.path.exists(link_path):
                    if file_path not in broken_links:
                        broken_links[file_path] = []
                    broken_links[file_path].append(link)
    return broken_links

if __name__ == "__main__":
    directories_to_check = ["blog", "docs", "community"]
    markdown_files = find_markdown_files(directories_to_check)
    broken_links = check_links(markdown_files)

    if broken_links:
        print("Broken links found:")
        for file, links in broken_links.items():
            print(f"  In file: {file}")
            for link in links:
                print(f"    - {link}")
    else:
        print("No broken links found.")
