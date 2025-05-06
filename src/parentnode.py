from htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props = None):
    super().__init__(tag, None, children, props)
  
  def to_html(self):
    if self.tag == None:
      raise ValueError("node needs a tag")

    if self.children == None:
      raise ValueError("node needs children")

    props_html = self.props_to_html()
    if props_html != "":
      tag = self.tag + " " + props_html
    else:
      tag = self.tag

    parent_html = [f"<{tag}>"]

    for child in self.children:
      parent_html.append(child.to_html())

    parent_html.append(f"</{self.tag}>")

    return "".join(parent_html)

  def __repr__(self):
    return f"ParentNode({self.tag}, {self.children}, {self.props})"
