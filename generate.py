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
    md = markdown.Markdown(extensions=['md_in_html', 'meta', 'toc', 'tables', 'fenced_code'])
    html_content = md.convert(md_content)
    post_date = md.Meta.get('post-date', '')
    edit_date = md.Meta.get('edit-date', '')
    title = md.Meta.get('title', '')
    tags = md.Meta.get('tags', [])
    toc_content = md.toc
    return title, html_content, post_date, edit_date, tags, toc_content

def create_html_document(html_content, post_date, edit_date, toc_content):
    """Create HTML document."""
    doc = dominate.document(title="Achoj's Wiki")
    with doc.head:
        meta(charset="utf-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        title("Achoj's Wiki")
        link(rel="icon", href="/source/images/favicon.ico")
        link(rel="stylesheet", href="/source/default.min.css")
        script(src="/source/highlight.min.js", type="text/javascript")
        link(rel="stylesheet", href="/source/styles.css")
        script("hljs.highlightAll();")

    with doc:
        with header():
            a("AchoJ's Wiki", href="/index.html", cls="wiki-header")
            with a(cls="home-button",href="/index.html"):
                img(src="/source/images/home.svg", title="home")
            with div(cls="dropdown"):
                img(src="/source/images/toc.svg")
                span(raw(toc_content), cls="dropdown-content", id="dropdownContent")
        with div(cls="content", id="md"):
            with div(cls="date"):
                span("post-time:" + post_date[0], cls="post-date")
                span("edit-time:" + edit_date[0], cls="edit-date")
            div(raw(html_content), cls="markdown-content")

    return doc

def write_html_to_file(doc, filename):
    """Write HTML content to file."""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(doc.render(pretty=True))

def generate_html_from_md(filename, output_folder):
    """Generate HTML from Markdown file."""
    md_content = read_markdown_file(filename)
    title, html_content, post_date, edit_date, tags, toc_content = convert_markdown_to_html(md_content)
    doc = create_html_document(html_content, post_date, edit_date, toc_content)
    html_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(filename))[0]}.html")
    write_html_to_file(doc, html_filename)
    return title, html_filename, tags, post_date, edit_date

def process_folder(input_folder, output_folder):
    """Process all Markdown files in a folder."""
    metadata_list = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".md"):
                print(file)
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, input_folder)
                output_path = os.path.join(output_folder, os.path.dirname(relative_path))
                os.makedirs(output_path, exist_ok=True)
                title, html_filename, tags, post_date, edit_date = generate_html_from_md(filepath, output_path)
                metadata_list.append({'filepath': filepath, 
                                      'html_filepath': html_filename, 
                                      'tags': tags, 
                                      'post_date': post_date, 
                                      'edit_date': edit_date,
                                      'title': title})
    return metadata_list

def generate_index(posts_list):
    """Generate index HTML file."""
    doc = dominate.document(title="Achoj's Wiki")
    with doc.head:
        meta(charset="utf-8")
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        title("Achoj's Wiki")
        link(rel="icon", href="/source/images/favicon.ico")
        link(rel="stylesheet", href="/source/styles.css")
        script(raw('''
            function openTab(evt, tabName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }
                tablinks = document.getElementsByClassName("tablinks");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }
                document.getElementById(tabName).style.display = "block";
                evt.currentTarget.className += " active";
            }'''))

    with doc:
        with header():
            a("AchoJ's Wiki", href="/index.html", cls="wiki-header")
            with a(cls="home-button",href="/index.html"):
                img(src="/source/images/home.svg", title="home")
        with div(cls="content", id="md"):
            with div(cls="avatar-area"):
                img(cls="avatar", src="/source/images/avatar.png", width="230px")
                with div(cls="avatar-content"):
                    div("AchoJ",cls="avatar-name")
                    p("Build the wiki with gpt")
                    p(raw("记录任何我想记录的东西"))
                    hr()
            div("文章",cls="post-title")
            with div(cls="tab-frame"):
                dominate.tags._input(type="radio",name="tab", id="tab1", checked="checked")
                label("时间排序", fr="tab1")
                dominate.tags._input(type="radio",name="tab", id="tab2")
                label("标签排序", fr="tab2")

                with div(cls="tab-content"):
                    temp_year, temp_month = '0', '0'
                    for item in posts_list:
                        html_filepath = item["html_filepath"].replace("\\", "/")
                        for post_date in item['post_date']:
                            match = re.match(r'(\d{4})\.(\d{2})\.(\d{2})', post_date)
                            if match:
                                year = match.group(1)
                                month = match.group(2)
                        if year != temp_year or month != temp_month:
                            temp_year = year
                            div(year + '-' + month, cls="post-tag")
                            temp_month = month
                        with div(cls="post-item", onclick="window.location.href='"+html_filepath+"'"):
                            span(item["title"], cls="post-name")
                            span(item["post_date"], cls="post-date")
                with div(cls="tab-content"):
                    tags = {}
                    for item in posts_list:
                        for tag in item['tags']:
                            if tag not in tags:
                                tags[tag] = []
                            tags[tag].append(item)
                
                    for tag, items in tags.items():  
                        div(tag,cls="post-tag")
                        for item in items:
                            html_filepath = item["html_filepath"].replace("\\", "/")
                            with div(cls="post-item", onclick="window.location.href='"+html_filepath+"'"):
                                span(item["title"], cls="post-name")
                                span(item["post_date"], cls="post-date")

        footer("Powered By Python&GPT")

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
