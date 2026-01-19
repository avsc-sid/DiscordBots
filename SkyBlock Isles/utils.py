import discord
from discord.ext import commands
import requests
import asyncio
import aiohttp
import json


def data():
    with open('data.json', 'r+') as f: 
        return json.load(f)

def skillData():
    with open('data.json', 'r+') as f:
        return json.load(f)["skills"]




def aliases(alias: str):
    alias = alias.lower()
    if alias in ("f", "fish", "fi"): return "fishing"                                                   # Aliases for Fishing
    elif alias in ("farm", "fa", "crop", "harvesting", "harvest", "crops"): return "farming"            # Aliases for Farming
    elif alias in ("m", "mine", "pick", "ore"): return "mining"                                         # Aliases for Mining
    elif alias in ("wood", "log", "w", "foraging", "chop", "axe"): return "woodcutting"                 # Aliases for Woodcutting
    elif alias in ("fast", "giant", "course", "run", "running", "parkour"): return "agility"            # Aliases for Agility
    elif alias in ("a", "sword", "att", "dmg"): return "attack"                                         # Aliases for Attack
    elif alias in ("def", "d", "shield", "armor", "defend"): return "defense"                           # Aliases for Defense
    elif alias in ("str", "brute", "force", "strenght"): return"strength"                               # Aliases for Strength
    elif alias in ("h", "hp", "heart", "apple", "regen"): return "health"                               # Aliases for Health
    elif alias in ("r", "ra", "bow", "arrow", "arr", "archer"): return "range"                          # Aliases for Range
    elif alias in ("mage", "ma", "wand", "wizard"): return "magic"                                      # Aliases for Mage
    #elif alias in ("sl", "slay", "slaying"): return "slayer"                                           # Aliases for Slayer (not released yet)
    elif alias in ("c", "cook", "food", "bake", "baking", "pie"): return "cooking"                      # Aliases for Cooking
    elif alias in ("fletch", "fl", "needle"): return "fletching"                                        # Aliases for Fletching 
    elif alias in ("sm", "ingot", "smelting", "smelt", "smeltery", "hammer"): return "smithing"         # Aliases for Smithing
    elif alias in ("art", "gem", "gemstones", "loom", "jewelry", "arti"): return "artisan"              # Aliases for Artisan
    elif alias in ("alch", "al", "rune", "runeforge", "relic", "pots"): return "alchemy"                # Aliases for Alchemy
    elif alias in ("fishing", "farming", "mining", "woodcutting", "agility", "attack", "defense", "strength", "health", "range", "magic", "slayer", "cooking", "fletching", "smithing", "artisan", "alchemy"): return alias
    else: return None
    

class Get():        
    def Level(skill: str):
        skills = skillData()
        skill = aliases(skill)
        return skills[skill]["level"]

    def XP(skill: str):
        skills = skillData()
        skill = aliases(skill)
        return round(float(skills[skill]["xp"]))

    def LevelAvg():
        skills = skillData()
        a = []
        for i in skills:
            a.append(skills[i]["level"])
        return round(sum(a) / len(a), 2)

    def LevelSum():
        skills = skillData()
        a = []
        for i in skills:
            a.append(skills[i]["level"])
        return sum(a)
    
    def TotalXP():
        skills = skillData()
        a = []
        for i in skills:
            a.append(skills[i]["xp"])
        w = sum(a)
        return Math.RoundToKAndM(w)
    
    def uuid():
        jsonData = data()
        return jsonData["uuid"]

    def XPNL(skill: str):
        skill = aliases(skill)
        skills = skillData()
        lvl = skills[skill]["level"]
        xp = skills[skill]["xp"]
        with open('xpChart.json', 'r+') as f:
            w = json.load(f)[str(lvl + 1)]
            return round(w - xp)

    def XPFNL(skill: str):
        skill = aliases(skill)
        skills = skillData()
        lvl = skills[skill]["level"]
        with open('xpChart.json', 'r+') as f:
            w = json.load(f)
            we = w[str(lvl)]
            wr = w[str(lvl + 1)]
            return wr -  we

    async def Rank(skill):
        skill = f"skills-{aliases(skill)}"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.skyblockisles.com/leaderboards/{skill}/rank/MetaGG2") as resp:
                j = await resp.json()
                return j["rank"]
    
    def Image(name: str):
        name = aliases(name)
        with open('images.json') as f:
            w = json.load(f)
            return w[name]
    
    def ProgressBar(skill: str):
        xpfnl = Get.XPFNL(skill)
        xpnl = Get.XPNL(skill)
        a = [":red_square:",":red_square:",":red_square:",":red_square:",":red_square:",":red_square:",":red_square:",":red_square:",":red_square:", ":red_square:"]
        s = ""
        t = int(round((1 - xpnl / xpfnl) * 10, 0))
        for i in range(t):
            a[i] = ":green_square:"
        for i in a:
            s = s + i
        return s
    
    def Progress(skill: str):
        xpfnl = Get.XPFNL(skill)
        xpnl = Get.XPNL(skill)
        t = round((1 - xpnl / xpfnl) * 100, 1)
        return t


class Math():
    def RoundToKAndM(num):
        w = round(num)
        e = len(str(w))
        if e >= 6:
            s = str(round(num / 1000000, 1))
            w = s + "m"
        elif e >= 3:
            s = str(round(num / 1000, 1))
            w = s + "k"
        return w

class Skills():
    def GetSkills():
        d = {}
        skills = skillData()
        for i in skills:
            d[i] = skills[i]["xp"]
        return d
    
    def Sequencer():
        d = Skills.GetSkills()
        x = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        return x

class Strings():
    def Capitalize(string: str):
        s = string[0:1].upper() + string[1:len(string)]
        return s
