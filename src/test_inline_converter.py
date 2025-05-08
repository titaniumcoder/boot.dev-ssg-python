import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType

from inline_converter import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineConverter(unittest.TestCase):
  def test_unknown(self):
    node = TextNode("mytext", "something")
    self.assertRaises(Exception, text_node_to_html_node, node)

  def test_text(self):
    node = TextNode("text", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "text")

  def test_bold(self):
    node = TextNode("text", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "text")

  def test_italic(self):
    node = TextNode("text", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "text")

  def test_code(self):
    node = TextNode("text", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "text")

  def test_link(self):
    node = TextNode("text", TextType.LINK, "https://www.python.org")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "text")
    self.assertEqual(html_node.props, {"href": "https://www.python.org"})

  def test_image(self):
    node = TextNode("text", TextType.IMAGE, "https://img.com/i.png")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, None)
    self.assertEqual(html_node.props, {"src": "https://img.com/i.png", "alt": "text"})

  def test_split_empty(self):
    nodes = split_nodes_delimiter([], "b", TextType.BOLD)
    self.assertEqual(nodes, [])

  def test_split_node_not_available(self):
    nodes = split_nodes_delimiter([TextNode("text", TextType.TEXT)], "b", TextType.BOLD)
    self.assertEqual(nodes, [TextNode("text", TextType.TEXT)])

  def test_split_node_available(self):
    nodes = split_nodes_delimiter([TextNode("text *bbb* and *bb* and _i_", TextType.TEXT)], "*", TextType.BOLD)
    self.assertEqual(nodes, [
      TextNode("text ", TextType.TEXT),
      TextNode("bbb", TextType.BOLD),
      TextNode(" and ", TextType.TEXT),
      TextNode("bb", TextType.BOLD),
      TextNode(" and _i_", TextType.TEXT),
    ])

  def iter_to_list(self, match_iter):
    return list(map(lambda m: (m.group(1), m.group(2)), match_iter))

  def test_extract_markdown_images_no_image(self):
    images = self.iter_to_list(extract_markdown_images("no image"))
    self.assertListEqual([], images)

  def test_extract_markdown_images_one_image(self):
    images = self.iter_to_list(extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    ))
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], images)

  def test_extract_markdown_images_two_image(self):
    images = self.iter_to_list(extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and  ![another image](https://i.imgur.com/zjjcJKX.png)"
    ))
    self.assertListEqual([
      ("image", "https://i.imgur.com/zjjcJKZ.png"),
      ("another image", "https://i.imgur.com/zjjcJKX.png")
    ], images)

  def test_extract_markdown_links_no_links(self):
    links = self.iter_to_list(extract_markdown_links("no link"))
    self.assertListEqual([], links)

  def test_extract_markdown_links_two_links(self):
    links = self.iter_to_list(extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    ))
    self.assertListEqual([
      ("to boot dev", "https://www.boot.dev"), 
      ("to youtube", "https://www.youtube.com/@bootdotdev")
    ], links)

  def test_extract_markdown_links_no_images(self):
    links = self.iter_to_list(extract_markdown_links(
        "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
    ))
    self.assertListEqual([], links)

  def test_split_links_no_link(self):
    node = TextNode(
        "This is text with no links at all",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with no links at all", TextType.TEXT),
        ],
        new_nodes,
    )    

  def test_split_links_two_link(self):
    node1 = TextNode(
        "This is text with no link at all",
        TextType.TEXT,
    )
    node2 = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    node3 = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node1, node2, node3])
    self.assertListEqual(
        [
            TextNode("This is text with no link at all", TextType.TEXT),
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )    

  def test_split_links_two_links_ending(self):
    node = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png).",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(".", TextType.TEXT),
        ],
        new_nodes,
    )    
  def test_split_images_no_images(self):
    node = TextNode(
        "This is text with no images at all",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with no images at all", TextType.TEXT),
        ],
        new_nodes,
    )    

  def test_split_images_two_images(self):
    node1 = TextNode(
        "This is text with no images at all",
        TextType.TEXT,
    )
    node2 = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    node3 = TextNode(
        "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node1, node2, node3])
    self.assertListEqual(
        [
            TextNode("This is text with no images at all", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ],
        new_nodes,
    )    

  def test_split_images_two_images_ending(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png).",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode(".", TextType.TEXT),
        ],
        new_nodes,
    )    

  def test_text_to_textnodes(self):
    new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    self.assertListEqual(
      [
          TextNode("This is ", TextType.TEXT),
          TextNode("text", TextType.BOLD),
          TextNode(" with an ", TextType.TEXT),
          TextNode("italic", TextType.ITALIC),
          TextNode(" word and a ", TextType.TEXT),
          TextNode("code block", TextType.CODE),
          TextNode(" and an ", TextType.TEXT),
          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
          TextNode(" and a ", TextType.TEXT),
          TextNode("link", TextType.LINK, "https://boot.dev"),
      ], new_nodes)

if __name__ == "__main__":
  unittest.main()

