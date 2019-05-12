# The reason for this tree to exit is to avoid unnecessary prefix checking if there are none
# Most of this code will be from binary tree class but with modification


class DecimalTreeNode(object):

    def __init__(self, data):
        """Initialize this decimal tree node with the given data."""
        self.data = data
        self.next = [None] * 10  # We can use the phone numbers as index to the child

    def __repr__(self):
        """Return a string representation of this decimal tree node."""
        return 'DecimalTreeNode({!r})'.format(self.data)

    def is_leaf(self):
        """Return True if this node is a leaf (has no children)."""
        return self.next == [None] * 10

    def is_branch(self):
        """Return True if this node is a branch (has at least one child)."""
        return self.next != [None] * 10

    def height(self):
        """Return the height of this node (the number of edges on the longest
           downward path from this node to a descendant leaf node).
           Best and worst case running time: O(n) where n is the number of nodes in the tree"""
        # Check if the node has a child or not
        if self.is_leaf():
            return 0

        ten_sides = [0] * 10

        for path in range(10):
            if self.next[path] is not None:
                ten_sides[path] += self.next[path].height()

        # Return one more than the greater of the left height and right height
        return max(ten_sides) + 1
