import discord
from discord.ext import commands
import aiohttp
import locale

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

        params = {'raw_paste': items_rejoin, 'market': '30000142'}
        #await self.bot.say(items_rejoin)
        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                   data=params) as response:
                soupObject = BeautifulSoup(await response.text(), "html5lib")
            try:
                results = soupObject.find(id='results').tfoot.get_text()
                resultsLink = soupObject.find('a[href*="evepraisal.com/e/"]')
                results = results.replace('\n', ' ')
                results = results.replace('\t', ' ')
                whitelist = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\.')
                results = ''.join(filter(whitelist.__contains__, results))
                for counter in range(1,100):
                    results = results.replace('  ', ' ')
                results_split = results.split(' ')
                sellvalue = results_split[9].split('.')[0]
                buyvalue = results_split[10].split('.')[0]
                sizem = results_split[11]
                sizem = sizem.replace('m3','')
                results_joined = ' '.join(results_split[1:4]) + ':\t' + "{:,.2f}".format(float(sellvalue)) + ' isk\n' + ' '.join(results_split[4:7]) + ':\t' + "{:,.2f}".format(float(buyvalue)) + ' isk\n' + ' '.join(results_split[7:9]) + ':\t\t' + "{:,.2f}".format(float(sizem)) + " m3"
                await self.bot.say('Link: ' + resultsLink + ' \n ' + results_joined)
                #await self.bot.say('Results: \n' + results_joined)
            except:
                await self.bot.say("Failed.")



def setup(bot):
    if soupAvailable:
        bot.add_cog(Mycog(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")