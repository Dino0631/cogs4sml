
"""
The MIT License (MIT)
Copyright (c) 2017 Dino
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __main__ import send_cmd_help
import requests
import os
import time
import discord
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import urllib
import urllib.request 
import asyncio
import aiohttp
from .utils.dataIO import dataIO
from cogs.utils import checks
import locale

racfclans = {
	"ALPHA" : "2CCCP",
	"BRAVO" : "2U2GGQJ",
	"CHARLIE" : "2QUVVVP",
	"DELTA" : "Y8GYCGV",
	"ECHO" : "LGVV2CG",
	"ESPORTS" : "R8PPJQG",
	"FOXTROT" : "QUYCYV8",
	"GOLF" : "GUYGVJY",
	"HOTEL" : "UGQ28YU",
	"MINI" : "22LR8JJ2",
	"MINI2" : "2Q09VJC8"
}
racfclanslist = [
	"Alpha",
	"Bravo",
	"Charlie",
	"Delta",
	"Echo",
	"Foxtrot",
	"Golf",
	"Hotel",
	"eSports",
	"Mini",
	"Mini2"
]
BOTCMDER = ["Bot Commander"]
NUMITEMS = 9
statscr_url = "http://statsroyale.com/profile/"
crapiurl = 'http://api.cr-api.com'
statsurl = 'http://statsroyale.com'
# PATH = os.path.join("data", "crtags")
# SETTINGS_JSON = os.path.join(PATH, "settings.json")
# BACKSETTINGS_JSON = os.path.join(PATH, "backsettings.json")
# CLAN_JSON = os.path.join(PATH, "clan.json")
# SET_JSON = os.path.join(PATH, "set.json")
validChars = ['0', '2', '8', '9', 'C', 'G', 'J', 'L', 'P', 'Q', 'R', 'U', 'V', 'Y']
tags = {}

async def async_refresh(url):
	async with aiohttp.get(url) as r:
		# response = await r.json()
		a = 1
		
class CRClan:

	def __init__(self):
		self.a = 1

	@classmethod
	async def create(self, tag):
		# tag2id = dataIO.load_json(BACKSETTINGS_JSON)
		self.member_count = 0                           #done
		self.members = []                               #done
		self.clan_tag = tag                             #done
		self.clan_url = crapiurl + '/clan/' + tag       #done
		self.clanurl = self.clan_url.replace('api.', '', 1)#done
		self.tr_req = '0'                               #done
		self.clan_trophy = ''                           #done
		self.name = ''                                  #done
		self.donperweek = ''							#done
		self.desc = ''									#done
		self.clan_badge = ''							#done
		self.leader = {}								#done
		self.size = 0									#done
		self.coleaders = []								#done
		self.elders = []								#done
		self.norole = []								#done
		# if clan_url != '':
		async with aiohttp.ClientSession() as session:
			async with session.get(self.clan_url) as resp:
				datadict = await resp.json()
		
		# for x in datadict:
		# 	try:
		# 		print(x)
		# 	except:
		# 		print('some key')
		# 	try:
		# 		print(datadict[x])
		# 	except:
		# 		print('some value')
		# for member in datadict['members']:
		# 	try:
		# 		print(member)
		# 	except:
		# 		print('some member')
		# r = requests.get(self.clan_url, headers=headers)
		# html_doc = r.text

		for i, m in enumerate(datadict['members']):
			rank = str(m['currentRank'])
			name = str(m['name'])
			tag = str(m['tag']).upper()
			url = crapiurl +'/profile/'+ tag
			level = str(m['expLevel'])
			trophy = str(m['score'])
			donations = str(m['donations'])
			role = str(m['roleName'])
			# if tag in tag2id:
			# 	userid = tag2id[tag]
			# else:
			userid = ''
			memberdict = {
				'name' : name.strip(),
				'rank' : rank.strip(),
				'tag' : tag.strip(),
				'userid': userid.strip(),
				'url' : url.strip(),
				'level' : level.strip(),
				'trophy' : trophy.strip(),
				'donations' : donations.strip(),
				'role' : role.strip()
			}
			memberdict['formatted'] = '`'+ memberdict['role']+'` ' + memberdict['name']+' [`#'+memberdict['tag']+'`]('+memberdict['url'].replace('api.', '', 1)+')'
			if memberdict['userid'] != '':
				try:
					memberdict['formatted'] += ' <@'+memberdict['userid'] + '>'
				except:
					pass
			if memberdict['role'] == 'Co-Leader':
				self.coleaders.append(memberdict)
			if memberdict['role'] == 'Member':
				self.norole.append(memberdict)
			if memberdict['role'] == 'Elder':
				self.elders.append(memberdict)
			if memberdict['role'] == 'Leader':
				self.leader = memberdict
			self.size += 1
			self.members.append(memberdict)

		self.clan_badge = crapiurl + datadict['badge_url']
		self.name = datadict['name']
		self.desc = datadict['description']
		d = self.desc
		# discordlink = d[d.find('discord.'):d[d.find('discord.'):].find(' ')+d.find('discord.')]
		d2 = d#.replace(discordlink, "[{}]({})".format(discordlink, 'https://'+discordlink))

		i = 0
		index = 0
		# print(d2[-15:])
		count = d2.lower().count('discord.')
		# print(count)
		while i<count:
			index = d2.lower().find('discord.', index+1)
			# print(index)
			# print(d2[index:index+len('discord.')])
			d4 = d2.replace(d2[index:index+len('discord.')], 'discord.')
			d3 = d4[index:]
			# print(d3.find('discord.'))
			# print(d3)
			# print()
			# print()
			# print()
			endlink = d3[d3.find('discord.'):].find(' ')
			if endlink == -1:
				endlink = len(d3)
			discordlink = d3[d3.find('discord.'):endlink+d3.find('discord.')]
			# print(discordlink)
			# print(d2[index:index+len(discordlink)])
			d2 = d2.replace(d2[index:index+len(discordlink)], " [{}](https://{})".format(d2[index:index+len(discordlink)], discordlink))

			# print(d2)
		# 	if i>10:
		# 		return
			i += 1
		sym = '#'
		numtagsind2 = 0
		tagsind2 = []
		index = 0
		i = 0
		while i<d2.count(sym):
			index = d2.find(sym, index+1)
			x = ''
			i2 = 1
			thing = ''
			while x != ' ':
				thing += x
				x = d2[index+i2]
				i2 += 1
			valid = True
			n = 0
			thing2 = ''
			for l in thing:
				if l not in validChars:
					if n>4 and not l.isalnum():
						valid = True
					else:
						valid = False
					break
				thing2 += l
				n+=1
			if valid and len(thing2)>4:
				numtagsind2 += 1
				tagsind2.append(thing2)
			i += 1
		for tag in tagsind2:
			tag = tag.replace(sym, '')
			d2 = d2.replace(sym+tag, '[{}]({})'.format(sym+tag, 'https://cr-api.com/clan/'+tag))
		self.desc2 =  d2
		self.clan_trophy = datadict['score']
		self.tr_req = datadict['requiredScore']
		self.donperweek = datadict['donations']
		return self




class CRTags:

	def __init__(self, bot):
		self.bot = bot
		self.emojiservers = []
		for server in bot.servers:
			self.emojiservers.append(server)
		self.cremojis = {}
		for server in self.emojiservers:
			for emoji in server.emojis:
				self.cremojis[emoji.name] = "<:{}:{}>".format(emoji.name,emoji.id)


	async def keyortag2tag(self, keyortag, ctx):
		originalkey = keyortag
		keyortag = keyortag.upper()
		members = list(ctx.message.server.members)
		membernames = []
		memberswithdiscrim = []
		for member in members:
			membernames.append(member.name)
			memberswithdiscrim.append(member.name + '#' + str(member.discriminator))
		userid = None
		tag = ''
		valid = True
		for letter in keyortag:
			if letter not in validChars:
				valid = False
				break
		if keyortag in racfclans:
			tag = racfclans[keyortag]
		elif valid:
			tag = keyortag
		elif keyortag.startswith('<@'): #assume mention
			userid = keyortag[2:-1]
			userid = userid.replace('!', '')
		elif keyortag.isdigit(): #assume userid
			userid = keyortag
		elif originalkey in members or originalkey in membernames or originalkey in memberswithdiscrim:	#if user in members
			for member in members:
				name = member.name
				if keyortag == member:
					userid = member.id
				elif keyortag == name:
					userid = member.id
					break
				elif keyortag == name + '#' + member.discriminator:
					userid = member.id
					break
		else:
			await self.bot.say('`{}` is not in the database, nor is an acceptable tag.'.format(keyortag))
			return
		# if userid != None:
		# 	try:
		# 		usertag = self.settings[userid]
		# 	except KeyError:
		# 		await self.bot.say("That person is not in the database")
		# 		return None
		# 	player = await CRPlayer.create(usertag)			
		# 	tag = player.clan_url.replace(statsurl,'').replace('/clan/', '')
		return tag

	@commands.command(aliases=['tra'], pass_context=True)
	async def trapi(self,ctx,clan=None):
		uclan = None
		if clan != None:
			uclan = clan.upper()
		if clan == None:
			clan = racfclanslist
		elif uclan not in racfclans:
			await self.bot.say("the clan, *\u200b{}* is not in racf".format(clan))
			return
		if type(clan) == type(['list']):
			await self.bot.send_typing(ctx.message.channel)
			em = discord.Embed(color=discord.Color(0xFF3844), title="RACF requirements:")
			for c in clan:
				for racfc in racfclanslist:
					if racfc.lower() == c.lower():
						goodcapsclan = racfc
						break
				tag = await self.keyortag2tag(c, ctx)
				clan_data = await CRClan.create(tag)
				trophyreq = await self.parsereq(clan_data.desc)
				if trophyreq==None:
					trophyreq = clan_data.tr_req
				if goodcapsclan == 'eSports':
					trophyreq = self.cremojis['gitgud']
				em.add_field(name="{}:".format(goodcapsclan), value=trophyreq)

		else:
			tag = await self.keyortag2tag(clan, ctx)
			clan_data = await CRClan.create(tag)
			# clan_data.desc = "WE are reddit delta, we require a pb 4500 and our feeder is reddit echo"
			#uncomment the above line to test the pb detection
			trophyreq = await self.parsereq(clan_data.desc)
			if trophyreq==None:
				trophyreq = clan_data.tr_req
			for c in racfclanslist:
				if c.lower() == clan.lower():
					goodcapsclan = c
					break
			if goodcapsclan == 'eSports':
				trophyreq = self.cremojis['gitgud']
			em = discord.Embed(color=discord.Color(0xFF3844), url=clan_data.clanurl,title="{} trophy req:".format(goodcapsclan), description=trophyreq)

		await self.bot.say(embed=em)

	async def parsereq(self, desc):
		trophynums = []
		n = 0
		for l in desc:
			try:
				if l.isdigit() or (l.lower()=='p' and desc[n+1].lower()=='b')or (l.lower()=='b' and desc[n-1].lower()=='p') or l.lower() == 'o' or l == ',':
					if l !=',':
						trophynums.append(l)
				elif trophynums[len(trophynums)-1] != " ":
					trophynums.append(' ')
			except IndexError:
				pass
			n+=1
		n = 0
		trnums = ''.join(trophynums)
		trnums = trnums.split(' ')
		while n<len(trnums):
			trnums[n] = trnums[n].replace('O', '0').replace('o', '0')
			d = trnums[n]
			# print("trnums: {}".format(trnums))
			# print("{}, len: {}".format(d, len(d)))
			if len(d) == 4 or d.lower() =='pb':
				if d.isdigit():
					trnums[n] = "{:,}".format(int(d))
				n += 1
			else:
				trnums.remove(d)
		n = 0
		trophyreq = None
		if len(trnums)==0:
			trnums = None
		elif len(trnums) == 1:
			trnums = trnums[0]
		elif len(trnums)==2:
			n = 0
			while n<len(trnums):
				if trnums[n].isdigit():
					trnums[n] = "{:,}".format(int(d))
				n+=1
			trnums = ' '.join(trnums)
		parseddesc = trnums
		if parseddesc == None:
			trophyreq = None
		if type(parseddesc) == type('string'):
			trophyreq = parseddesc
		elif type(parseddesc) == type(['list']):
			trreqs =''
			n = 0
			for d in parseddesc:
				trreqs +=d 
				# print("parseddesc len: {}\nn: {}\nnextone: {}".format(len(parseddesc) ,n, parseddesc[n+1].lower()))
				try:
					if n !=len(parseddesc)-1 and parseddesc[n+1].lower()!='pb':
						trreqs += ', '
					else:
						trreqs += ' '
				except IndexError:
					pass
				n+=1
			trophyreq = trreqs
		return trophyreq



	
def setup(bot):
	bot.add_cog(CRTags(bot))
