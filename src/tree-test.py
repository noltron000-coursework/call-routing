from decimaltree import DecimalTreeNode
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
        # Attach left-left grandchild node
        node.next[0].next[5] = DecimalTreeNode(1)
        assert node.height() == 2
        # Attach right-right grandchild node
        node.next[9].next[5] = DecimalTreeNode(8)
        assert node.height() == 2
        # Attach right-right-left great-grandchild node
        node.next[9].next[5].next[7] = DecimalTreeNode(7)
        assert node.height() == 3
