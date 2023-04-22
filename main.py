import time
from twitchio.ext import commands

# Read auth data from auth.txt file
oauth_token = ""
channel_name = ""

with open("auth.txt") as f:
    f = f.readlines()
    oauth_token = f[0].replace("\n", "").replace(" ", "")
    channel_name = f[1].replace("\n", "").replace(" ", "")

# Bot class
class Bot(commands.Bot):

    # Initialize bot
    def __init__(self):
        self.msg_queue = []
        self.cool_down = time.time()-100
        super().__init__(token=oauth_token, prefix='!', initial_channels=[channel_name])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Ignore self messages
        if message.echo:
            return
        
        # Ignore message if bot is on cooldown
        if time.time() - self.cool_down < 90:
            return

        # Handle a !play message
        if(message.content == "!play"):
            t = time.time()
            
            # Remove messages recive more than 30 seconds ago
            while len(self.msg_queue)>0 and t - self.msg_queue[0] > 30:
                self.msg_queue.pop(0)
                
            # Add current message to queue
            self.msg_queue.append(t)
            
            # If there are 5 messages in the last 30 seconds send !play message, start cooldown, and clear queue
            if(len(self.msg_queue) >= 5):
                self.msg_queue = []
                self.cool_down = time.time()
                await message.channel.send("!play")
                print(" > !Play")
                

bot = Bot()
bot.run()