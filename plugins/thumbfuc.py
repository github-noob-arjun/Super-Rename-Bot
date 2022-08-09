from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

DOWNLOAD_LOCATION = "./DOWNLOADS"

@Client.on_message(filters.group & filters.command(['viewthumb']))
async def viewthumb(client,message):
    try:
        thumb = find(message.from_user.id)
        try:
            if thumb:
                await message.reply_photo(photo=thumb, caption="your current caption")
            else:
                await message.reply_text("**You dont have any custom Thumbnail**")
        except Exception as a:
            await message.reply_text(f"{a}") 
    except Exception as e:
        await message.reply_text(f"{e}")

#@Client.on_message(filters.group & filters.command(['delthumb']))
#async def removethumb(client,message):
    #delthumb(int(message.from_user.id))
   # await message.reply_text("**Thumbnail deleted**")
	
@Client.on_message(filters.group & filters.command(['addthumb']))
async def addthumbs(client,message):
    if not message.reply_to_message:
        return await message.reply("**Reply to a photo :)**")
    if not message.reply_to_message.photo:
        return await message.reply("**this is not a photo :)**")
    try:
        file_id = str(message.reply_to_message.photo.file_id)
        try:
            addthumb(int(message.from_user.id) , file_id)
            await message.reply_text("**Your Custom Thumbnail Saved Successfully** ✅")
        except Exception as a:
            await message.reply_text(f"{a}")
    except Exception as a:
        await message.reply_text(f"{a}")


@Client.on_message(filters.group & filters.command(['seethumb']))
async def show_thumb(bot, update):
    thumb_image_path = DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    if not os.path.exists(thumb_image_path):
        mes = await thumb(update.from_user.id)
        if mes != None:
            m = await bot.get_messages(update.chat.id, mes.msg_id)
            await m.download(file_name=thumb_image_path)
            thumb_image_path = thumb_image_path
        else:
            thumb_image_path = None    
    
    if thumb_image_path is not None:
        try:
            await bot.send_photo(
                chat_id=update.chat.id,
                photo=thumb_image_path,
                reply_to_message_id=update.message_id
            )
        except:
            pass
    else:
        await update.reply_text("**first add a thumbnail. Use /addthumb**")
        


