import discord
from discord.ext import commands
import aiohttp
import locale
import re
from cogs.audio import Audio

try: # check if BeautifulSoup4 is installed
    from bs4 import BeautifulSoup
    soupAvailable = True
except:
    soupAvailable = False

class StevenCog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

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
                soupObject = BeautifulSoup(await response.text(), "html.parser")
            try:
                results = soupObject.find(id='results').tfoot.get_text()
                link = soupObject.find_all('a')[1].get_text()

                whitelist = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\.')
                results = ''.join(filter(whitelist.__contains__, results))
                results = re.sub(' +',' ',results)

                results_split = results.split(' ')
                sellvalue = results_split[9].split('.')[0]
                buyvalue = results_split[10].split('.')[0]
                sizem = results_split[11]
                sizem = sizem.replace('m3','')
                results_joined = ' '.join(results_split[1:4]) + ':\t' + "{:,.2f}".format(float(sellvalue)) + ' isk\n' + ' '.join(results_split[4:7]) + ':\t' + "{:,.2f}".format(float(buyvalue)) + ' isk\n' + ' '.join(results_split[7:9]) + ':\t\t' + "{:,.2f}".format(float(sizem)) + " m3"
                
                await self.bot.say('Link: ' + link + ' \n' + results_joined)
                #await self.bot.say('Results: \n' + results_joined)
            except:
                await self.bot.say("Failed.")

    @commands.command(pass_context=True)
    async def vox(self, sid, ctx, *args: str):
        for word in args:
            await ctx.invoke(self.bot.get_cog('Audio')._guarantee_downloaded, server=self.bot.get_server(sid), url='http://ddmers.com/vox/'+word+'.mp3')
            await ctx.invoke(self.bot.get_cog('Audio')._add_to_queue, server=self.bot.get_server(sid), url='http://ddmers.com/vox/'+word+'.mp3')

def setup(bot):
    if soupAvailable:
        bot.add_cog(StevenCog(bot))
    else:
        raise RuntimeError("You need to run `pip3 install beautifulsoup4`")