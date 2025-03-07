import random
import threading
from order_book import OrderBook

def simulate_stock_transactions(order_book, num_orders=1000):
    """Simulate active stock transactions by randomly adding orders."""
    tickers = [f"STOCK_{i+1:04d}" for i in range(1024)]
    order_types = ['Buy', 'Sell']

    for _ in range(num_orders):
        order_type = random.choice(order_types)
        ticker = random.choice(tickers)
        quantity = random.randint(1, 10)  # random quantity between 1 and 1,000
        price = round(random.random()*100, 2)  # random price between 0 and 100

        order_book.add_order(order_type, ticker, quantity, price)

def run_concurrent_test(order_book, num_threads, orders_per_thread):
    """Run multiple threads to simulate concurrent order additions and matching."""
    threads = []

    # create threads for adding orders
    for _ in range(num_threads):
        thread = threading.Thread(target=simulate_stock_transactions, args=(order_book, orders_per_thread))
        threads.append(thread)
        thread.start()

    # create a thread for matching orders
    match_thread = threading.Thread(target=order_book.match_order)
    threads.append(match_thread)
    match_thread.start()

    # wait for all threads to finish
    for thread in threads:
        thread.join()

    print("Concurrent test completed.")

if __name__ == "__main__":
    order_book = OrderBook()

    run_concurrent_test(order_book, num_threads=5, orders_per_thread=10)

    print("\nRemaining Orders:")
    print(order_book)