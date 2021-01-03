from shared import secrets, search

client = search.TwitterMonitor()
client.run(secrets.discord_api_key_fiat)