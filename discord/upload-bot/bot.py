import json
from pprint import pprint
from discord import Game
from discord.ext.commands import Bot
from helpers import download_file

TOKEN = ''

BOT_PREFIX = ("?", "!")

LAST_MESSAGE_ID_CHECKED = {}

client = Bot(command_prefix=BOT_PREFIX)

pinry = Pinry(
    host='localhost',
    username='',
    password=''
)


async def upload_discord_log(log):
    print('upload start')
    upload_report = ''
    thanks = False

    for attachment in log.attachments:
        pprint(attachment)

        filepath = f'{attachment["filename"]}'
        source = attachment['url']

        download_file(source, filepath)
        pinry.upload_file(filepath)

        pin = await pinry.new_pin(
            description='automatic upload',
            tags=[],
            filename=attachment['filename']
        )

        if pin.get('id'):
            thanks = True
            upload_report += f'Uploaded **{attachment["filename"]}** under **{log.channel.name}**\n'
        else:
            upload_report += f'Upload failed: **{attachment["filename"]}**'

    if thanks:
        upload_report += f'Thank you, {log.author.mention}!'

    await client.say(f'Upload complete: {attachment["filename"]}\nUrl: http://localhost/{pin["id"]}/')

    LAST_MESSAGE_ID_CHECKED[log.channel.id] = log.id
    with open('last_message_id_checked.json', 'w') as outfile:
        json.dump(LAST_MESSAGE_ID_CHECKED, outfile)


@client.event
async def on_message(message):
    if message.content.startswith('!upload'):
        force = message.content.startswith('!upload --force')

        async for log in client.logs_from(message.channel, limit=200, reverse=True):
            if not force:
                if LAST_MESSAGE_ID_CHECKED.get(message.channel.id):
                    if LAST_MESSAGE_ID_CHECKED[message.channel.id] > log.id:
                        print(f'Already checked: {log.content}')

            if log.attachments:
                await upload_discord_log(log)

    if message.content.startswith('!scan'):
        async for log in client.logs_from(message.channel, limit=200, reverse=True):
            print(log.content)
            if log.attachments:
                print(log.attachments)

    if message.content.startswith('!clear'):
        clear_all = message.content.startswith('!clear_all')

        async for log in client.logs_from(message.channel, limit=100):
            if not clear_all:
                if log.author == client.user or log.content.strip() == '!upload':
                    await client.delete_message(log)
            else:
                await client.delete_message(log)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="uploader"))
    print("Logged in as " + client.user.name)


if __name__ == '__main__':
    try:
        with open('last_message_id_checked.json') as json_data:
            LAST_MESSAGE_ID_CHECKED = json.load(json_data)
    except FileNotFoundError:
        LAST_MESSAGE_ID_CHECKED = {}

    pprint(LAST_MESSAGE_ID_CHECKED)

    client.run(TOKEN)
