from pyrogram import Client, filters
from helper.database import find, delthumb, addthumb

@Client.on_message(filters.group & filters.command(['viewthumb']))
async def viewthumb(client,message):
    thumb = find(int(message.from_user.id))[0]
    if thumb:
       await client.send_photo(
	   chat_id=message.chat.id, 
	   photo=thumb)
    else:
        await message.reply_text("**You dont have any custom Thumbnail**") 
		
@Client.on_message(filters.group & filters.command(['delthumb']))
async def removethumb(client,message):
    delthumb(int(message.from_user.id))
    await message.reply_text("**Custom Thumbnail Deleted Successfully**")
	
@Client.on_message(filters.group & filters.photo)
async def addthumbs(client,message):
    file_id = str(message.photo.file_id)
    addthumb(message.from_user.id , file_id)
    await message.reply_text("**Your Custom Thumbnail Saved Successfully** ✅")
	
