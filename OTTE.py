import discord
import asyncio
import requests
import random
from urllib import parse
#import
from urllib.request import urlopen
from discord.ext import commands
from bs4 import BeautifulSoup

#info
client = commands.Bot(command_prefix='오트 ')
token = "ODAwMDU2NDMyNzE2MjgzOTc3.YAMknQ.MbQj25EvaMcpUZPZv_YRAyuacRA"

#start
@client.event
async def on_ready():
    print("")
    print("==================")
    print("")
    print(client.user.name)
    print(client.user.id)
    print("")
    print("==================")
    print("")

    game = discord.Game("BETA")
    await client.change_presence(status=discord.Status.dnd, activity=game)

#.event
@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content == "오트 실검":
        url = "https://m.search.naver.com/search.naver?query=%EC%8B%A4%EA%B2%80"
        html = urlopen(url)
        parse = BeautifulSoup(html, "html.parser")
        result = ""
        tags = parse.find_all("span", {"class": "tit_keyword"})
        for i, e in enumerate(tags):
            result = result + (str(i+1)) + "위|" + e.text + "\n"
            await message.channel.send(result)

    #인사
    list = ["안뇽", "안뇽~", "ㅎㅇ", "ㅎㅇ~", "안녕", "안녕~", "반가워", "반가워~"]
    menu = random.choice(list)
    if message.content == "오트 안녕":
        await message.channel.send(menu)

    #오트
    if message.content == "오트":
        await message.channel.send('오트사용법을 알고싶으시다면\n`"오트 명령어"`를 입력하여주세요.')

    #핑
    if message.content == "오트 핑":
        la = client.latency
        await message.channel.send(f'**`[ {str(round(la * 1000))}ms ]`**')

    #공지
    if message.content == "오트 공지":
        embed = discord.Embed(title="NOTICE", description="", color=0xcb68ff)
        embed.add_field(name="패드립x", value="[ 3 ]", inline=True)
        embed.add_field(name="섹드립x", value="[ 2 ]", inline=True)
        embed.add_field(name="시비x", value="[ 1 ]", inline=True)
        embed.set_footer(text="누적숫자 5 번 채워지면 추방, 7 번 채워지면 BAN 입니다.")
        await message.channel.send(embed=embed)

    #명령어
    if message.content == "오트 명령어":
        embed = discord.Embed(title="COMMAND", description="", color=0xcb68ff)
        embed.add_field(name='`"오트 공지"`', value="> 공지를 보여줍니다.", inline=False)
        embed.add_field(name='`"오트 명령어"`', value="> 사용가능한 명령어를 보여줍니다.", inline=False)
        embed.add_field(name='`"오트 핑"`', value="> 오트의 핑을 보여줍니다.", inline=False)
        embed.add_field(name='`"오트 청소"`', value="> 채팅을 청소하여줍니다.", inline=False)
        embed.add_field(name='`"오트 코로나"`', value="> 코로나 현재 상황을 보여줍니다.", inline=False)

        embed.set_footer(text="")
        await message.channel.send(embed=embed)

    #청소
    if message.content.startswith("오트 청소"):
        if message.author.guild_permissions.manage_messages:
            try:
                amount = message.content[6:]
                await message.channel.purge(limit=int(amount))
                await message.channel.send(f"**[ {amount} ]** 개의 메시지를 청소하였습니다.")
            except ValueError:
                await message.channel.send("청소하실 메시지의 **[ 갯수 ]** 를 입력해 주세요.")
        else:
            await message.channel.send("**[ 권한 ]** 이 없습니다.")

    #message
    if message.content == "오트 코로나":
        res = requests.get("http://ncov.mohw.go.kr/").text
        soup = BeautifulSoup(res, "html.parser")

        #국내, 해외 발생 리스트
        ko_v = soup.find("div", attrs={"class":"datalist"}).find_all("span", attrs={"class":"data"})
        kov_list = []
        for kov in ko_v:
            kov_list.append(kov.get_text())

        #확진자[0], 격리해제[1], 치료중[2], 사망[3] 리스트
        all_per = soup.find("ul", attrs={"class":"liveNum"}).find_all("span", attrs={"class":"num"})
        all_per_list = []
        for allper in all_per:
            all_per_list.append(allper.get_text().replace("(누적)", ""))

        #전일대비 리스트
        before_per = soup.find("ul", attrs={"class":"liveNum"}).find_all("span", attrs={"class":"before"})
        before_per_list = []
        for beforper in before_per:
            before_per_list.append(beforper.get_text().replace("전일대비 ", ""))

        #최신 브리핑 리스트
        new_briefing = soup.find("ul", attrs={"class":"m_text_list"}).find_all("a")
        new_briefing_list = []
        for briefing in new_briefing:
            new_briefing_list.append(briefing.get_text())    # [0]
            new_briefing_list.append(briefing["href"])    # [1]

        #00월 00일 00시 기준
        whentotaldata = soup.find("span", attrs={"class":"livedate"}).get_text().strip().replace("(", "").replace(")", "").replace(", ", " | ")

        #임베드
        embed = discord.Embed(title="코로나 19 현황", description="", color=0xff0000)
        embed.set_author(name="코로나 바이러스 감염증 - (COVID-19)", url="http://ncov.mohw.go.kr/", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
        embed.add_field(name="Last data time", value="**" + whentotaldata + "**", inline=False)
        embed.add_field(name="`총 확진환자`", value=all_per_list[0] + before_per_list[0] , inline=True)
        embed.add_field(name="`완치환자`", value=all_per_list[1] + before_per_list[1], inline=True)
        embed.add_field(name="`치료 중(격리 중)`", value=all_per_list[2] + before_per_list[2], inline=True)
        embed.add_field(name="`사망자`", value=all_per_list[3] + before_per_list[3], inline=True)
        embed.add_field(name="`국내발생`", value="+ " + kov_list[0], inline=True)
        embed.add_field(name="`해외발생`", value="+ " + kov_list[1], inline=True)
        embed.add_field(name="`최신 브리핑`", value="[{}](http://ncov.mohw.go.kr{})".format(new_briefing_list[0], new_briefing_list[1]) + "\n"
                                                + "[{}](http://ncov.mohw.go.kr{})".format(new_briefing_list[2], new_briefing_list[3]) , inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
        embed.set_footer(text="자세한 정보는 위의 사이트를 방문해주세요.", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789098688315654164/Flag_of_South_Korea.png")
        await message.channel.send(embed=embed)

client.run(token)
