import discord
from discord.ext import commands
import aiohttp

try: # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("I can do stuff!")




    @commands.command(pass_context=True)
    async def evepraisal(self, ctx):
        """Run evepraisal and spit out result"""

        #Your code will go here
        url = "http://evepraisal.com/estimate" #build the web adress

        items = ctx.message.content

        items_split = items.split(" ")
        items_rejoin = " ".join(items_split[1:])

        params = {'raw_textarea': items_rejoin, 'market': '30000142', 'load_full': '1'}
        await self.bot.say(items_rejoin)
        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                   data=params) as response:
                soupObject = BeautifulSoup(await response.text(), "html.parser")
            try:
                #results = soupObject.find(id='results').get_text()
                results = soupObject.body.get_text()
                await self.bot.say(results)
            except:
                await self.bot.say("Failed.")



def setup(bot):
    if soupAvailable:
        bot.add_cog(Mycog(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")