class HTMLNode:
  def __init__(self, tag = None, value = None, children = None, props = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError()

  def props_to_html(self):
    if self.props == None:
      return ""

    html = []
    for k in self.props:
      html.append(f"{k}=\"{self.props[k]}\"")
    return " ".join(html)

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
