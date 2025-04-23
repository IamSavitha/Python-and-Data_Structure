class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.left_node = None
        self.right_node = None
        self.parent = parent

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_node(data, self.root)

    def _insert_node(self, data, node):
        if data < node.data:
            if node.left_node is None:
                node.left_node = Node(data, node)
            else:
                self._insert_node(data, node.left_node)
        elif data > node.data:
            if node.right_node is None:
                node.right_node = Node(data, node)
            else:
                self._insert_node(data, node.right_node)

    def traverse_in_order(self):
        elements = []
        self._traverse_in_order(self.root, elements)
        return elements

    def _traverse_in_order(self, node, elements):
        if node:
            self._traverse_in_order(node.left_node, elements)
            elements.append(node.data)
            self._traverse_in_order(node.right_node, elements)

    def remove(self, data):
        if self.root:
            self.root = self._remove_node(data, self.root)

    def _remove_node(self, data, node):
        if not node:
            return node

        if data < node.data:
            node.left_node = self._remove_node(data, node.left_node)
            if node.left_node:
                node.left_node.parent = node
        elif data > node.data:
            node.right_node = self._remove_node(data, node.right_node)
            if node.right_node:
                node.right_node.parent = node
        else:
            if not node.left_node and not node.right_node:
                return None
            elif not node.left_node:
                return node.right_node
            elif not node.right_node:
                return node.left_node
            else:
                predecessor = self._get_predecessor(node.left_node)
                node.data = predecessor.data
                node.left_node = self._remove_node(predecessor.data, node.left_node)
                if node.left_node:
                    node.left_node.parent = node
        return node

    def _get_predecessor(self, node):
        current = node
        while current.right_node:
            current = current.right_node
        return current

    def get_min(self):
        if self.root is None:
            return None
        return self._get_min_value(self.root)

    def _get_min_value(self, node):
        current = node
        while current.left_node:
            current = current.left_node
        return current.data

    def get_max(self):
        if self.root is None:
            return None
        return self._get_max_value(self.root)

    def _get_max_value(self, node):
        current = node
        while current.right_node:
            current = current.right_node
        return current.data

    @staticmethod
    def build_tree(elements):
        bst = BST()
        for data in elements:
            bst.insert(data)
        return bst

if __name__ == "__main__":
    bst = BST()
    bst.insert(10)
    bst.insert(5)
    bst.insert(8)
    bst.insert(12)
    bst.insert(-5)
    bst.insert(44)
    bst.insert(-12)
    bst.insert(19)
    bst.insert(22)

    print("Before removal:", bst.traverse_in_order())
    bst.remove(10)
    print("After removal:", bst.traverse_in_order())

    print("Min value:", bst.get_min())
    print("Max value:", bst.get_max())
