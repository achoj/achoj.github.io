import os
import re
from datetime import datetime
import markdown
import dominate
from dominate.tags import *
from dominate.util import *

def read_markdown_file(filename):
    """Read Markdown content from a file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def convert_markdown_to_html(md_content):
    """Convert Markdown content to HTML."""
    md = markdown.Markdown(extensions=['md_in_html', 'meta','tables', 'fenced_code'])
    html_content = md.convert(md_content)
    post_date = md.Meta.get('post-date', '')
    logo_path = md.Meta.get('logo', '')
    title = md.Meta.get('title', '')
    type = md.Meta.get('type', [])
    return title, html_content, post_date, logo_path, type

def create_html_document(html_content, post_date, logo_path, title):
    """Create HTML document."""
    doc = dominate.document(title=title)
    with doc.head:
        meta(charset="utf-8")
        meta(name="viewport", content="width=device-width, initial-scale=0.55")
        link(rel="stylesheet", href="/source/post.css")

    with doc:
        with header():
            a("AchoJ's Web Page", href="/index.html", cls="wiki-header")
            a("Back to home", href="/index.html", cls="back-to-home")
        with div(cls="content", id="md"):
            with p(cls="site"):
                span(post_date,cls="post_date")
                a("@achoj",href="mailto:shoutoudelanfanqie@gmail.com")
            h1(title)
            if logo_path != "":
                with p(cls="logo"):
                    img(src=logo_path[0], width="300px")
            div(raw(html_content), cls="markdown-content")
    return doc

def write_html_to_file(doc, filename):
    """Write HTML content to file."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(doc.render(pretty=True))

def generate_html_from_md(filename, output_folder):
    """Generate HTML from Markdown file."""
    md_content = read_markdown_file(filename)
    title, html_content, post_date, logo_path, type = convert_markdown_to_html(md_content)
    doc = create_html_document(html_content, post_date, logo_path, title)
    html_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(filename))[0]}.html")
    write_html_to_file(doc, html_filename)
    return title, html_filename, type, post_date, logo_path

def process_folder(input_folder, output_folder):
    """Process all Markdown files in a folder."""
    metadata_list = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, input_folder)
                output_path = os.path.join(output_folder, os.path.dirname(relative_path))
                os.makedirs(output_path, exist_ok=True)
                title, html_filename, type, post_date, logo_path = generate_html_from_md(filepath, output_path)
                metadata_list.append({'filepath': filepath, 
                                      'html_filepath': html_filename, 
                                      'type': type, 
                                      'post_date': post_date, 
                                      'logo_path': logo_path,
                                      'title': title})
    return metadata_list

def generate_index(posts_list):
    """Generate index HTML file."""
    doc = dominate.document(title="Achoj's Web Page")
    with doc.head:
        meta(charset="utf-8")
        meta(name="viewport", content="width=device-width, initial-scale=0.6")
        link(rel="stylesheet", href="/source/index.css")

    with doc:
        with div(cls="content", id="md"):
            h1("Achoj's Web Page")
            with table(width="100%"):
                tr()
                with td(width="50%", valign="top"):
                    h2("Daily articles")
                    with ul():
                        for item in posts_list:
                            print(item["type"])
                            html_filepath = item["html_filepath"].replace("\\", "/")
                            title = item["title"]
                            if item["type"][0] == "daily":
                                with li():   
                                    a(title, href=html_filepath)
                                    br()
                                    small(item["post_date"], cls="post-date")
                with td(width="50%", valign="top"):
                    h2("Programming articles")
                    with ul():
                        for item in posts_list:
                            print(item["type"])
                            html_filepath = item["html_filepath"].replace("\\", "/")
                            title = item["title"]
                            if item["type"][0] == "programming":
                                with li():   
                                    a(title, href=html_filepath)
                                    br()
                                    small(item["post_date"], cls="post-date")

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(doc.render(pretty=True))

# 新增的排序函数
def sort_metadata_by_post_date(metadata_list):
    """Sort metadata list by post date."""
    def get_post_date(item):
        # Extract post date and convert it to datetime object
        post_date_str = item['post_date'][0]
        return datetime.strptime(post_date_str, "%Y.%m.%d")
    
    return sorted(metadata_list, key=get_post_date, reverse=True)

if __name__ == "__main__":
    input_folder_path = 'articles/'
    output_folder_path = 'articles-html/'
    metadata_list = process_folder(input_folder_path, output_folder_path)
    sorted_meta_list = sort_metadata_by_post_date(metadata_list)
    generate_index(sorted_meta_list)
