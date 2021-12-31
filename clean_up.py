from binance import Client

import config


def init():
    #opening client connection to binance
    client = Client(config.API_KEY, config.API_SECRET)
    info = client.get_my_trades(symbol='AVAXUSDT',limit=1)
    print(info)


def main():
    init()


main()