from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

@Client.on_message(filters.group & filters.command(['viewthumb']))
async def viewthumb(client,message):
    thumb = find(int(message.from_user.id))[0]
    if thumb:
       await message.reply_photo(photo=thumb)
    else:
        await message.reply_text("**You dont have any custom Thumbnail**") 
		
@Client.on_message(filters.group & filters.command(['delthumb']))
async def removethumb(client,message):
    delthumb(int(message.from_user.id))
    await message.reply_text("**Custom Thumbnail Deleted Successfully**")
	
@Client.on_message(filters.group & filters.command(['addthumb']))
async def addthumbs(client,message):
    if not message.reply_to_message:
        return await message.reply("**Reply to a photo :)**")
    if not message.reply_to_message.photo:
        return await message.reply("**this is not a photo :)**")
    file_id = str(message.reply_to_message.photo.file_id)
    addthumb(message.from_user.id , file_id)
    await message.reply_text("**Your Custom Thumbnail Saved Successfully** ✅")
	
