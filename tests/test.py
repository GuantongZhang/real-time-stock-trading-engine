import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import the modules to be tested
from order_node import OrderNode
from lock_free_lists import LockFreeFIFOLinkedList, LockFreeSortedLinkedList
from order_book import OrderBook
from simulator import simulate_stock_transactions, run_concurrent_test


# Test cases for OrderNode
def test_order_node_initialization():
    """Test the initialization of an OrderNode."""
    node = OrderNode('Buy', 'AAPL', 100, 150)
    assert node.order == ('Buy', 'AAPL', 100, 150)
    assert node.next is None


# Test cases for LockFreeFIFOLinkedList
def test_lock_free_fifo_linked_list_enqueue():
    """Test enqueue operation in LockFreeFIFOLinkedList."""
    fifo = LockFreeFIFOLinkedList()
    fifo.enqueue('Buy', 'AAPL', 100, 150)
    assert fifo.head.order == ('Buy', 'AAPL', 100, 150)
    assert fifo.tail.order == ('Buy', 'AAPL', 100, 150)

    fifo.enqueue('Buy', 'GOOG', 50, 1200)
    assert fifo.head.order == ('Buy', 'AAPL', 100, 150)
    assert fifo.tail.order == ('Buy', 'GOOG', 50, 1200)


def test_lock_free_fifo_linked_list_dequeue():
    """Test dequeue operation in LockFreeFIFOLinkedList."""
    fifo = LockFreeFIFOLinkedList()
    fifo.enqueue('Buy', 'AAPL', 100, 150)
    fifo.enqueue('Buy', 'GOOG', 50, 1200)

    assert fifo.dequeue() == ('Buy', 'AAPL', 100, 150)
    assert fifo.dequeue() == ('Buy', 'GOOG', 50, 1200)
    assert fifo.dequeue() is None  # Empty queue


# Test cases for LockFreeSortedLinkedList
def test_lock_free_sorted_linked_list_insert():
    """Test insert operation in LockFreeSortedLinkedList."""
    sorted_list = LockFreeSortedLinkedList()
    sorted_list.insert('Sell', 'AAPL', 100, 140)
    sorted_list.insert('Sell', 'AAPL', 50, 130)
    sorted_list.insert('Sell', 'AAPL', 200, 150)

    assert sorted_list.head.order == ('Sell', 'AAPL', 50, 130)  # Lowest price first
    assert sorted_list.head.next.order == ('Sell', 'AAPL', 100, 140)
    assert sorted_list.head.next.next.order == ('Sell', 'AAPL', 200, 150)


def test_lock_free_sorted_linked_list_remove():
    """Test remove operation in LockFreeSortedLinkedList."""
    sorted_list = LockFreeSortedLinkedList()
    sorted_list.insert('Sell', 'AAPL', 100, 140)
    sorted_list.insert('Sell', 'AAPL', 50, 130)
    sorted_list.insert('Sell', 'AAPL', 200, 150)

    sorted_list.remove(('Sell', 'AAPL', 100, 140))
    assert sorted_list.head.order == ('Sell', 'AAPL', 50, 130)
    assert sorted_list.head.next.order == ('Sell', 'AAPL', 200, 150)


def test_lock_free_sorted_linked_list_get_best_sell():
    """Test get_best_sell operation in LockFreeSortedLinkedList."""
    sorted_list = LockFreeSortedLinkedList()
    sorted_list.insert('Sell', 'AAPL', 100, 140)
    sorted_list.insert('Sell', 'AAPL', 50, 130)
    sorted_list.insert('Sell', 'AAPL', 200, 150)

    assert sorted_list.get_best_sell() == ('Sell', 'AAPL', 50, 130)  # Lowest price


# Test cases for OrderBook
def test_order_book():
    """Test the OrderBook based on the provided example."""
    order_book = OrderBook()

    order_book.add_order('Sell', 'AAPL', 100, 140)
    order_book.add_order('Sell', 'AAPL', 50, 130)
    order_book.add_order('Buy', 'AAPL', 120, 150)
    order_book.add_order('Sell', 'GOOG', 100, 1200)
    order_book.add_order('Sell', 'GOOG', 100, 1200)
    order_book.add_order('Buy', 'GOOG', 150, 1200)
    
    print(len(str(order_book)))
    assert str(order_book) == (
        "Buy Orders:\n"
        "  ('Buy', 'AAPL', 120, 150)\n"
        "  ('Buy', 'GOOG', 150, 1200)\n"
        "Sell Orders:\n"
        "  Ticker: AAPL\n"
        "    ('Sell', 'AAPL', 50, 130)\n"
        "    ('Sell', 'AAPL', 100, 140)\n"
        "  Ticker: GOOG\n"
        "    ('Sell', 'GOOG', 100, 1200)\n"
        "    ('Sell', 'GOOG', 100, 1200)"
    )

    # Match orders
    order_book.match_order()

    # Verify the state of the order book after matching
    assert str(order_book) == (
        "Buy Orders:\n"
        "Sell Orders:\n"
        "  Ticker: AAPL\n"
        "    ('Sell', 'AAPL', 30, 140)\n"
        "  Ticker: GOOG\n"
        "    ('Sell', 'GOOG', 50, 1200)"
    )

    # Try matching again (no more matches should be possible)
    order_book.match_order()

    # Verify the state remains unchanged
    assert str(order_book) == (
        "Buy Orders:\n"
        "Sell Orders:\n"
        "  Ticker: AAPL\n"
        "    ('Sell', 'AAPL', 30, 140)\n"
        "  Ticker: GOOG\n"
        "    ('Sell', 'GOOG', 50, 1200)"
    )

# Run all tests
if __name__ == "__main__":
    # Run all test functions
    test_order_node_initialization()
    test_lock_free_fifo_linked_list_enqueue()
    test_lock_free_fifo_linked_list_dequeue()
    test_lock_free_sorted_linked_list_insert()
    test_lock_free_sorted_linked_list_remove()
    test_lock_free_sorted_linked_list_get_best_sell()
    test_order_book()

    print("All tests passed!")