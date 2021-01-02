import gpt_reply_guy
import logger
import secrets

logger.start_logging()

client = gpt_reply_guy.GPTReplyGuy()
client.run(secrets.api_key)