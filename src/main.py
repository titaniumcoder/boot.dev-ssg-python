from textnode import TextNode, TextType

from block_converter import markdown_to_html_node, extract_title

import os, shutil, sys

def main():
  basepath = '/'
  if len(sys.argv) > 0:
    basepath = sys.argv[1]
  copy_files("static", "docs")
  generate_pages("content", "template.html", "docs", basepath)

def copy_files(src, dest):
  # recursively delete files from dest
  clean_dir(dest)
  # create directory if not exists
  make_dir(dest)
  # recursively copy files from src to dest
  copy_dir(src, dest)

def clean_dir(dir):
  if not os.path.exists(dir):
    return
  
  shutil.rmtree(dir)

def make_dir(dir):
  if os.path.exists(dir):
    return

  os.mkdir(dir)

def copy_dir(src, dest):
  content = os.listdir(src)
  for content in os.listdir(src):
    fullname = os.path.join(src, content)
    if os.path.isdir(fullname):
      target_dir = os.path.join(dest, content)
      os.mkdir(target_dir)
      copy_dir(fullname, target_dir)
    if os.path.isfile(fullname):
      shutil.copy(fullname, dest)

def generate_pages(from_path, template_path, dest_path, basepath):
  for content in os.listdir(from_path):
    fullname = os.path.join(from_path, content)
    if os.path.isdir(fullname):
      target_dir = os.path.join(dest_path, content)
      os.mkdir(target_dir)
      generate_pages(fullname, template_path, target_dir, basepath)
    if os.path.isfile(fullname):
      target_path, ext = os.path.splitext(os.path.join(dest_path, content))
      generate_page(fullname, template_path, target_path + ".html", basepath)

def generate_page(from_path, template_path, dest_path, basepath):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")

  markdown_file = open(from_path)
  markdown = markdown_file.read()
  markdown_file.close()

  html_content = markdown_to_html_node(markdown).to_html()
  title = extract_title(markdown)

  template_file = open(template_path)
  template = template_file.read()
  template_file.close()

  template = template.replace("{{ Content }}", html_content)
  template = template.replace("{{ Title }}", title)
  template = template.replace("href=\"/", f"href=\"{basepath}")
  template = template.replace("src=\"/", f"src=\"{basepath}")

  os.makedirs(os.path.dirname(dest_path), exist_ok=True)

  dest_file = open(dest_path, "w")
  dest_file.write(template)
  dest_file.flush()
  dest_file.close()

if __name__ == "__main__":
  main()
