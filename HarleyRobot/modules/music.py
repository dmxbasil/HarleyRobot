import os
import requests
import aiohttp
import youtube_dl

from pyrogram import filters
from HarleyRobot import pbot
from youtube_search import YoutubeSearch



def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@pbot.on_message(filters.command(['song']))
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('🔎 Finding the song...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "✖️ Found Nothing. Sorry.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    m.edit("`Downloading Song... Please wait ⏱`")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎙 **Title**: [{title[:35]}]({link})\n🎬 **Source**: YouTube\n⏱️ **Duration**: `{duration}`\n👁‍🗨 **Views**: `{views}`\n📤 **By**: @@HarleyQuinn_RoBot '
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur)
        m.delete()
    except Exception as e:
        m.edit('❌ Error')
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

        
        import asyncio, time, os, asyncio, json
from telethon.tl.types import DocumentAttributeAudio
from HarleyRobot.events import register
from HarleyRobot.utlis import progress
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,

                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
try:
   from youtubesearchpython import SearchVideos 

except:
	os.system("pip install pip install youtube-search-python")
	from youtubesearchpython import SearchVideos 
	pass

#@register(pattern="^/song (.*)")
async def download_video(v_url):

    lazy = v_url ; sender = await lazy.get_sender() ; me = await lazy.client.get_me()

    if not sender.id == me.id:
        rkp = await lazy.reply("`processing...`")
    else:
    	rkp = await lazy.edit("`processing...`")   
    url = v_url.pattern_match.group(1)
    if not url:
         return await rkp.edit("`Error \nusage song <song name>`")
    search = SearchVideos(url, offset = 1, mode = "json", max_results = 1)
    test = search.result()
    p = json.loads(test)
    q = p.get('search_result')
    try:
       url = q[0]['link']
    except:
    	return await rkp.edit("`failed to find`")
    type = "audio"
    await rkp.edit("`Preparing to download...`")
    if type == "audio":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True    
    try:
        await rkp.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await rkp.edit(f"`Preparing to upload song:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
    elif video:
        await rkp.edit(f"`Preparing to upload song :`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=url,
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")


@register(pattern="^/video (.*)")
async def download_video(v_url):  
    lazy = v_url ; sender = await lazy.get_sender() ; me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`processing...`")
    else:
    	rkp = await lazy.edit("`processing...`")   
    url = v_url.pattern_match.group(1)
    if not url:
         return await rkp.edit("`Error \nusage song <song name>`")
    search = SearchVideos(url, offset = 1, mode = "json", max_results = 1)
    test = search.result()
    p = json.loads(test)
    q = p.get('search_result')
    try:
       url = q[0]['link']
    except:
    	return await rkp.edit("`failed to find`")
    type = "audio"
    await rkp.edit("`Preparing to download...`")
    if type == "audio":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True
    try:
        await rkp.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await rkp.edit(f"`Preparing to upload song `\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await rkp.edit(f"`Preparing to upload video song :`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await rkp.delete()
        
