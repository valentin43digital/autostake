import requests


def get_dex_info(chainId, pairAddress):
    r = requests.get(f"https://api.dexscreener.io/latest/dex/pairs/{chain}/{address}")
    return r.json()


if __name__ == "__main__":
    chain = "bsc"
    address = "0x1747af98ebf0b22d500014c7dd52985d736337d2"
    print(get_dex_info(chainId=chain, pairAddress=address))
