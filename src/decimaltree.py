# The reason for this tree to exit is to avoid unnecessary prefix checking if there are none
# Most of this code will be from binary tree class but with modification

# There code were heavily inspired by SW Harrison's implementation of a Decimal Search Tree
# Thank you to him for taking the time to explain this data structure.

class DecimalTreeNode(object):
    def __init__(self, data):
        """
        Initialize a decimal tree node with the given data.
        """
        # the difference between binary and decimal trees:
        # - binary trees have 2 children.
        # - decimal trees have 10 children.
        # - n-ary trees have n children.

        # like a binary tree, each node has a data point.
        self.data = data

        # rather than having left & right pointers:
        # - we have an array that always has a length 10.
        # - the array's nth item represents the nth decimal.
        # - each item is one of the node's children.
        self.next = [None] * 10
        # NOTE: the root node represents a 0-length number.


    def __repr__(self):
        """
        Visually represent this node using a string.
        Return the string.
        """
        return 'DecimalTreeNode({!r})'.format(self.data)


    def is_leaf(self):
        """
        Check if this node is a leaf (has no children).
        Return True or False based on result.
        """
        return self.next == [None] * 10


    def is_branch(self):
        """
        Check if this node is a branch (has any children).
        Return True or False based on result.
        """
        return self.next != [None] * 10


    def height(self):
        """
        Return the height of this node.
        The height is the number edges on the path to get
        to the lowest descendant leaf node possible.
        If this node itself is a leaf, it has a height of 0.
        The height of a non-existant node (NoneType) is 0.
        ~~~
        best & worst case time complexity: O(n)
        --> we must traverse every node to find the height.
        """
        # check if the node has a child or not.
        if self.is_leaf():
            return 0

        # track the height of our tallest child.
        tallest_child = 0

        # we need to check each and every child's height.
        for child in self.next:
            # measure this child's height.
            child_height = child.height()
            # if this child is really tall, track it.
            if child_height > tallest_child:
                tallest_child = child_height

        # add 1 to include this node in the height tracker.
        return tallest_child + 1


# Decimal Search tree configured to the call routing project
class DecimalSearchTree(object):

    def __init__(self, items=None):
        """Initialize this binary search tree and insert the given items."""
        self.root = DecimalTreeNode('+')
        # The inputted data will be a tuple = ("Carrier Name", (route number , route price))
        # Tree node data will be a tuple ("Carrier name", route price)
        self.size = 0
        # What is items going to be? []
        # if items is not None:
        #     for item in items:

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

    def insert(self, number, data):
        self._insert(number, data, self.root)

    def _insert(self, number, data,  node):
        """TODO: Modify this code to the data type being passed in"""
        """Insert the number in order of the Decimal Search Tree recursively."""
        # Check if the number has done traversing
        if len(number) == 0:
            # Insert the data there aren't any
            if node.data is None:
                node.data = data
                self.size += 1
            # There are data, but check if it greater than the new data
            elif node.data[1] > data[1]:  # Data will be (carrier name, price)
                node.data = data
            return

        index = int(number[0])  # Use the first number of the string of numbers to decide where to go
        remainder = number[1:]  # Reduce the numbers string

        if node.next[index] is None:  # Signalling that there is no node at that index
            node.next[index] = DecimalTreeNode(None)   # Not putting the data here since there is still a remainder

        self._insert(remainder, data, node.next[index])  # Call recursively with the remainder and node at index

    def _find_node_recursive(self, number, node):
        """Return the node containing the given item in this decimal search tree,
        or None if the given item is not found. Search is performed recursively
        starting from the given node (give the root node to start recursion).
        Best case running time: O(1) if the targeted item is in the root node
        Worst case running time: O(log10n) -> O(log n) since the search size is reduced by 10 % with each iteration"""

        if len(number) == 0:  # Signalling that the tree has a path that contains all the numbers
            return node

        next_index = int(number[0])  # Get the first of number to act as an index to the node.next array
        remainder = number[1:]  # Get rid of the first number string of numbers

        if node.next[next_index] is not None:  # Check if the node at the inputted number index is not None
            return self._find_node_recursive(remainder, node.next[next_index])  # Keep search until the remainder is 0
        else:  # Signalling that there is no more path that contains matching number
            return None

    def find_prices(self, number):
        """Find the longest matching prefix of a number and get its price and carrier"""
        return self._find_prices(number, self.root)

    def _find_prices(self, number, node, data=None):
        """Find the longest matching prefix of a number and get its price and carrier"""

        current = data
        if len(number) == 0:
            return current

        next_index = int(number[0])
        remainder = number[1:]

        if node.next[next_index] is not None:
            next_node = node.next[next_index]
            if next_node.data is not None:
                if current is not None:
                    if next_node.data[1] < current[1]:
                        return self._find_prices(remainder, next_node, next_node.data)
                    else:
                        return self._find_prices(remainder, next_node, current)
                else:
                    return self._find_prices(remainder, next_node, next_node.data)
            else:
                return self._find_prices(remainder, next_node, current)
        else:
            return current
