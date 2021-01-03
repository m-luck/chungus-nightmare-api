import cryptocompare
from shared import secrets, search

client = search.CryptoMonitor()
client.run(secrets.discord_api_key_crypto)

client.report()