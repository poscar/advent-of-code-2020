class Node:
  def __init__(self, data):
    self.data = data
    self.next = None

  def __lt__(self, other):
    if isinstance(other, Node):
      return self.data < other.data
    return self.data < other

  def __le__(self, other):
    if isinstance(other, Node):
      return self.data <= other.data
    return self.data <= other

  def __gt__(self, other):
    if isinstance(other, Node):
      return self.data > other.data
    return self.data > other

  def __ge__(self, other):
    if isinstance(other, Node):
      return self.data >= other.data
    return self.data >= other

  def __eq__(self, other):
    if other == None:
      return False

    if isinstance(other, Node):
      return self is other

    return self.data == other

  def __ne__(self, other):
    if other == None:
      return True

    if isinstance(other, Node):
      return self is not other

    return self.data != other

  def __repr__(self):
    return self.data

  def __hash__(self):
    return self.data.__hash__()

  def __str__(self):
    return str(self.data)

class LinkedList:
  def __init__(self, data):
    self.dataToNode = {}
    self.head = None

    prevItem = None
    for item in data:
      node = Node(item)

      self.dataToNode[item] = node

      if self.head == None:
        self.head = node

      if prevItem != None:
        prevItem.next = node

      prevItem = node
    
    # Link the last and first nodes
    if prevItem != None:
      prevItem.next = self.head

  def getNodeWithData(self, data):
    return self.dataToNode[data]

  def __iter__(self):
    currNode = None

    if self.head != None:
      yield self.head
      currNode = self.head.next

    while currNode != self.head:
      yield currNode
      currNode = currNode.next

  def __repr__(self):
    nodes = []
    currNode = None

    if self.head != None:
      nodes.append(str(self.head))
      currNode = self.head.next

    while currNode != self.head:
      nodes.append(str(currNode))
      currNode = currNode.next

    return "->".join(nodes)