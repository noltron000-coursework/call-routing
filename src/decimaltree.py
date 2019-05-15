# The reason for this tree to exit is to avoid unnecessary prefix checking if there are none
# Most of this code will be from binary tree class but with modification

# There code were heavily inspired by SW Harrison's implementation of a Decimal Search Tree
# Thank you to him for taking the time to explain this data structure.

class DecimalTreeNode(object):
    def __init__(self, data=None):
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
        return f'DecimalTreeNode({self.data!r})'


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


# Decimal Search tree configured to the call routing project.
class DecimalSearchTree(object):
    def __init__(self, items=None):
        """
        Initialize search tree with given items.
        """
        self.root = DecimalTreeNode('+') 
        # HACK maybe we can remove the '+' as a value. We can assume it starts at '+'.
        # XXX reword these comments below.
        # The inputted data will be a tuple = ("Carrier Name", (route number , route price))
        # Tree node data will be a tuple ("Carrier name", route price)

        self.size = 0
        # What is items going to be? []
        # if items is not None:
        #     for item in items:


    def __repr__(self):
        """
        Visually represent this tree using a string.
        Return the formatted string.
        """
        return f'DecimalSearchTree({self.size} nodes)'


    def is_empty(self):
        """
        Check if there are literally no nodes in this tree.
        Return True or False based on result.
        """
        return self.root is None


    def height(self):
        """
        Return the height of the root node.
        ~~~
        best & worst case time complexity: O(n)
        --> same complexity as referenced method.
        """
        return self.root.height()


    def contains(self, number): 
        # FIXME contains is not semantic. 
        # node_exists() would be more meaningful.
        # contains() implies it contains data.
        # we could write another function for contains()...
        # in this modified tree, the data is a price.
        # finding a price is not usually what we want to do.
        # we want to find the phone number.
        # this is represented by its path.
        """
        Does this search tree have the given path?
        - Yes! Return True; the item is found.
        - No! Return False; the item is not found.
        ---
        best case runtime: O(1)
        --> the root node contains our item.
        ---
        median case runtime: O(ln(n))
        --> the item is a leaf in a balanced tree.
        ---
        worst case runtime: O(n)
        --> the tree can be represented using a linked list.
            the item is at the tail of the linked list.
        """
        # find a node with a certain path, if it exists.
        # the node must contain data to be valid.
        # the node's path is determined by the given number.
        node = self._find_node_recursive(number, self.root)

        # return True if the node is found, or False if not.
        return node is not None


    def search(self, item):
        """
        Does this search tree contain the given item?
        - Yes! Return our Node; the item's container.
        - No! Return None; item does not exist in any node.
        ---
        best case runtime: O(1)
        --> the root node contains our item.
        ---
        median case runtime: O(ln(n))
        --> the item is a leaf in a balanced tree.
        ---
        worst case runtime: O(n)
        --> the tree can be represented using a linked list.
            the item is at the tail of the linked list.
        """
        # find a node with the given item, if any
        node = self._find_node_recursive(item, self.root)
        # return the node if it is found, or None if not.
        return node.data if node is not None else None

        # HACK it seems we are returning a node's data:
        # - it would be best if we returned the node itself.
        # - this would allow for a more versatile function.
        # - also the return line makes my eyes cross!
        #   it has too much going on, break apart.


    def insert(self, phone, data, node='ROOT'):
        """
        insert a phone number into this tree.
        its data is the carrier price.
        we might have to generate a sequence of empty nodes.
        these empty nodes still have semantic meaning.
        TODO improve docstring
        ~~~
        best case runtime: O(XXX)
        --> XXX
        ---
        median case runtime: O(XXX)
        --> XXX
        ---
        worst case runtime: O(XXX)
        --> XXX

        TODO: Modify this code to the data type being passed in.
        Insert the phone# in order of the Decimal Search Tree recursively.
        """
        # do we start at the root node?
        if node == 'ROOT':
            node = self.root

        # check whether our phone# is an empty string.
        # that would mean the node is our injection site!
        if not phone:
            # now inject data at our node.
            # first ensure there is no data at our node.
            if node.data is None:
                node.data = data
                self.size += 1

            # data will be (carrier name, price)
            # - HACK: would it not make more sense to use.
            # - a dictionary for data? {carrier name: price}
            # if there is already data, keep the lower one!
            elif node.data[1] > data[1]:
                node.data = data

        else:
            # find digit.
            digit = int(phone[0])
            # remove digit from phone# string.
            phone = phone[1:]

            # check if next node exists.
            if node.next[digit] is None:
                # initialize empty node and point to it.
                node.next[digit] = DecimalTreeNode()

            # recursively call insert here.
            # - use remaining phone number,
            # - the same data,
            # - and the next node determined by this digit.
            self.insert(phone, data, node.next[digit])

    def _find_node_recursive(self, number, node):
        """
        Return the node containing the given item in this decimal search tree,
        or None if the given item is not found. Search is performed recursively
        starting from the given node (give the root node to start recursion).
        Best case running time: O(1) if the targeted item is in the root node
        Worst case running time: O(log10n) -> O(log n) since the search size is reduced by 10 % with each iteration
        """

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
