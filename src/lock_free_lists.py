from order_node import OrderNode

class LockFreeFIFOLinkedList:
    """A lock-free FIFO linked list for storing Buy orders."""

    def __init__(self):
        self.head = None  # head pointer
        self.tail = None  # tail pointer

    def compare_and_swap(self, target, old_value, new_value):
        """
        Atomic Compare-And-Swap for updating head or next pointer.
        """
        if target is self:  # if target is the head pointer
            if self.head == old_value:  # if head has not changed
                self.head = new_value  # update head
                return True
        elif target == "tail":  # if target is the tail pointer
            if self.tail == old_value:  # if tail has not changed
                self.tail = new_value  # update tail
                return True
        else:  # if target is a node's next pointer
            if target.next == old_value:  # if next pointer has not changed
                target.next = new_value  # update next pointer
                return True
        return False

    def enqueue(self, order_type, ticker_symbol, quantity, price):
        """Add a Buy order to the end of the FIFO queue."""
        new_node = OrderNode(order_type, ticker_symbol, quantity, price)

        while True:
            old_tail = self.tail
            if not old_tail:  # if the list is empty
                if self.compare_and_swap(self, self.head, new_node):
                    self.compare_and_swap("tail", None, new_node)
                    return
            else:
                new_node.next = None
                if self.compare_and_swap(old_tail, old_tail.next, new_node):
                    self.compare_and_swap("tail", old_tail, new_node)
                    return

    def dequeue(self):
        """Remove and return the Buy order at the head of the FIFO queue."""
        while True:
            old_head = self.head
            if not old_head:
                return None  # queue is empty

            new_head = old_head.next
            if self.compare_and_swap(self, old_head, new_head):
                if not new_head:  # if the queue is now empty
                    self.compare_and_swap("tail", old_head, None)
                return old_head.order
            

class LockFreeSortedLinkedList:
    """A lock-free sorted linked list for storing Sell orders."""
    
    def __init__(self):
        self.head = None  # head pointer

    def compare_and_swap(self, target, old_value, new_value):
        """
        Atomic Compare-And-Swap for updating a target (head or next pointer).
        """
        if target is self:  # if target is the head pointer
            if self.head == old_value:  # if head has not changed
                self.head = new_value  # update head
                return True
        else:  # if target is a node's next pointer
            if target.next == old_value:  # if next pointer has not changed
                target.next = new_value  # update next pointer
                return True
        return False

    def insert(self, order_type, ticker_symbol, quantity, price):
        """Insert a Sell order into the sorted linked list in ascending order of price."""
        new_node = OrderNode(order_type, ticker_symbol, quantity, price)

        while True:
            # find the correct position to insert the new node
            prev = None
            current = self.head

            while current and current.order[3] < price:
                prev = current
                current = current.next

            # link the new node to the next node
            new_node.next = current

            # try to insert the new node
            if prev is None:  # insert at the head
                if self.compare_and_swap(self, current, new_node):
                    return
            else:  # insert after prev
                if self.compare_and_swap(prev, current, new_node):
                    return

    def remove(self, order):
        """Remove a Sell order from the linked list."""
        while True:
            prev = None
            current = self.head

            # find the node to remove
            while current and current.order != order:
                prev = current
                current = current.next

            if not current:
                return  # order not found

            # remove the node
            if prev is None:  # remove the head
                if self.compare_and_swap(self, current, current.next):
                    return
            else:  # remove a non-head node
                if self.compare_and_swap(prev, current, current.next):
                    return

    def get_best_sell(self):
        """Get the best Sell order (lowest price)."""
        return self.head.order if self.head else None