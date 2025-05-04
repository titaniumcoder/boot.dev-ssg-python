import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
  def test_abstract(self):
    htmlnode = HTMLNode("a", "b", None, None)
    self.assertRaises(NotImplementedError, htmlnode.to_html)

  def test_props_to_html_for_none_works(self):
    htmlnode = HTMLNode("a", "b", None, None)
    self.assertEqual("", htmlnode.props_to_html())

  def test_props_to_html_for_none_works(self):
    htmlnode = HTMLNode("a", "b", None, {"a": "b", "c": "d"})
    self.assertEqual('a="b"c="d"', htmlnode.props_to_html())

if __name__ == "__main__":
  unittest.main()

