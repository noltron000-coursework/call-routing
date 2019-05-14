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


# Decimal Search tree configured to the call routing project

class DecimalSearchTree(object):

    def __init__(self, items=None):
        """Initialize this binary search tree and insert the given items."""
        self.root = DecimalTreeNode('+')
        # The inputted data will be a tuple = ("Carrier Name", (route number , route price))
        # Tree node data will be a tuple ("Carrier name", route price)
        self.size = 0
        # if items is not None:
        #     for item in items:
        #         self.insert(item)

    def __repr__(self):
        """Return a string representation of this binary search tree."""
        return 'DecimalSearchTree({} nodes)'.format(self.size)

    def is_empty(self):
        """Return True if this decimal search tree is empty (has no nodes)."""
        return self.root is None

    def height(self):
        """Return the height of this tree (the number of edges on the longest
           downward path from this tree's root node to a descendant leaf node).
           Best and worst case running time: O(n) where n is the number nodes in the tree"""
        return self.root.height()

    def contains(self, number):
        """Return True if this Decimal search tree contains a path at contains all the numbers.
        Best case running time: O(1) if the targeted item is in the root node
        Worst case running time: O(log10n) -> O(log n) since the search size is reduced by 10 % with each iteration
                                 n is the number of nodes in the tree"""
        # Find whether the tree has a path that contains all the numbers in order
        node = self._find_node_recursive(number, self.root)
        return node is not None

    def search(self, item):
        """Return an item in this decimal search tree matching the given item,
        or None if the given item is not found.
        Best case running time: O(1) if the targeted item is in the root node
        Worst case running time: O(log10n) -> O(log n) since the search size is reduced by 10 % with each iteration
                                 n is the number of nodes in the tree"""
        # Find a node with the given item, if any
        node = self._find_node_recursive(item, self.root)
        # node = self._find_parent_node_iterative(item)
        # Return the node's data if found, or None
        return node.data if node is not None else None

    # def insert(self, number, item):
    #     """Insert the given item in order into this binary search tree.
    #     Best case running time: O(1) is the tree is empty
    #     Worst case running time: O(log10n) since the program have to do binary search to find the parent node
    #                              n is the number of nodes in the tree"""
    #     new_node = DecimalTreeNode(item)
    #     # Handle the case where the tree is empty
    #     if self.is_empty():
    #         # Create a new root node
    #         self.root = new_node
    #         # Increase the tree size
    #         self.size += 1
    #         return
    #
    #     # Find the parent node of where the given item should be inserted
    #     parent = self._find_parent_node_recursive(item, self.root)  # Could be None if root doesn't have any child nodes
    #
    #     # Check if the given item should be inserted left of parent node
    #     if parent.data > item:
    #         # Create a new node and set the parent's left child
    #         parent.left = new_node
    #     # Check if the given item should be inserted right of parent node
    #     elif parent.data < item:
    #         # Create a new node and set the parent's right child
    #         parent.right = new_node
    #     # Increase the tree size
    #     self.size += 1

    def insert(self, number, data,  node):
        """TODO: Modify this code to the data type being passed in"""
        """Insert the number in order of the Decimal Search Tree recursively."""
        # Check if the number has done traversing
        if len(number) == 0:
            print(node.data)
            # Insert the data there aren't any
            if node.data is None:
                node.data = data
                self.size += 1
            # There are data, but check if it greater than the new data
            elif node.data > data:
                node.data = data
            return

        index = int(number[0])  # Use the first number of the string of numbers to decide where to go
        remainder = number[1:]  # Reduce the numbers string

        if node.next[index] is None:  # Signalling that there is no node at that index
            node.next[index] = DecimalTreeNode(None)   # Not putting the data here since there is still a remainder

        self.insert(remainder, data, node.next[index])  # Call recursively with the remainder and node at index


    def _find_parent_node_recursive(self, item, node, parent=None):
        """Return the parent node of the node containing the given item
        (or the parent node of where the given item would be if inserted)
        in this tree, or None if this tree is empty or has only a root node.
        Search is performed recursively starting from the given node
        (give the root node to start recursion)."""
        # Check if starting node exists
        if node is None:
            # Not found (base case)
            if parent:
                return parent
            else:
                return None
        #
        # # Check if the given item matches the node's data
        # if node.data == item:
        #     # Return the parent of the found node
        #     return parent
        # # Check if the given item is less than the node's data
        # for path in range(10):
        #     if node.next[path].data == item:
        #
        # elif node.data > item:
        #     # Recursively descend to the node's left child, if it exists
        #     return self._find_parent_node_recursive(item, node.left, node)
        # # Check if the given item is greater than the node's data
        # elif node.data < item:
        #     # Recursively descend to the node's right child, if it exists
        #     return self._find_parent_node_recursive(item, node.right, node)

    def _find_node_recursive(self, number, node):
        """Return the node containing the given item in this decimal search tree,
        or None if the given item is not found. Search is performed recursively
        starting from the given node (give the root node to start recursion).
        Best case running time: O(1) if the targeted item is in the root node
        Worst case running time: O(log10n) -> O(log n) since the search size is reduced by 10 % with each iteration"""

        if len(number) == 0:  # Signalling that the tree has a path that contains all the numbers
            return node.data

        next_index = int(number[0])  # Get the first of number to act as an index to the node.next array
        remainder = number[1:]  # Get rid of the first number string of numbers

        if node.next[next_index] is not None:  # Check if the node at the inputted number index is not None
            return self._find_node_recursive(remainder, node.next[next_index])  # Keep search until the remainder is 0
        else:  # Signalling that there is no more path that contains matching number
            return None


tree = DecimalSearchTree()
# Insert one item to the tree
tree.insert('00', 1, tree.root)
tree.insert('00', 0.3, tree.root)
child_node = tree.root.next[0]
print(tree)