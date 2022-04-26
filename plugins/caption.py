from pyrogram import Client, filters 

@Client.on_messages(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**Give me a caption to set.\n\nExample:- `/set_caption 📕 File Name: {filename}\n\n💾 Size: {filesize}\n\n⏰ Duration: {duration}`**)
    
