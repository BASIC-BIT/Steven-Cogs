import discord
from discord.ext import commands
import aiohttp

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
    async def evepraisal(self, *text):
        """Run evepraisal and spit out result"""

        #Your code will go here
        url = "http://evepraisal.com/estimate/post" #build the web adress

        params = {'raw_textarea': ' '.join(text[0::len(text)]), 'market': '30000142', 'load_full': '1'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url,
                                   params=params) as response:
                soupObject = BeautifulSoup(await response.text(), "html.parser")
            try:
                results = soupObject.find(id='results').get_text()
                await self.bot.say(results)
            except:
                await self.bot.say("Failed.")



def setup(bot):
    bot.add_cog(Mycog(bot))