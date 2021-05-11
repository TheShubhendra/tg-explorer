import asyncio
from decouple import config

from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.get_logger()

API_ID = config("API_ID", None)
API_HASH = config("API_HASH", None)

client = TelegramClient("tg_explorer", API_ID, API_HASH)


def extract_invite_hash(text):
    pat=r"https://t.me/joinchat/([A-Za-z0-9]+)"
    x = re.findall(pat,text)
    logger.info(f"Found {len(x)} invite links")

async def join_chat(invite_hash):
    result = await client(ImportChatInviteRequest(invite_hash))
    logger.info(result.stringify())
 
async def check_invite_link(invite_hash):
    result = await client(CheckChatInviteRequest(invite_hash))
    print(result.stringify())


async def main():
    await client.start()
    await check_invite_link()

if __name__ == "__main__":
	asyncio.run(main())
