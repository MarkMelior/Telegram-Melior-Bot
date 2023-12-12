
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import var
from aiogram.dispatcher import FSMContext
import functions
from aiogram.dispatcher.filters.state import State, StatesGroup

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import aiohttp
import io
import time
import asyncio
import logging
import functools



# Демотиватор 2.0
async def demotivator(msg: types.Message):
    if msg.attachments:
        attachment = msg.attachments[0]
        if attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg") or attachment.filename.endswith(".png") or attachment.filename.endswith(".webp"):
            if msg.content:
                url = str(msg.attachments[0]) # must be an image
                async with aiohttp.ClientSession() as session: # creates session
                    async with session.get(url) as resp: # gets image from url
                        img = await resp.read() # reads image from response
                        with io.BytesIO(img) as file: # converts to file-like object
                            template = Image.open('assets/demotivator/template.jpg')
                            mem = Image.open(file).convert('RGBA')
                            text = msg.content

                            width = 610
                            height = 569
                            resized_mem = mem.resize((width, height), Image.ANTIALIAS)

                            text_position = (0, 0)
                            text_color = (266,0,0)


                            strip_width, strip_height = 700, 1300

                            def findLen(text_len):
                                counter = 0    
                                for i in text_len:
                                    counter += 1
                                return counter

                            font_width = 60
                            
                            if findLen(text) >= 25:
                                font_width = 50

                            background = Image.new('RGB', (strip_width, strip_height)) #creating the black strip
                            draw = ImageDraw.Draw(template)

                            if '\n' in text:  
                                split_offers = text.split('\n')

                                for i in range(2):
                                    if i == 1:
                                        strip_height += 110
                                        font_width -= 20
                                    font = ImageFont.truetype("assets/demotivator/font.ttf", font_width) 
                                    text_width, text_height = draw.textsize(split_offers[i], font)

                                    position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                                    draw.text(position, split_offers[i], font=font)
                            else:
                                font = ImageFont.truetype("assets/demotivator/font.ttf", font_width)
                                text_width, text_height = draw.textsize(text, font)
                                strip_height = 1330
                                position = ((strip_width-text_width)/2,(strip_height-text_height)/2)
                                draw.text(position, text, font=font)


                            template.paste(resized_mem, (54, 32),  resized_mem)
                            buffer = io.BytesIO()
                            template.save(buffer, format='JPEG', quality=75)
                            buffer.seek(0)

                            await msg.delete()
                            emb = nextcord.Embed( description = f'{msg.author.mention} Ваш демик готов!', color = 0xd7d7d7 )
                            emb.set_author( name = msg.author, icon_url = msg.author.avatar )
                            emb.set_footer(text = f'Текст: {msg.content}')
                            emb.set_image(url="attachment://MeliorLive.jpeg")
                            await msg.channel.send( file = nextcord.File(buffer, "MeliorLive.jpeg"), embed = emb )
                            return
            else:
                await msg.delete()
                emb = nextcord.Embed( description = '❌ Ты забыл добавить подпись', color = cError )
                emb.set_author( name = msg.author, icon_url = msg.author.avatar )
                await msg.channel.send( embed = emb, delete_after = 10 )
                return
        else:
            await msg.delete()
            emb = nextcord.Embed( description = '❌ Неверный формат фото! ```Поддерживаемые форматы: [.jpg, .png, .jpeg, .webp]```', color = cError )
            emb.set_author( name = msg.author, icon_url = msg.author.avatar )
            await msg.channel.send( embed = emb, delete_after = 10 )
    else:
        await msg.delete()
        emb = nextcord.Embed( description = 'Отправь мне фото с подписью', color = cError )
        emb.set_author( name = msg.author, icon_url = msg.author.avatar )
        await msg.channel.send( embed = emb, delete_after = 10 )