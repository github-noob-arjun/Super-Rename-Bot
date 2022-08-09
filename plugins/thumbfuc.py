from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

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
