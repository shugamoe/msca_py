# Julian McClellan
# Week 5 | Order Book
# Advanced Python for Streaming Analytics

# TODO(jcm) implement Modify order, delete order

import unittest

class GlobalOrderBook:
    def __init__(self):
        self.books = {}
    def add_order(self, order):
        if self.books.get(order["symbol"]):
            self.books[order["symbol"]].add_order(order)
        else:
            self.books[order["symbol"]] = OrderBook()
            self.books[order["symbol"]].add_order(order)
    
    def modify_order(self, order):
        if self.books.get(order["symbol"]):
            self.books[order["symbol"]].modify_order(order)
        else:
            raise Exception("No order book exists for this symbol.")

    def delete_order(self, order):
        if self.books.get(order["symbol"]):
            self.books[order["symbol"]].delete_order(order)
        else:
            raise Exception("No order book exists for this symbol.")

    def get_top_of_book(self, symbol):
        if self.books.get(symbol):
            return self.books[symbol].get_top_of_book()
        else:
            raise Exception("No order book exists for this symbol.")


class OrderBook:
    def __init__(self):
        self.offers, self.bids = [], []
    def add_order(self, order):
        # Could also replace this logic with getattr
        if order["side"] == "bid":
            self.bids.append(order)
        elif order["side"] == "offer":
            self.offers.append(order)
        else:
            raise Exception("Order side?")
        self.best_price_to_top(order["side"])

    def modify_order(self, order):
        if order["side"] == "bid":
            self.bids = [bid if bid["id"] != order["id"] else order for bid in self.bids]
        elif order["side"] == "offer":
            self.offers = [offer if offer["id"] != order["id"] else order for offer in self.offers]
        else: 
            raise Exception("Order side?")

    def delete_order(self, order):
        if order["side"] == "bid":
            self.bids = [bid for bid in self.bids if bid["id"] != order["id"]]
        elif order["side"] == "offer":
            self.offers = [offer for offer in self.offers if offer["id"] != order["id"]]
        else: 
            raise Exception("Order side?")

    def best_price_to_top(self, side):
        if side == "order":
            self.offers.sort(key=lambda k: k["price"], reverse=True)
        elif side == "bid":
            self.bids.sort(key=lambda k: k["price"], reverse=True)

    def get_top_of_book(self):
        self.best_price_to_top("bid")
        self.best_price_to_top("offer")
        return (self.bids[0] if len(self.bids) > 0 else None,
                self.offers[0] if len(self.offers) > 0 else None)


class TestOrderBook(unittest.TestCase):
    o1 = {"price": 10.43, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "AAPL", "id": 1}

    o2 = {"price": 10.03, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "AAPL", "id": 2}

    o3 = {"price": 11.03, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "AAPL", "id": 3}

    o3_replace = {"price": 11.69, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "AAPL", "id": 3}

    o1penis = {"price": 10.43, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "PENIS", "id": 1}

    o2penis = {"price": 10.03, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "PENIS", "id": 2}

    o3penis = {"price": 11.03, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "PENIS", "id": 3}

    o3p_replace = {"price": 11.69, "quantity": 1000, "side": "bid", "venue":
            "London", "symbol": "PENIS", "id": 3} 

    def test_add_order(self):
        ob = OrderBook()
        ob.add_order(self.o1)

        self.assertTrue(len(ob.bids) == 1)
        self.assertTrue(ob.bids[0]["price"] == 10.43)

        ob.add_order(self.o2)
        self.assertTrue(len(ob.bids) == 2)
        self.assertTrue(ob.bids[0]["price"] == 10.43)
        self.assertTrue(ob.bids[1]["price"] == 10.03)

        ob.add_order(self.o3)
        self.assertTrue(len(ob.bids) == 3)
        self.assertTrue(ob.bids[0]["price"] == 11.03)
        self.assertTrue(ob.bids[1]["price"] == 10.43)
        self.assertTrue(ob.bids[2]["price"] == 10.03)

        b, o = ob.get_top_of_book()
        self.assertTrue(b["price"] == 11.03)
        self.assertTrue(o is None)


    def test_g_add_mod_delete_order(self):
        gob = GlobalOrderBook()
        gob.add_order(self.o1)
        gob.add_order(self.o1penis)
        self.assertTrue(len(gob.books.keys()) == 2)

        self.assertTrue(gob.books.get(self.o1["symbol"]))
        self.assertTrue(gob.books.get(self.o1penis["symbol"]))
        self.assertTrue(gob.books[self.o1["symbol"]].bids[0]["price"] == 10.43)


        gob.add_order(self.o2)
        gob.add_order(self.o2penis)
        self.assertTrue(gob.books[self.o1["symbol"]].bids[0]["price"] == 10.43)
        self.assertTrue(gob.books[self.o1["symbol"]].bids[1]["price"] == 10.03)
        self.assertTrue(gob.books[self.o2["symbol"]].bids[0]["price"] == 10.43)
        self.assertTrue(gob.books[self.o1["symbol"]].bids[1]["price"] == 10.03)


        gob.add_order(self.o3)
        gob.add_order(self.o3penis)

        b, o = gob.get_top_of_book("AAPL")
        self.assertTrue(b["price"] == 11.03)
        self.assertTrue(o is None)

        b, o = gob.get_top_of_book("PENIS")
        self.assertTrue(b["price"] == 11.03)
        self.assertTrue(o is None)

        gob.modify_order(self.o3_replace)
        gob.modify_order(self.o3p_replace)

        b, o = gob.get_top_of_book("AAPL")
        self.assertTrue(b["price"] == 11.69)
        b, o = gob.get_top_of_book("PENIS")
        self.assertTrue(b["price"] == 11.69)

        gob.delete_order({"symbol": "AAPL", "id": 3, "side": "bid"})
        gob.delete_order({"symbol": "PENIS", "id": 3, "side": "bid"})

        b, o = gob.get_top_of_book("AAPL")
        self.assertTrue(b["price"] == 10.43)
        self.assertTrue(o is None)

        b, o = gob.get_top_of_book("PENIS")
        self.assertTrue(b["price"] == 10.43)
        self.assertTrue(o is None)



if __name__ == "__main__":
    unittest.main()



