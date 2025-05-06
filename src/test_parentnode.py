import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
  def test_tag_none(self):
    node = ParentNode(None, [], None)
    self.assertRaises(ValueError, node.to_html)

  def test_children_none(self):
    node = ParentNode("a", None, None)
    self.assertRaises(ValueError, node.to_html)

  def test_children_empty(self):
    node = ParentNode("p", [], None)
    self.assertEqual("<p></p>", node.to_html())

  def test_children_empty_with_empty_props(self):
    node = ParentNode("p", [], {})
    self.assertEqual("<p></p>", node.to_html())

  def test_children_empty_with_one_prop(self):
    node = ParentNode("p", [], {"class": "parent"})
    self.assertEqual("<p class=\"parent\"></p>", node.to_html())

  def test_children_empty_with_multiple_prop(self):
    node = ParentNode("p", [], {"class": "parent", "title": "hover"})
    self.assertEqual("<p class=\"parent\" title=\"hover\"></p>", node.to_html())

  def test_with_one_child(self):
    node = ParentNode("p", [LeafNode("b", "a")])
    self.assertEqual("<p><b>a</b></p>", node.to_html())

  def test_with_multiple_children(self):
    node = ParentNode("p", [LeafNode("b", "a"), LeafNode("i", "b")])
    self.assertEqual("<p><b>a</b><i>b</i></p>", node.to_html())

  def test_nesting(self):
    node = ParentNode("p", [ParentNode("div", [LeafNode("b", "a")], {"class": "dd"}), LeafNode("i", "b")])
    self.assertEqual("<p><div class=\"dd\"><b>a</b></div><i>b</i></p>", node.to_html())

if __name__ == "__main__":
  unittest.main()

