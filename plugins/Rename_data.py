from helper.utils import progress_for_pyrogram, convert
from pyrogram import Client, filters
from pyrogram.types import (  InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os 
import humanize
from PIL import Image
import time

THUMB_1 = os.environ.get("THUMBNAIL_1", None)
THUMB_2 = os.environ.get("THUMBNAIL_2", None)

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot,update):
	try:
           await update.message.delete()
           await update.answer("process cancelled β")
	except:
           return
	

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    await message.reply_text(
       text=f"""π Hai {message.from_user.mention} \nπΈ'π π° ππππππ π΅πππ ππππππ+π΅πππ ππ πππππ π²πππππππ π±πΎπ ππππ πΏππππππππ πππππππππ!\n\nI can work only Some groups""",
       reply_markup=InlineKeyboardMarkup( [[
           InlineKeyboardButton("π  π₯ππ π‘ππ π€π½πππππ π ", url='https://t.me/github_noob'),
           ],[
           InlineKeyboardButton("β π’πΊππΌπΎπ", callback_data='cancel')
           ]]
       )
    )

@Client.on_message(filters.group & filters.command(["help"]))
async def help(client, message):
    await message.reply_text(
       text=f"""π Hai {message.from_user.mention}.!

<i><b><u>My helps</u></b></i>

**You don't need to use any extension.
If you want another extension use like this :-** `!AVC`

<i><b><u>Default extinctions</u></b></i>
β’ document :- .MKV
β’ video :- .MP4
β’ audio :- .MP3

<i><b><u>My commands</u></b></i>

/start - check alive (in PM)
/help - for this message (group only)

<i><b>Thumbnail 1</b></i>

/rename - Rename as document (group only)
/rvid - Rename as stream file (group only)
/raud - Rename as audio (group only)

<i><b>Thumbnail 2</b></i>

/rename2 - Rename as document (group only)
/rvid2 - Rename as stream file (group only)
/raud2 - Rename as audio (group only)**""",
       reply_markup=InlineKeyboardMarkup(
           [[
           InlineKeyboardButton("π  π₯ππ π‘ππ π€π½πππππ π ", url='https://t.me/github_noob')
           ],[
           InlineKeyboardButton("β π’πΊππΌπΎπ", callback_data='cancel')
           ]]
       )
    )

@Client.on_message(filters.photo)
async def photoid(client, message):     
    await message.reply(
        text=f"**PHOTO ID** :- \n `{message.photo.file_id}`"
    )


@Client.on_message(filters.group & filters.command(["rdoc", "rename"]))
async def doc(bot,update):
     if not update.reply_to_message:
         return await update.reply("**Reply to a Media :)**")
     if not update.reply_to_message.media:
         return await update.reply("**Reply to a Media :(**")
     if len(update.command) == 1:
         return await update.reply("**Give me a new file name for Rename :)**")
     #type = update.data.split('_')[1]
     #new_name = update.message.text
     #new_filename = new_name.split(":-")[1]
     new_filename = update.text.split(" ", 1)[1]
     if not "!" in new_filename:
        new_filename = new_filename + ".mkv"
     else:
        new_filename = new_filename.replace("!", ".")
     file_path = f"downloads/{new_filename}"
     #file = update.message.reply_to_message
     file = update.reply_to_message
     #ms = await update.message.edit("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     ms = await update.reply_text(text="ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     #user_id = int(update.message.from_user.id)
     user_id = int(update.from_user.id)
     ph_path = None
     #data = find(update.message.from_user.id)
     media = getattr(file, file.media.value)
     c_thumb = THUMB_1
     new_cap = new_filename.replace("!", ".")
     caption = f"**__{new_cap}__**\n\n**__Uploaded By : @MovieJunctionGrp__** π₯"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit(text="ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....")
     c_time = time.time() 
     try:
         await update.reply_document(
             document=file_path,
             thumb=ph_path, 
             caption=caption, 
             progress=progress_for_pyrogram,
             progress_args=( "ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....",  ms, c_time   ))
     except Exception as e: 
         await ms.edit(f"{e}")
         print(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 

@Client.on_message(filters.group & filters.command("rvid"))
async def vid(bot,update):
     if not update.reply_to_message:
         return await update.reply("**Reply to a Media :)**")
     if not update.reply_to_message.media:
         return await update.reply("**Reply to a Media :(**")
     if len(update.command) == 1:
         return await update.reply("**Give me a new file name for Rename :)**")
     #type = update.data.split('_')[1]
     #new_name = update.message.text
     #new_filename = new_name.split(":-")[1]
     new_filename = update.text.split(" ", 1)[1]
     if not "!" in new_filename:
        new_filename = new_filename + ".mp4"
     else:
        new_filename = new_filename.replace("!", ".")
     file_path = f"downloads/{new_filename}"
     #file = update.message.reply_to_message
     file = update.reply_to_message
     #ms = await update.message.edit("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     ms = await update.reply("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     #user_id = int(update.message.from_user.id)
     user_id = int(update.from_user.id)
     ph_path = None
     #data = find(update.message.from_user.id)
     media = getattr(file, file.media.value)
     c_thumb = THUMB_1
     new_cap = new_filename.replace("!", ".")
     caption = f"**__{new_cap}__**\n\nUploaded By : @MovieJunctionGrp__** π₯"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit("ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ...")
     c_time = time.time() 
     try:
         await update.reply_video(
             video=file_path,
	     caption=caption,
	     thumb=ph_path,
	     duration=duration,
	     progress=progress_for_pyrogram,
	     progress_args=( "ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....",  ms, c_time))
     except Exception as e: 
         await ms.edit(f"{e}")
         print(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 

@Client.on_message(filters.group & filters.command("raud"))
async def aud(bot,update):
     if not update.reply_to_message:
         return await update.reply("**Reply to a Media :)**")
     if not update.reply_to_message.media:
         return await update.reply("**Reply to a Media :(**")
     if len(update.command) == 1:
         return await update.reply("**Give me a new file name for Rename :)**")
     #type = update.data.split('_')[1]
     #new_name = update.message.text
     #new_filename = new_name.split(":-")[1]
     new_filename = update.text.split(" ", 1)[1]
     if not "!" in new_filename:
        new_filename = new_filename + ".mp3"
     else:
        new_filename = new_filename.replace("!", ".")
     file_path = f"downloads/{new_filename}"
     #file = update.message.reply_to_message
     file = update.reply_to_message
     #ms = await update.message.edit("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     ms = await update.reply("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     #user_id = int(update.message.from_user.id)
     user_id = int(update.from_user.id)
     ph_path = None
     #data = find(update.message.from_user.id)
     media = getattr(file, file.media.value)
     c_thumb = THUMB_1
     new_cap = new_filename.replace("!", ".")
     caption = f"**__{new_cap}__**\n\n**__Uploaded By : @MovieJunctionGrp__** π₯"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit("ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....")
     c_time = time.time() 
     try:
         await update.reply_audio(
             audio=file_path,
             caption=caption,
             thumb=ph_path, 
             duration=duration,
             progress=progress_for_pyrogram,
             progress_args=( "ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....",  ms, c_time   ))
     except Exception as e: 
         await ms.edit(f"{e}")
         print(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 

@Client.on_message(filters.group & filters.command(["rdoc2", "rename2"]))
async def doc2(bot,update):
     if not update.reply_to_message:
         return await update.reply("**Reply to a Media :)**")
     if not update.reply_to_message.media:
         return await update.reply("**Reply to a Media :(**")
     if len(update.command) == 1:
         return await update.reply("**Give me a new file name for Rename :)**")
     #type = update.data.split('_')[1]
     #new_name = update.message.text
     #new_filename = new_name.split(":-")[1]
     new_filename = update.text.split(" ", 1)[1]
     if not "!" in new_filename:
        new_filename = new_filename + ".mkv"
     else:
        new_filename = new_filename.replace("!", ".")
     file_path = f"downloads/{new_filename}"
     #file = update.message.reply_to_message
     file = update.reply_to_message
     #ms = await update.message.edit("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     ms = await update.reply_text(text="ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     #user_id = int(update.message.from_user.id)
     user_id = int(update.from_user.id)
     ph_path = None
     #data = find(update.message.from_user.id)
     media = getattr(file, file.media.value)
     c_thumb = THUMB_2
     new_cap = new_filename.replace("!", ".")
     caption = f"**__{new_cap}__**\n\n**__Uploaded By : @MovieJunctionGrp__** π₯"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit(text="ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....")
     c_time = time.time() 
     try:
         await update.reply_document(
             document=file_path,
             thumb=ph_path, 
             caption=caption, 
             progress=progress_for_pyrogram,
             progress_args=( "ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....",  ms, c_time   ))
     except Exception as e: 
         await ms.edit(f"{e}")
         print(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 

@Client.on_message(filters.group & filters.command("rvid2"))
async def vid2(bot,update):
     if not update.reply_to_message:
         return await update.reply("**Reply to a Media :)**")
     if not update.reply_to_message.media:
         return await update.reply("**Reply to a Media :(**")
     if len(update.command) == 1:
         return await update.reply("**Give me a new file name for Rename :)**")
     #type = update.data.split('_')[1]
     #new_name = update.message.text
     #new_filename = new_name.split(":-")[1]
     new_filename = update.text.split(" ", 1)[1]
     if not "!" in new_filename:
        new_filename = new_filename + ".mp4"
     else:
        new_filename = new_filename.replace("!", ".")
     file_path = f"downloads/{new_filename}"
     #file = update.message.reply_to_message
     file = update.reply_to_message
     #ms = await update.message.edit("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     ms = await update.reply("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     #user_id = int(update.message.from_user.id)
     user_id = int(update.from_user.id)
     ph_path = None
     #data = find(update.message.from_user.id)
     media = getattr(file, file.media.value)
     c_thumb = THUMB_2
     new_cap = new_filename.replace("!", ".")
     caption = f"**__{new_cap}__**\n\n**__Uploaded By : @MovieJunctionGrp__** π₯"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit("ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ...")
     c_time = time.time() 
     try:
         await update.reply_video(
             video=file_path,
	     caption=caption,
	     thumb=ph_path,
	     duration=duration,
	     progress=progress_for_pyrogram,
	     progress_args=( "ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....",  ms, c_time))
     except Exception as e: 
         await ms.edit(f"{e}")
         print(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 

@Client.on_message(filters.group & filters.command("raud2"))
async def aud2(bot,update):
     if not update.reply_to_message:
         return await update.reply("**Reply to a Media :)**")
     if not update.reply_to_message.media:
         return await update.reply("**Reply to a Media :(**")
     if len(update.command) == 1:
         return await update.reply("**Give me a new file name for Rename :)**")
     #type = update.data.split('_')[1]
     #new_name = update.message.text
     #new_filename = new_name.split(":-")[1]
     new_filename = update.text.split(" ", 1)[1]
     if not "!" in new_filename:
        new_filename = new_filename + ".mp3"
     else:
        new_filename = new_filename.replace("!", ".")
     file_path = f"downloads/{new_filename}"
     #file = update.message.reply_to_message
     file = update.reply_to_message
     #ms = await update.message.edit("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     ms = await update.reply("ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³...")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "ππππΈπ½πΆ ππΎ π³πΎππ½π»πΎπ°π³....",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return 
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
           duration = metadata.get('duration').seconds
     except:
        pass
     #user_id = int(update.message.from_user.id)
     user_id = int(update.from_user.id)
     ph_path = None
     #data = find(update.message.from_user.id)
     media = getattr(file, file.media.value)
     c_thumb = THUMB_2
     new_cap = new_filename.replace("!", ".")
     caption = f"**__{new_cap}__**\n\n**__Uploaded By : @MovieJunctionGrp__** π₯"
     if (media.thumbs or c_thumb):
         if c_thumb:
            ph_path = await bot.download_media(c_thumb) 
         else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")
     await ms.edit("ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....")
     c_time = time.time() 
     try:
         await update.reply_audio(
             audio=file_path,
             caption=caption,
             thumb=ph_path, 
             duration=duration,
             progress=progress_for_pyrogram,
             progress_args=( "ππππΈπ½πΆ ππΎ ππΏπ»πΎπ°π³πΈπ½πΆ....",  ms, c_time   ))
     except Exception as e: 
         await ms.edit(f"{e}")
         print(e) 
         os.remove(file_path)
         if ph_path:
           os.remove(ph_path)
     await ms.delete() 
     os.remove(file_path) 
     if ph_path:
        os.remove(ph_path) 
