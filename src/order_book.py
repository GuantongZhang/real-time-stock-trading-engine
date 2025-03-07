from lock_free_lists import LockFreeFIFOLinkedList, LockFreeSortedLinkedList
class OrderBook:
    """A lock-free order book."""
    
    def __init__(self):
        self.buy_orders = LockFreeFIFOLinkedList()  # store Buy orders in a queue
        self.sell_orders = {}  # dictionary to store Sell orders per ticker (each is sorted)
    
    def __str__(self):
        """Returns a string representation of the order book."""
        result = []

        # Display Buy orders
        result.append("Buy Orders:")
        current_buy = self.buy_orders.head
        while current_buy:
            result.append(f"  {current_buy.order}")
            current_buy = current_buy.next

        # Display Sell orders
        result.append("Sell Orders:")
        for ticker, sell_list in self.sell_orders.items():
            result.append(f"  Ticker: {ticker}")
            current_sell = sell_list.head
            while current_sell:
                result.append(f"    {current_sell.order}")
                current_sell = current_sell.next

        return "\n".join(result)

    def add_order(self, order_type, ticker_symbol, quantity, price, display=True):
        """Add an order to the order book."""
        if order_type == 'Buy':
            self.buy_orders.enqueue(order_type, ticker_symbol, quantity, price)
        elif order_type == 'Sell':
            if ticker_symbol not in self.sell_orders:
                self.sell_orders[ticker_symbol] = LockFreeSortedLinkedList()
            self.sell_orders[ticker_symbol].insert(order_type, ticker_symbol, quantity, price)

        if display: print(f'Order added: {(order_type, ticker_symbol, quantity, price)}')

    def match_order(self):
        """Match Buy orders with the best available Sell orders for all tickers."""

        while True:
            # THE LOGIC HERE NEED TO BE MODIFIED IF WE WANT TO KEEP UNRESOLVED BUY ORDERS AFTER MATCHING.
            # At this moment we assume that match_order will only be run once.
            buy_order = self.buy_orders.dequeue()
            if not buy_order:
                print("No more matches possible.")
                break  # no more Buy orders to process

            buy_type, buy_ticker, buy_qty, buy_price = buy_order

            if buy_ticker not in self.sell_orders:
                continue  # no Sell orders for this ticker

            best_sell = self.sell_orders[buy_ticker].get_best_sell()
            if not best_sell:
                continue  # No Sell orders available for this ticker

            sell_type, sell_ticker, sell_qty, sell_price = best_sell

            if buy_price >= sell_price:
                # Calculate matched quantity
                matched_qty = min(buy_qty, sell_qty)
                print(f"Matched {matched_qty} shares of {buy_ticker} at Buy={buy_price}, Sell={sell_price}")

                # Remove matched Sell order
                self.sell_orders[buy_ticker].remove(best_sell)

                # Re-add remaining quantities
                if buy_qty > matched_qty:
                    self.add_order(buy_type, buy_ticker, buy_qty - matched_qty, buy_price, display=False)
                if sell_qty > matched_qty:
                    self.add_order(sell_type, sell_ticker, sell_qty - matched_qty, sell_price, display=False)