import shutil
import time
import discord
import os
from discord.ext import tasks
from discord.ext import commands
import zipfile
import warnings
import public_ip as ip
import requests
import io
# Import pywinauto Desktop class and timings class
from pywinauto import Desktop, timings
# Import pywinauto Application class
from pywinauto.application import Application


TOKEN = 'OTgwMzU2MTgxNTUxODkwNDMy.GFY67j.9KKZTELWfRPt8g_NERcutbo_iXUaqJVq4JEqQ4'
DOWNLOAD_DIR = 'C:/Users/Nam/Downloads'
DOCUMENTS_DIR = 'C:/Users/Nam/Documents'
CHANNEL_ID = 985792201751674891
CHANNEL_NAME = 'server_status'
MY_ID = 337341398997270528
IP = 0

loopStarted = False
serverOn = False
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(intents=intents, command_prefix='::')
app = None

def turnOnS():
    global serverOn
    global app
    app = Application().start(r"C:/Users/Nam/Documents/Server/bedrock_server.exe", wait_for_idle=False)
    while not app.is_process_running():
        pass
    serverOn = True


def turnOffS():
    global serverOn
    global app
    main_dlg = app.top_window()
    main_dlg.type_keys('stop{ENTER}')
    while app.is_process_running():
        pass
    serverOn = False


@client.event
async def on_ready():
    global IP
    IP = ip.get()
    await client.get_channel(CHANNEL_ID).send(str(client.user) + ' is active.')


@client.command()
async def turn_on(ctx):
    global serverOn
    if ctx.channel.name == CHANNEL_NAME:
        if not serverOn:
            turnOnS()
            await ctx.send(f'{ctx.message.author.display_name} has turned on the MC server.')
            await ctx.send(f'Server Address: ' + IP)
            await ctx.send(f'Port: 19132')
        else:
            await ctx.send(f'THE SERVER IS ALREADY ON DIPSHIT.')


@client.command()
async def turn_off(ctx):
    global serverOn
    if ctx.channel.name == CHANNEL_NAME:
        if serverOn:
            turnOffS()
            await ctx.send(f'{ctx.message.author.display_name} has turned off the MC server.')
        else:
            await ctx.send(f'THE SERVER IS ALREADY OFF DIPSHIT.')


@client.command()
async def update(ctx, version):
    global serverOn
    global DOWNLOAD_DIR
    global DOCUMENTS_DIR

    if ctx.message.author.id == MY_ID:
        if serverOn:
            await ctx.send(f'The server is on. I cannot update the server you fucking monkey.')
        else:
            r = requests.get('https://minecraft.azureedge.net/bin-win/bedrock-server-' + version + '.zip')
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(DOCUMENTS_DIR + '/newServer/')

            filesToKeep = ['worlds', 'permissions.json', 'server.properties', 'allowlist.json']

            oldFiles = os.listdir(DOCUMENTS_DIR + '/Server')
            for oldFile in oldFiles:
                if (oldFile not in filesToKeep):
                    if ('.' not in oldFile):
                        shutil.rmtree(DOCUMENTS_DIR + '/Server/' + oldFile)
                    else:
                        os.remove(DOCUMENTS_DIR + '/Server/' + oldFile)

            newFiles = os.listdir(DOCUMENTS_DIR + '/newServer')
            for newFile in newFiles:
                if newFile not in filesToKeep:
                    shutil.move(DOCUMENTS_DIR + '/newServer/' + newFile,
                                DOCUMENTS_DIR + '/Server');
            shutil.rmtree(DOCUMENTS_DIR + '/newServer');
            await ctx.send(f'Update done!')
    else:
        await ctx.send(f'STOP TRYING TO UPDATE IT VICTORIA. - Nam')


@client.command()
async def restart(ctx):
    global serverOn
    if ctx.message.author.id == MY_ID:
        if serverOn:
            await ctx.send(f'The server is on. I cannot restart the computer you fucking monkey.')
        else:
            await ctx.send(f'Restarting... Give me 2 minutes.')
            os.system("shutdown /r /t  30")
            quit()
    else:
        await ctx.send(f'STOP TRYING TO FUCKING RESTART MY COMPUTER. - Nam')


@client.command()
async def shutdown(ctx):
    global serverOn
    if ctx.message.author.id == MY_ID:
        if serverOn:
            await ctx.send(f'The server is on. I cannot shutdown the computer you fucking monkey.')
        else:
            await ctx.send(f'I hate you dumb sluts. Goodbye.')
            os.system("shutdown /s /t 30")
            quit()
    else:
        await ctx.send(f'STOP TRYING TO FUCKING SHUTDOWN MY COMPUTER. - Nam')


@client.event
async def on_message(message):
    if (message.author != client.user):
        if "::" in message.content:
            await client.process_commands(message)
        else:
            await message.delete()


client.run(TOKEN)