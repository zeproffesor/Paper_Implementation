from LimitOrderBook import LimitOrderBook
import numpy
from Order import Order
import logging

ALPHA = 100.0
MU = 30.0
DELTA = 5.0


class Simulator:

    def __init__(self):
        self.orderBook = LimitOrderBook()


    def generate_orders(self):
        num_market_orders = numpy.random.poisson(MU)
        num_limit_orders = numpy.random.poisson(ALPHA)
        num_cancel_orders = numpy.random.poisson(DELTA)

        ret = {"Market_Orders":[], "Limit_Orders":[], "Cancel_Orders":[]}
        for _ in range(num_market_orders):
            order = "1,"
            dir = numpy.random.randint(0,2)
            order += str(dir)+","
            order += "AAPL,"
            order += "10000" if dir else "0"
            ret["Market_Orders"].append(self.parse_order(order))
        
        for _ in range(num_limit_orders):
            order = "1,"
            dir = numpy.random.randint(0,2)
            order += str(dir)+","
            order += "AAPL,"
            price = numpy.random.randint(0,self.orderBook.get_best_ask()+1) if dir else numpy.random.randint(self.orderBook.get_best_bid(),10001)
            order += str(price)
            ret["Limit_Orders"].append(self.parse_order(order))

        if len(self.orderBook.all_curr_orders()):
            cancel_orders = list(numpy.random.choice(numpy.array(self.orderBook.all_curr_orders()), min(len(self.orderBook.all_curr_orders()),num_cancel_orders), replace=False))
            ret["Cancel_Orders"].extend(cancel_orders)
        return ret
    
    def parse_order(self, order):
        args = order.split(',')
        args[0] = int(args[0])
        args[1] = int(args[1])
        args[3] = int(args[3])
        return Order(*args)
    
    def simulate(self):
        for i in range(1000):
            orders = self.generate_orders()
            for order in orders['Cancel_Orders']:
                self.orderBook.cancel_order(order)
            for order in orders['Limit_Orders']:
                self.orderBook.add_order(order)
            for order in orders['Market_Orders']:
                self.orderBook.add_order(order)
            
            ts = []
            for limit_price in range(10001):
                ts.append( ( self.orderBook.book[limit_price].num_orders(0), self.orderBook.book[limit_price].num_orders(1) ) )
            
            compressed_ts = []
            j=0
            while j<len(ts):
                if ts[j][0] or ts[j][1]:
                    compressed_ts.append(ts[j])
                    j += 1
                else:
                    zeros = 0
                    k = j
                    while k<len(ts) and ts[k][0]==0 and ts[k][1]==0:
                        zeros += 1
                        k += 1
                    j = k
                    compressed_ts.append(zeros)
            
            with open("data.txt", "a") as f:
                f.write(str(compressed_ts)+"\n")
            logging.info("Appended"+str(compressed_ts)[:11]+"...")

def main():
    logging.basicConfig(level=20)
    simulator = Simulator()
    simulator.simulate()
    

main()