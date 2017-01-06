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




    @commands.command()
    async def evepraisal(self, **text):
        """Run evepraisal and spit out result"""

        #Your code will go here
        url = "http://evepraisal.com/estimate" #build the web adress

        params = {'raw_textarea': '\t'.join(text[1::len(text)]), 'market': '30000142', 'load_full': '1'}
        self.bot.say('\t'.join(text[1::len(text)]))
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