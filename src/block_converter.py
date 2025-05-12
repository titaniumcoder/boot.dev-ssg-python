from enum import Enum
import re

from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode

from inline_converter import text_node_to_html_node, text_to_textnodes

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
  split = markdown.split("\n\n")
  return [m.strip() for m in split if m.strip() != ""]

def block_to_block_type(block):
  if re.match(r"#{1,6} .+", block):
    return BlockType.HEADING

  if block.startswith("```") and block.endswith("```"):
    return BlockType.CODE

  lines = block.split("\n")

  if all(line.startswith(">") for line in lines):
    return BlockType.QUOTE

  if all(line.startswith("-") for line in lines):
    return BlockType.UNORDERED_LIST

  is_list = True
  for index in range(0, len(lines)):
    start_wanted = f"{index + 1}."
    if not lines[index].startswith(start_wanted):
      is_list = False
      break;
  
  if is_list:
    return BlockType.ORDERED_LIST

  return BlockType.PARAGRAPH

def convert_line_to_leafnode(line):
  textnodes = text_to_textnodes(line)
  return [text_node_to_html_node(textnode) for textnode in textnodes]

def convert_lines_to_leafnodes(lines):
  deep_nested = [convert_line_to_leafnode(line) for line in lines]
  return [x for xs in deep_nested for x in xs]

def convert_to_html_node(block):
  block_type = block_to_block_type(block)
  match block_type:
    case BlockType.HEADING:
      [(heading, text)] = re.findall(r"(#{1,6}) (.+)", block)
      heading_type = len(heading)
      return ParentNode(f"h{heading_type}", convert_lines_to_leafnodes([text]))
    case BlockType.PARAGRAPH:
      line = block.replace("\n", " ")
      return ParentNode("p", convert_lines_to_leafnodes([line]))
    case BlockType.QUOTE:
      line = " ".join([line[2:] for line in block.split("\n")])
      return ParentNode("blockquote", convert_lines_to_leafnodes([line]))
    case BlockType.UNORDERED_LIST:
      lines = [line[2:] for line in block.split("\n")]
      leafnodes = [ParentNode("li", [leafnode]) for leafnode in convert_lines_to_leafnodes(lines)]
      return ParentNode("ul", leafnodes)
    case BlockType.ORDERED_LIST:
      lines = [re.match(r"\d+\. (.*)", line).group(1) for line in block.split("\n")]
      leafnodes = [ParentNode("li", [leafnode]) for leafnode in convert_lines_to_leafnodes(lines)]
      return ParentNode("ol", leafnodes)
    case BlockType.CODE:
      return ParentNode("pre", [ParentNode("code", [LeafNode(None, block[4:-3])])]) 

    case _:
      raise Exception(f"Unexpected Blocktype: {block_type}")

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  children = [convert_to_html_node(block) for block in blocks]

  return ParentNode("div", children)

def filter_headings(block):
  return block_to_block_type(block) == BlockType.HEADING

def filter_header_1(lines):
  headers = []
  for line in lines:
    matches = re.findall(r"^# (.+)", line)
    if len(matches) > 0:
      headers.append(matches[0])
  return headers

def extract_title(markdown):
  # stupid because repetitive but I am lazy and performance
  # is not king. just scanning for '#' seems to be against 
  # my DRY feeling
  blocks = markdown_to_blocks(markdown)
  headings = []
  for block in blocks:
    if filter_headings(block):
      for text in filter_header_1([block]):
        headings.append(text)

  if len(headings) != 1:
    raise Exception("more than one heading")
  return headings[0]
