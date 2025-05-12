import re

from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(textnode):
  match textnode.text_type:
    case TextType.TEXT:
      return LeafNode(None, textnode.text)
    case TextType.BOLD:
      return LeafNode("b", textnode.text)
    case TextType.ITALIC:
      return LeafNode("i", textnode.text)
    case TextType.CODE:
      return LeafNode("code", textnode.text)
    case TextType.LINK:
      return LeafNode("a", textnode.text, {"href": textnode.url})
    case TextType.IMAGE:
      return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})

    case _:
      raise Exception("unknown text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  result = []
  for old_node in old_nodes:
    text = old_node.text
    splitted_node_text = text.split(delimiter)
    for i in range(0, len(splitted_node_text)):
      if i % 2 == 0:
        result.append(TextNode(splitted_node_text[i], old_node.text_type, old_node.url))
      else:
        result.append(TextNode(splitted_node_text[i], text_type))
  
  return result

def extract_markdown_images(text):
  regex = r"\!\[(.*?)\]\((.*?)\)"
  return re.finditer(regex, text)

def extract_markdown_links(text):
  regex = r"(?<!\!)\[(.*?)\]\((.*?)\)"
  return re.finditer(regex, text)

def split_nodes_image(old_nodes):
  result = []
  for old_node in old_nodes:
    text = old_node.text
    images = [(m.start(), m.end(), TextNode(m.group(1), TextType.IMAGE, m.group(2))) for m in extract_markdown_images(text)][::-1]
    if len(images) == 0:
      result.append(old_node)
    else:
      nodes = []
      for image in images:
        if image[1] != len(text):
          nodes.append(TextNode(text[image[1]:], old_node.text_type, old_node.url))
        text = text[:image[0]]
        nodes.append(image[2])
      if text != "":
        nodes.append(TextNode(text, old_node.text_type, old_node.url))
      result += nodes[::-1]
  return result

def split_nodes_link(old_nodes):
  result = []
  for old_node in old_nodes:
    text = old_node.text
    links = [(m.start(), m.end(), TextNode(m.group(1), TextType.LINK, m.group(2))) for m in extract_markdown_links(text)][::-1]
    if len(links) == 0:
      result.append(old_node)
    else:
      nodes = []
      for link in links:
        if link[1] != len(text):
          nodes.append(TextNode(text[link[1]:], old_node.text_type, old_node.url))
        text = text[:link[0]]
        nodes.append(link[2])
      if text != "":
        nodes.append(TextNode(text, old_node.text_type, old_node.url))
      result += nodes[::-1]
  return result

def text_to_textnodes(text):
  r1 = split_nodes_image([TextNode(text, TextType.TEXT)])
  r2 = split_nodes_link(r1)
  r3 = split_nodes_delimiter(r2, "**", TextType.BOLD)
  r4 = split_nodes_delimiter(r3, "_", TextType.ITALIC)
  return split_nodes_delimiter(r4, "`", TextType.CODE)
