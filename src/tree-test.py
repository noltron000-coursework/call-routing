from decimaltree import DecimalTreeNode, DecimalSearchTree
import unittest


class DecimalTreeTest(unittest.TestCase):

    def test_init(self):
        data = 12
        node = DecimalTreeNode(data)
        assert node.data == 12
        assert node.next == [None] * 10

    def test_is_leaf(self):
        # Create node with no children
        node = DecimalTreeNode(2)
        assert node.is_leaf() is True
        # Attach child node of index 0
        node.next[0] = DecimalTreeNode(1)
        assert node.is_leaf() is False
        # Attach child node at index 9
        node.next[9] = DecimalTreeNode(3)
        assert node.is_leaf() is False
        # Detach child node at index 0
        node.next[0] = None
        assert node.is_leaf() is False
        # Detach right child node
        node.next[9] = None
        assert node.is_leaf() is True

    def test_is_branch(self):
        # Create node with no children
        node = DecimalTreeNode(2)
        assert node.is_branch() is False
        # Attach child node at index 0
        node.next[0] = DecimalTreeNode(1)
        assert node.is_branch() is True
        # Attach child node at index 9
        node.next[9] = DecimalTreeNode(3)
        assert node.is_branch() is True
        # Detach child node at index 0
        node.next[0] = None
        assert node.is_branch() is True
        # Detach right child node
        node.next[9] = None
        assert node.is_branch() is False

    def test_height(self):
        # Create node with no children
        node = DecimalTreeNode(4)
        assert node.height() == 0
        # Attach child node at index 0
        node.next[0] = DecimalTreeNode(2)
        assert node.height() == 1
        # Attach child node at index 9
        node.next[9] = DecimalTreeNode(6)
        assert node.height() == 1
        # Attach grandchild node to node at index 0 of the root node
        node.next[0].next[5] = DecimalTreeNode(1)
        assert node.height() == 2
        # Attach grandchild node to the node at index 9 of the root
        node.next[9].next[5] = DecimalTreeNode(8)
        assert node.height() == 2
        # Attach great-grandchild node
        node.next[9].next[5].next[7] = DecimalTreeNode(7)
        assert node.height() == 3


class DecimalSearchTreeTest(unittest.TestCase):

    def test_init(self):
        tree = DecimalSearchTree()
        assert tree.root.data == "+"
        assert tree.size == 0

    def test_insert(self):
        tree = DecimalSearchTree()
        # Insert one item to the tree
        tree.insert('0', 1, tree.root)
        assert tree.size == 1
        assert tree.height() == 1
        child = tree.root.next[0]
        assert child is not None
        assert child.data == 1
        # Insert a grandchild
        tree.insert('01', 3, tree.root)
        assert child.next[1] is not None
        assert child.next[1].data == 3
        assert tree.height() == 2

    def test_inserting_lower_price(self):
        tree = DecimalSearchTree()
        # Insert one item to the tree
        tree.insert('00', 1, tree.root)
        tree.insert('00', 0.3, tree.root)
        child_node = tree.root.next[0]
        assert child_node.next[0].data == 0.3

