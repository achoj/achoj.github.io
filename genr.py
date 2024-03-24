import os
import re

def extract_info_from_filename(filepath):
    array = filepath.split('/')

    # 进一步分割每个元素以获取更多的子元素
    for i in range(len(array)):
        array[i] = array[i].split('_')

    year = array[1][0]
    month = array[2][0]
    day = array[2][1]
    name = array[2][2]
    file_type = array[2][3].split('.')[0]
    file_type = "programming" if file_type == "p" else "normal"
    date = f"{year}-{month}-{day}"
    return name, date, file_type

def generate_div(filepath, filename, file_type, date):
    print(filepath)
    div = f'<div class="post-item" path="{filepath}">\n' \
          f'    <span class="name">{filename}</span>\n' \
          f'    <span class="time">{date}</span>\n' \
          f'</div>'
    return div

def insert_div_to_index_html(div, file_type):
    # 读取index.html文件内容
    with open('index.html', 'r', encoding='utf-8') as file:
        index_content = file.read()

    # 定义要插入的位置和字符串
    if file_type == 'normal':
        insertion_point = '<div class="file-list" type="normal">'
    elif file_type == 'programming':
        insertion_point = '<div id="file-list" type="programming">'

    # 在内容中插入div
    index_content = index_content.replace(insertion_point, f"{insertion_point}\n{div}")

    # 将更新后的内容写回index.html文件
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(index_content)


def process_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            name, date, file_type = extract_info_from_filename(filepath)
            if name and date and file_type:
                div = generate_div(filepath, name, file_type, date)
                insert_div_to_index_html(div, file_type)

def remove_content_between_tags():
    # 读取index.html文件内容
    with open('index.html', 'r', encoding='utf-8') as file:
        index_content = file.read()

    # 定义要删除的起始和结束标记
    start_normal_tag = '<div class="file-list" type="normal">'
    end_normal_tag = '<!-- end of normal -->'
    start_programming_tag = '<div id="file-list" type="programming">'
    end_programming_tag = '<!-- end of programming -->'

    # 找到起始和结束标记的位置
    start_normal_index = index_content.find(start_normal_tag)
    end_normal_index = index_content.find(end_normal_tag)
    start_programming_index = index_content.find(start_programming_tag)
    end_programming_index = index_content.find(end_programming_tag)

    # 删除normal标记之间的内容
    if start_normal_index != -1 and end_normal_index != -1:
        index_content = index_content[:start_normal_index + len(start_normal_tag)] + index_content[end_normal_index:]

    # 删除programming标记之间的内容
    if start_programming_index != -1 and end_programming_index != -1:
        index_content = index_content[:start_programming_index + len(start_programming_tag)] + index_content[end_programming_index:]

    # 将更新后的内容写回index.html文件
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(index_content)

if __name__ == "__main__":
    remove_content_between_tags()
    process_files_in_directory("articles")
