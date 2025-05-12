import unittest

from block_converter import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestBlockConverter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_code(self):
      block = "```Ich bin wilder Code ```mit Inhalt ```"
      self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_blocktype_heading(self):
      self.assertEqual(BlockType.HEADING, block_to_block_type("# H1"))
      self.assertEqual(BlockType.HEADING, block_to_block_type("## H2"))
      self.assertEqual(BlockType.HEADING, block_to_block_type("### H3"))
      self.assertEqual(BlockType.HEADING, block_to_block_type("#### H4"))
      self.assertEqual(BlockType.HEADING, block_to_block_type("##### H5"))
      self.assertEqual(BlockType.HEADING, block_to_block_type("###### H6"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("####### H7"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("#"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("#1"))

    def test_blocktype_blockquote(self):
      self.assertEqual(BlockType.QUOTE, block_to_block_type("> a\n>b\n>c"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("> a\nb\n>c"))

    def test_blocktype_unordered(self):
      self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type("- a\n- b\n- c"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("- a\nb\n- c"))

    def test_blocktype_ordered(self):
      self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type("1. a\n2. b\n3. c"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("1 a\n3. b\n2. c"))
      self.assertEqual(BlockType.PARAGRAPH, block_to_block_type("1. a\nb\n2. c"))

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

###### Heading 6

####### Heading 7
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h6>Heading 6</h6><p>####### Heading 7</p></div>",
        )

    def test_blockquote(self):
        md = """
> Ich bin ein Berliner
> Oder so ähnlich

> Make America great again
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Ich bin ein Berliner Oder so ähnlich</blockquote><blockquote>Make America great again</blockquote></div>",
        )

    def test_lists(self):
        md = """
- Unordered List 1
- Unordered List 2

1. Ordered List 1
2. Ordered List 2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Unordered List 1</li><li>Unordered List 2</li></ul><ol><li>Ordered List 1</li><li>Ordered List 2</li></ol></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extract_title_success(self):
        md = """
# I am the page header
"""

        title = extract_title(md)
        self.assertEqual(
            title,
            "I am the page header",
        )

    def test_extract_title_missing(self):
        md = """
> I have no title
"""
        self.assertRaises(Exception, extract_title, md)

    def test_extract_title_failure(self):
        md = """
# Title 1

# Title 2
"""
        self.assertRaises(Exception, extract_title, md)
