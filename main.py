from telethon import TelegramClient, Button
from telethon.events import NewMessage
from telethon.custom import Message
from telethon.errors import ButtonUrlInvalidError
from telethon.types import PeerChannel
from enum import IntEnum, unique
from re import match

from config import Configs
from strings import Strings

client = TelegramClient(
    session=Configs.SESSION_NAME,
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH
).start(
    bot_token=Configs.BOT_TOKEN
)


button = [
    Button.url("name", "url")
]


step = dict()


@unique
class Part(IntEnum):
    GET_MESSAGE = 1
    GET_URL = 2


@client.on(NewMessage(func=lambda event: event.is_private and str(event.sender_id) in step, from_users=Configs.ADMINS))
async def get_informations(event: Message):
    
    message = event.message.message
    user_id = str(event.sender_id)
    part = step.get(user_id).get("PART")
    
    if (message == "/cancel"):

        await client.send_message(
            entity=event.chat_id,
            message=Strings.CANCELED
        )

        del step[user_id]

    elif (part == Part.GET_MESSAGE):

        step[user_id] = {
            "PART": Part.GET_URL,
            "MESSAGE": event.message
        }

        await client.send_message(
            entity=event.chat_id,
            message=Strings.GET_URL
        )

    elif (part == Part.GET_URL):

        if (not match(r"^https{0,1}.", str(message))):

            await client.send_message(
                entity=event.chat_id,
                message=Strings.BAD_URL
            )

        else:

            button = [Button.url(text=Strings.CONNECT, url=str(message))]
            text = step[user_id]["MESSAGE"]

            try:

                await client.send_message(
                    entity=event.chat_id,
                    message=text,
                    buttons=button
                )

                channel_not_sended, message = set(), step[user_id]["MESSAGE"]
                del step[user_id]

            except ButtonUrlInvalidError:

                await client.send_message(
                    entity=event.chat_id,
                    message=Strings.BAD_URL
                )
            
            else:

                for channel in Configs.CHANNELS:

                    try:

                        await client.send_message(
                            entity=PeerChannel(int(channel)),
                            message=message,
                            buttons=button
                        )

                    except:

                        channel_not_sended.add(channel)
                
                else:

                    channel_sended = (Configs.CHANNELS - channel_not_sended)
                    message = Strings.channels_send_status(channel_sended, channel_not_sended)

                    await client.send_message(
                        entity=event.chat_id,
                        message=message
                    )


@client.on(NewMessage(func=lambda event: event.is_private and not str(event.sender_id) in step, from_users=Configs.ADMINS))
async def commands(event: Message):

    message = event.message.message

    if (message == "/start"):

        await client.send_message(
        entity=event.chat_id,
        message=Strings.START
    )

    elif (message == "/send"):

        
        if (Configs.CHANNELS):

            text = Strings.GET_MESSAGE
            step[str(event.sender_id)] = {
                "PART": Part.GET_MESSAGE
            }

        else:

            text = Strings.CHANNEL_LIST_IS_EMPTY

        await client.send_message(
        entity=event.chat_id,
        message=text
    )

    
print("Bot is online : )")
client.run_until_disconnected()
