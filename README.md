# real-time-stock-trading-engine

A Solution to the Interview Question of Onymos Inc.

## Author

Guantong Zhang

## Requirements

Implement a real-time Stock trading engine for matching Stock Buys with Stock Sells.
1. Write an ‘addOrder’ function that will have the following parameters:
      ‘Order Type’ (Buy or Sell), ‘Ticker Symbol’, ‘Quantity’, ‘Price’
      Support 1,024 tickers (stocks) being traded.
      Write a wrapper to have this ‘addOrder’ function randomly execute with different parameter values to simulate active stock transactions.

2. Write a ‘matchOrder’ function, that will match Buy & Sell orders with the following criteria:
      Buy price for a particular ticker is greater than or equal to lowest Sell price available then.
      Write your code to handle race conditions when multiple threads modify the Stock order book, as run in real-life, by multiple stockbrokers. Also, use lock-free data structures.
      Do not use any dictionaries, maps or equivalent data structures. Essentially there should be no ‘import’-s nor ‘include’-s nor similar construct relevant to the programming language you are using that provides you dictionary, map or equivalent data structure capability. In essence, you are writing the entire code. Standard language-specific non data structure related items are ok, but try to avoid as best as you can.
      Write your ‘matchOrder’ function with a time-complexity of O(n), where 'n' is the number of orders in the Stock order book.

## Basic Usage

    from src.order_book import OrderBook

    # Create an order book
    order_book = OrderBook()

    # Add orders
    order_book.add_order('Sell', 'AAPL', 100, 140)
    order_book.add_order('Sell', 'AAPL', 50, 130)
    order_book.add_order('Buy', 'AAPL', 120, 150)

    # Match orders
    order_book.match_order()

    # Print the remaining orders
    print(order_book)
    
### Output
    Order added: ('Sell', 'AAPL', 100, 140)
    Order added: ('Sell', 'AAPL', 50, 130)
    Order added: ('Buy', 'AAPL', 120, 150)
    Matched 50 shares of AAPL at Buy=150, Sell=130
    Matched 70 shares of AAPL at Buy=150, Sell=140
    Buy Orders:
      ('Buy', 'AAPL', 0, 150)
    Sell Orders:
      Ticker: AAPL
        ('Sell', 'AAPL', 30, 140)

## Concurrent Usage
    from src.simulator import run_concurrent_test
    from src.order_book import OrderBook
    
    # Create an order book
    order_book = OrderBook()
    
    # Run the concurrent test
    run_concurrent_test(order_book, num_threads=10, orders_per_thread=100)
    
    # Print the remaining orders
    print(order_book)
    
### Output
    Concurrent test completed.
    Buy Orders:
      ('Buy', 'AAPL', 50, 150)
      ('Buy', 'GOOG', 100, 1250)
    Sell Orders:
      Ticker: AAPL
        ('Sell', 'AAPL', 30, 140)
      Ticker: GOOG
        ('Sell', 'GOOG', 50, 1200)
    
## Testing

To run the test, use the following command:

    python -m pytest tests/test.py -v

## Contact

If you have any questions or suggestions, feel free to reach out:

Email: guantonz@andrew.cmu.edu / gtzhang2002@gmail.com

GitHub: GuantongZhang
