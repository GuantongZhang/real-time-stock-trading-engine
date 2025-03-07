class OrderNode:
    """A node in a lock-free linked list."""
    def __init__(self, order_type, ticker_symbol, quantity, price):
        self.order = (order_type, ticker_symbol, quantity, price)
        self.next = None  # pointer to next node