from gptreplyguy import gpt_reply_guy, logger
from shared import secrets, search

logger.start_logging()

# client = gpt_reply_guy.GPTReplyGuy()
client = search.TwitterMonitor()
client.run(secrets.discord_api_key_chungus)