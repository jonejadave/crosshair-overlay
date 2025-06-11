# main.py

import sys
from PyQt5 import QtWidgets
from Crosshair import FullScreenCrosshair
import discord
import threading

class DiscordBot(discord.Client):
    def __init__(self, crosshair, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crosshair = crosshair

    async def on_ready(self):
        print(f'✅ Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.lower() == '!roll':
            print("🎯 Rolling...")
            self.crosshair.roll_requested.emit()
            await message.channel.send("Rolling a new crosshair...")

def start_discord_bot(crosshair):
    intents = discord.Intents.default()
    intents.message_content = True
    client = DiscordBot(crosshair, intents=intents)
    client.run("key_here")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    crosshair = FullScreenCrosshair()

    # Start Discord bot in a separate thread
    threading.Thread(target=start_discord_bot, args=(crosshair,), daemon=True).start()

    sys.exit(app.exec_())
