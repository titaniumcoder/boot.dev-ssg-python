import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_value_none(self):
    leafnode = LeafNode("a", None, None)
    self.assertRaises(ValueError, leafnode.to_html)

  def test_leaf_to_html_p(self):
    leafnode = LeafNode("p", "Hello world!")
    self.assertEqual(leafnode.to_html(), "<p>Hello world!</p>")

  def test_leaf_to_html_a(self):
    leafnode = LeafNode("a", "The searchengine", {"href": "https://www.python.org", "target": "_blank"})
    self.assertEqual(leafnode.to_html(), "<a href=\"https://www.python.org\" target=\"_blank\">The searchengine</a>")

if __name__ == "__main__":
  unittest.main()

