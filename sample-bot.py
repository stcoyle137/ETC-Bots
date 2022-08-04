#!/usr/bin/env python3
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py --test prod-like; sleep 1; done

import argparse
from collections import deque
from enum import Enum
import time
import math
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
# Replace "REPLACEME" with your team name!
team_name = "STRIPEDBASS"

# ~~~~~============== MAIN LOOP ==============~~~~~

# You should put your code here! We provide some starter code as an example,
# but feel free to change/remove/edit/update any of it as you'd like. If you
# have any questions about the starter code, or what to do next, please ask us!
#
# To help you get started, the sample code below tries to buy BOND for a low
# price, and it prints the current prices for VALE every second. The sample
# code is intended to be a working example, but it needs some improvement
# before it will start making good trades!


def main():
    args = parse_arguments()

    exchange = ExchangeConnection(args=args)

    # Store and print the "hello" message received from the exchange. This
    # contains useful information about your positions. Normally you start with
    # all positions at zero, but if you reconnect during a round, you might
    # have already bought/sold symbols and have non-zero positions.
    hello_message = exchange.read_message()
    print("First message from exchange:", hello_message)

    # Send an order for BOND at a good price, but it is low enough that it is
    # unlikely it will be traded against. Maybe there is a better price to
    # pick? Also, you will need to send more orders over time.

    exchange.send_add_message(order_id=1, symbol="BOND", dir=Dir.BUY, price=999, size=50)
    exchange.send_add_message(order_id=2, symbol="BOND", dir=Dir.SELL, price=1001, size=50)

    exchange.send_add_message(order_id=1000000, symbol="GS", dir=Dir.BUY, price=8000, size=50)
    exchange.send_add_message(order_id=1000001, symbol="GS", dir=Dir.SELL, price=9000, size=50)

    exchange.send_add_message(order_id=1000007, symbol="MS", dir=Dir.BUY, price=3700, size=50)
    exchange.send_add_message(order_id=1000002, symbol="MS", dir=Dir.SELL, price=4200, size=50)

    exchange.send_add_message(order_id=1000006, symbol="WFC", dir=Dir.BUY, price=5000, size=50)
    exchange.send_add_message(order_id=1000003, symbol="WFC", dir=Dir.SELL, price=6000, size=50)

    exchange.send_add_message(order_id=1000005, symbol="XLF", dir=Dir.BUY, price=4000, size=50)
    exchange.send_add_message(order_id=1000004, symbol="XLF", dir=Dir.SELL, price=4500, size=50)

    # Set up some variables to track the bid and ask price of a symbol. Right
    # now this doesn't track much information, but it's enough to get a sense
    # of the VALE market.
    vale_bid_price, vale_ask_price = None, None
    vale_last_print_time = time.time()
    valbz_bid_price, valbz_ask_price = None, None
    valbz_last_print_time = time.time()


    gs_last_time = time.time()
    # Here is the main loop of the program. It will continue to read and
    # process messages in a loop until a "close" message is received. You
    # should write to code handle more types of messages (and not just print
    # the message). Feel free to modify any of the starter code below.
    #
    # Note: a common mistake people make is to call write_message() at least
    # once for every read_message() response.
    #
    # Every message sent to the exchange generates at least one response
    # message. Sending a message in response to every exchange message will
    # cause a feedback loop where your bot's messages will quickly be
    # rate-limited and ignored. Please, don't do that!
    bond_id_buy_list = [1]
    bond_id_sell_list = [2]
    vale_id_buy_list = 0
    vale_id_sell_list = 0
    vale_sell_amt = 0
    vale_buy_amt = 0
    valbz_id_buy_list = 0
    valbz_id_sell_list = 0
    valbz_sell_amt = 0
    valbz_buy_amt = 0
    id_current = 2
    avg = None

    array_GS_over_time = []

    while True:
        # All exchange information comes from this method
        message = exchange.read_message()

        # Some of the message types below happen infrequently and contain
        # important information to help you understand what your bot is doing,
        # so they are printed in full. We recommend not always printing every
        # message because it can be a lot of information to read. Instead, let
        # your code handle the messages and just print the information
        # important for you!
        if message["type"] == "close":
            print("The round has ended")
            break
        elif message["type"] == "error":
            print(message)
        elif message["type"] == "reject":
            if message["order_id"] == vale_id_buy_list:
                print("Vale Buy")
            elif message["order_id"] == vale_id_sell_list:
                print("Vale Sell")
            print(message)
        elif message["type"] == "fill":
            if message["order_id"] in bond_id_buy_list:
                id_current += 1
                exchange.send_add_message(order_id=id_current, symbol="BOND", dir=Dir.BUY, price=999, size=message["size"])
                bond_id_buy_list.append(id_current)
            elif message["order_id"] in bond_id_sell_list:
                id_current += 1
                exchange.send_add_message(order_id=id_current, symbol="BOND", dir=Dir.SELL, price=1001, size=message["size"])
                bond_id_sell_list.append(id_current)
            elif message["order_id"] == vale_id_buy_list:
                vale_buy_amt -= message["size"]
            elif message["order_id"] == vale_id_sell_list:
                vale_sell_amt -= message["size"]
            print(message)




            print(message)
        elif message["type"] == "book":
            for side in ["sell", "buy"]:
                for i in range(len(message[side])):
                    d = None
                    if side == "sell":
                        d = Dir.BUY
                    else:
                        d = Dir.SELL
                    id_current += 1
                    if message[side][i][0] not in [8000,9000,3700,4200,5000,6000,4000,4500]:
                        time.sleep(0.01)
                        exchange.send_add_message(order_id=id_current, symbol=message["symbol"], dir=d, price=message[side][i][0], size=message[side][i][1])
            '''
            if message["symbol"] == "VALE":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]


                vale_bid_price = best_price("buy")
                vale_ask_price = best_price("sell")

                now = time.time()

                if now > vale_last_print_time + 1:
                    vale_last_print_time = now
                    print(
                        {
                            "vale_bid_price": vale_bid_price,
                            "vale_ask_price": vale_ask_price,
                        }
                    )

                if vale_bid_price == None or valbz_bid_price == None:
                    x = 0
                elif vale_bid_price > valbz_bid_price and vale_sell_amt == 0:
                    id_current += 1
                    exchange.send_cancel_message(order_id=vale_id_sell_list)
                    exchange.send_cancel_message(order_id=vale_id_buy_list)
                    vale_id_sell_list = id_current
                    exchange.send_add_message(order_id=id_current, symbol="VALE", dir=Dir.SELL, price=vale_bid_price, size=10)
                    vale_buy_amt = 0
                    vale_sell_amt = 10

                if vale_ask_price == None or valbz_ask_price == None:
                    x = 0
                elif vale_ask_price < valbz_ask_price and vale_buy_amt == 0:
                    id_current += 1
                    exchange.send_cancel_message(order_id=vale_id_sell_list)
                    exchange.send_cancel_message(order_id=vale_id_buy_list)
                    vale_id_buy_list = id_current
                    exchange.send_add_message(order_id=id_current, symbol="VALE", dir=Dir.BUY, price=vale_ask_price, size=10)
                    vale_buy_amt = 10
                    vale_sell_amt = 0

            elif message["symbol"] == "VALBZ":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]


                valbz_bid_price = best_price("buy")
                valbz_ask_price = best_price("sell")

                now = time.time()

                if now > valbz_last_print_time + 1:
                    valbz_last_print_time = now
                    print(
                        {
                            "valbz_bid_price": valbz_bid_price,
                            "valbz_ask_price": valbz_ask_price,
                        }
                    )
                if vale_bid_price == None or valbz_bid_price == None:
                    x = 0
                elif vale_bid_price > valbz_bid_price and vale_sell_amt == 0:
                    id_current += 1
                    exchange.send_cancel_message(order_id=vale_id_sell_list)
                    exchange.send_cancel_message(order_id=vale_id_buy_list)
                    vale_id_sell_list = id_current
                    exchange.send_add_message(order_id=id_current, symbol="VALE", dir=Dir.SELL, price=vale_bid_price, size=10)
                    vale_buy_amt = 0
                    vale_sell_amt = 10

                if vale_ask_price == None or valbz_ask_price == None:
                    x = 0
                elif vale_ask_price < valbz_ask_price and vale_buy_amt == 0:
                    id_current += 1
                    exchange.send_cancel_message(order_id=vale_id_sell_list)
                    exchange.send_cancel_message(order_id=vale_id_buy_list)
                    vale_id_buy_list = id_current
                    exchange.send_add_message(order_id=id_current, symbol="VALE", dir=Dir.BUY, price=vale_ask_price, size=10)
                    vale_buy_amt = 10
                    vale_sell_amt = 0

            elif message["symbol"] == "GS":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                avg = math.floor((best_price("buy") + best_price("sell"))/2)

                if time.time() > gs_last_time + 1:
                    gs_last_time = time.time()

                    exchange.send_cancel_message(order_id=10000000000000000)
                    exchange.send_cancel_message(order_id=10000000000000001)

                    exchange.send_add_message(order_id=10000000000000000, symbol="GS", dir=Dir.BUY, price=avg-3, size=1)
                    exchange.send_add_message(order_id=10000000000000001, symbol="GS", dir=Dir.SELL, price=avg+3, size=1)

'''














# ~~~~~============== PROVIDED CODE ==============~~~~~

# You probably don't need to edit anything below this line, but feel free to
# ask if you have any questions about what it is doing or how it works. If you
# do need to change anything below this line, please feel free to


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class ExchangeConnection:
    def __init__(self, args):
        self.message_timestamps = deque(maxlen=500)
        self.exchange_hostname = args.exchange_hostname
        self.port = args.port
        self.exchange_socket = self._connect(add_socket_timeout=args.add_socket_timeout)

        self._write_message({"type": "hello", "team": team_name.upper()})

    def read_message(self):
        """Read a single message from the exchange"""
        message = json.loads(self.exchange_socket.readline())
        if "dir" in message:
            message["dir"] = Dir(message["dir"])
        return message

    def send_add_message(
        self, order_id: int, symbol: str, dir: Dir, price: int, size: int
    ):
        """Add a new order"""
        self._write_message(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "price": price,
                "size": size,
            }
        )

    def send_convert_message(self, order_id: int, symbol: str, dir: Dir, size: int):
        """Convert between related symbols"""
        self._write_message(
            {
                "type": "convert",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "size": size,
            }
        )

    def send_cancel_message(self, order_id: int):
        """Cancel an existing order"""
        print(order_id)
        self._write_message({"type": "cancel", "order_id": order_id})

    def _connect(self, add_socket_timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if add_socket_timeout:
            # Automatically raise an exception if no data has been recieved for
            # multiple seconds. This should not be enabled on an "empty" test
            # exchange.
            s.settimeout(5)
        s.connect((self.exchange_hostname, self.port))
        return s.makefile("rw", 1)

    def _write_message(self, message):
        json.dump(message, self.exchange_socket)
        self.exchange_socket.write("\n")

        now = time.time()
        self.message_timestamps.append(now)
        if len(
            self.message_timestamps
        ) == self.message_timestamps.maxlen and self.message_timestamps[0] > (now - 1):
            print(
                "WARNING: You are sending messages too frequently. The exchange will start ignoring your messages. Make sure you are not sending a message in response to every exchange message."
            )


def parse_arguments():
    test_exchange_port_offsets = {"prod-like": 0, "slower": 1, "empty": 2}

    parser = argparse.ArgumentParser(description="Trade on an ETC exchange!")
    exchange_address_group = parser.add_mutually_exclusive_group(required=True)
    exchange_address_group.add_argument(
        "--production", action="store_true", help="Connect to the production exchange."
    )
    exchange_address_group.add_argument(
        "--test",
        type=str,
        choices=test_exchange_port_offsets.keys(),
        help="Connect to a test exchange.",
    )

    # Connect to a specific host. This is only intended to be used for debugging.
    exchange_address_group.add_argument(
        "--specific-address", type=str, metavar="HOST:PORT", help=argparse.SUPPRESS
    )

    args = parser.parse_args()
    args.add_socket_timeout = True

    if args.production:
        args.exchange_hostname = "production"
        args.port = 25000
    elif args.test:
        args.exchange_hostname = "test-exch-" + team_name
        args.port = 25000 + test_exchange_port_offsets[args.test]
        if args.test == "empty":
            args.add_socket_timeout = False
    elif args.specific_address:
        args.exchange_hostname, port = args.specific_address.split(":")
        args.port = int(port)

    return args


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (
        team_name != "REPLACEME"
    ), "Please put your team name in the variable [team_name]."

    main()
