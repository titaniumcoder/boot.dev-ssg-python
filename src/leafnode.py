from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props = None):
    super().__init__(tag, value, None, props)
  
  def to_html(self):
    if self.value == None:
      raise ValueError("Node needs a value")

    if self.tag == None:
      return self.value

    props_html = self.props_to_html()
    if props_html != "":
      tag = self.tag + " " + props_html
    else:
      tag = self.tag

    return f"<{tag}>{self.value}</{self.tag}>"

  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value})"
