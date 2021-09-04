class Node:
	""""""
	def __init__(self, value, parent=None):
		self.parent = parent
		self.value = value
		self.left = None
		self.right = None

	def add(self, new_value) -> None:
		"""Adding new child node"""
		if new_value < self.value:
			if self.left is None:
				self.left = Node(new_value, self)
			else:
				self.left.add(new_value)
		else:
			if self.right is None:
				self.right = Node(new_value, self)
			else:
				self.right.add(new_value)

	def find_min(self):
		"""Get minimum node in a subtree."""
		current = self
		while current.left_child:
			current_node = current_node.left_child
		return current

	def find_max(self):
		"""Get maximum node in a subtree."""
		current = self
		while current.right:
			current = current.right
		return current

	def replace_node_in_parent(self, new_node=None) -> None:
		if self.parent:
			if self == self.parent.left_child:
				self.parent.left_child = new_node
			else:
				self.parent.right_child = new_node
		if new_node:
			new_node.parent = self.parent


class Tree:
	""" Initialisation of binary tree
		from non query type (int, float, char) or list"""
	def __init__(self, value):
		if type(value) is list:
			self.root = Node(value[0])
			for _ in value[1:]:
				self.add(_)
		else:
			self.root = Node(value)

	def add(self, new_value) -> None:
		"""Adding new element into the tree"""
		self.root.add(new_value)

	def is_member(self, search_value) -> bool:
		return is_element(self.root, search_value)

	def find_min(self):
		"""Get minimum node in a tree."""
		return self.root.find_min()

	def find_max(self):
		"""Get maximum node in a tree."""
		return self.root.find_max()

	def binary_tree_delete(self, key) -> None:
		if key < self.key:
			self.left_child.binary_tree_delete(key)
			return
		if key > self.key:
			self.right_child.binary_tree_delete(key)
			return
		if self.left_child and self.right_child:
			successor = self.right_child.find_min()
			self.key = successor.key
			successor.binary_tree_delete(successor.key)
		elif self.left_child:
			self.replace_node_in_parent(self.left_child)
		elif self.right_child:
			self.replace_node_in_parent(self.right_child)
		else:
			self.replace_node_in_parent(None)


def is_element(object, search_value):
		if object.value == search_value:
			return True
		else:
			if search_value > object.value and (object.right is not None):
				return is_element(object.right, search_value)
			elif object.left is not None:
				return is_element(object.left, search_value)
			else:
				return False


t = Tree([7,4,9,1,5])
t.add(6)
t.add(2)
t.add(12)
print(t.find_max().value)