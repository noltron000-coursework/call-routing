# This tree exists to avoid unnecessary prefix checking.
# Most of this code is modified from the binary tree class.
# This code is inspired by SW Harrison's implementations.
# Thank him for taking time to explain this data structure!

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
        return f"DecimalTreeNode({self.data!r})"


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
            # measure this child's height, if it exists.
            if child:
                child_height = child.height()
            else:
                child_height = 0

            # if this child is really tall, track it.
            if child_height > tallest_child:
                tallest_child = child_height

        # add 1 to include this node in the height tracker.
        return tallest_child + 1


class DecimalSearchTree(object):
    def __init__(self, items=None):
        """
        Initialize search tree with given items.
        """
        # the root node will always be empty.
        self.root = DecimalTreeNode()
        self.size = 0
        # insert items
        if items is not None:
            for item in items:
                self.insert(item)

        # a node's item will be a tuple.
        # (carrier name, (route number, route price))
        # HACK: maybe change the item type semantically.

        # the input item is a list of tuples.
        # [(carrier name, (route number, route price)),...]
        # HACK: maybe make it a dictionary instead of tuple.

        # items is all the routes.
        # we traverse the route tree with our numbers.
        # TODO: initialize with item(s).

    def __repr__(self):
        """
        Visually represent this tree using a string.
        Return the formatted string.
        """
        return f"DecimalSearchTree({self.size} nodes)"


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
        '''
        Does this search tree contain the given item?
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
        '''
        # find a node with the given item, if any.
        node = self._find_path_recursive(number, self.root)
        # return True if it is found, or False if not.
        return node is not None


    def search(self, item):
        """
        Does this search tree contain the given item?
        - Yes! Return our Node; the item's container.
        - No! Return None; item does not exist in any node.
        ~~~
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
        # find a node with the given item, if any.
        node = self._find_path_recursive(item, self.root)
        # return the node if it is found, or None if not.
        return node.data if node is not None else None

        # HACK it seems we are returning a node's data:
        # - it would be best if we returned the node itself.
        # - this would allow for a more versatile function.
        # - also the return line makes my eyes cross!
        #   it has too much going on, break apart.


    def insert(self, phone, data, node="ROOT"):
        """
        insert a given {phone:item} pair into this tree.
        this function uses recursion.
        traverse the tree using the phone number.
        this leads to the node we need to inject with data.
        we might have to generate a sequence of empty nodes.
        these empty nodes still have semantic meaning.
        the tree must maintain a strict sorted structure.
        ---
        best case runtime: O(1)
        --> the root node is our parent node.
        ---
        median case runtime: O(ln(n))
        --> our parent node is a leaf in a balanced tree.
        ---
        worst case runtime: O(n)
        --> the tree can be represented using a linked list.
            our parent node is the tail of the linked list.
        """
        # check if we start at the root node.
        if node == "ROOT":
            node = self.root

        # check whether our phone# is an empty string.
        # that would mean the node is our injection site!
        if not phone:
            # now inject data at our node.
            # first ensure there is no data at our node.
            if node.data is None:
                node.data = data
                self.size += 1

            # data will be (carrier name, price).
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
            # grab our next node.
            next = node.next[digit]

            # check if next node exists.
            if next is None:
                # initialize empty node and point to it.
                next = DecimalTreeNode()

            # recursively call insert here.
            # - use remaining phone number,
            # - the same data,
            # - and the next node determined by this digit.
            self.insert(phone, data, next)


    def _find_path_recursive(self, phone, node="ROOT"):
        """
        find a node by following a given path, & return it.
        the path is equal to the given phone number.
        traverse tree recursively starting at a given node.
        ~~~
        best case runtime: O(1)
        --> the root node is our parent node.
        ---
        median case runtime: O(ln(n))
        --> our parent node is a leaf in a balanced tree.
        ---
        worst case runtime: O(n)
        --> the tree can be represented using a linked list.
            parent node is at the tail of the linked list.
        """
        # check if we start at the root node.
        if node == "ROOT":
            node = self.root

        # if node is None, the path is a dead-end.
        if node is None:
            return None

        # check whether our phone# is an empty string.
        # that would mean we have found our node!
        elif not phone:
            return node

        else:
            # find digit.
            digit = int(phone[0])
            # remove digit from phone# string.
            phone = phone[1:]
            # grab our next node.
            next = node.next[digit]

            # recursively call find_path here.
            # - use remaining phone number,
            # - and the next node determined by this digit.
            return self._find_path_recursive(phone, next)


    def get_price(self, phone, node="ROOT", best_data=None):
        """
        Find the longest matching prefix of a phone number.
        We traverse this tree recursively.
        Return its price and carrier.
        """
        # check if we start at the root node.
        if node=="ROOT":
            node=self.root

        # if node is None, the path is a dead-end.
        # return the last data that we found.
        if node is None:
            return best_data

        # check whether our phone# is an empty string.
        # that would mean we have found our node!
        elif not phone:
            return best_data

        else:
            # find digit.
            digit = int(phone[0])
            # remove digit from phone# string.
            phone = phone[1:]
            # grab our next node.
            next = node.next[digit]

            # if the next node has data,
            # it might be better than our best_data.
            # lets peek inside and check.
            if node.data:
                # our best_data could still be None here.
                # this happens when we don't find any data,
                # even if we traversed a few nodes yet.
                # in this case we grab the nodes data.
                if not best_data:
                    # the node's data could still be None!
                    # this represents a waypoint node;
                    # its an expected result.
                    return self.get_price(
                        phone, next, node.data)

                # if the node's data is better,
                # replace our best_data with it.
                elif node.data[1] < best_data[1]:
                    return self.get_price(
                        phone, next, node.data)

                # leave our best_data alone if we didn't
                # find better data in the node.
                elif node.data[1] >= best_data[1]:
                    return self.get_price(
                        phone, next, best_data)

            # node.data doesn't have to exist.
            # this happens often; it represents a waypoint.
            # in this case we continue to the next node,
            # but make no changes to our best_data.
            else:
                return self.get_price(
                    phone, next, best_data)
