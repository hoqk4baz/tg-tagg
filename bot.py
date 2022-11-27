from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
import os, logging, asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)
api_id = 19151088
api_hash = "0e07250efd85a5bab74b23472a8ed293"
bot_token = "5708622433:AAGb0TjOuVr-HkUEKbVXxqRm_AGDnptomGE"
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    await event.reply("**Ben SensiTv Etiket Botu**, Grup veya Kanaldaki neredeyse tüm üyelerden bahsedebilirim ★\nDaha fazla bilgi için **/help**'i tıklayın.",
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/SensiTvTag_bot?startgroup=a'),
                      Button.url('📣 Geliştirici', 'https://t.me/OkkoOkan')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
    helptext = "**SensiTv Etiket Bot'un Yardım Menüsü**\n\nKomut: /all \n  Bu komutu, başkalarına bahsetmek istediğiniz metinle birlikte kullanabilirsiniz. \n\n`Örnek: /all Günaydın!`  \n\nBu komutu yanıt olarak kullanabilirsiniz. Herhangi bir mesaj yanıtlandığında, yanıtlanan mesaj ile kullanıcıları etiketleyecebilir\n@OkkoOkan"
    await event.reply(helptext,
                    buttons=(
                      [Button.url('🌟 Beni Bir Gruba Ekle', 'https://t.me/SensiTvTag_bot?startgroup=a'),
                      Button.url('📣 Geliştirici', 'https://t.me/OkkoOkan')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
    global anlik_calisan
    if event.is_private:
        return await event.respond("__Bu komut gruplarda ve kanallarda kullanılabilir.!__")
   
    admins = []
    async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        admins.append(admin.id)
    sender = await event.get_sender()
    if not sender.id in admins:
        return await event.respond(f"[{sender.first_name}](tg://user?id={sender.id}) **__Yalnızca yöneticiler hepsinden bahsedebilir warn text bold__**")
 
    if event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.pattern_match.group(1) and event.reply_to_msg_id:
        return await event.respond("**__Bana bir mesaj ver!__**")
    else:
        return await event.respond("**__Bir mesajı yanıtlayın veya başkalarından bahsetmem için bana bir metin verin!__**")
  
    if mode == "text_on_cmd":
        anlik_calisan.append(event.chat_id)
        usrnum = 0
        usrtxt = ""
        async for usr in client.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) , "
            if event.chat_id not in anlik_calisan:
                await event.respond("İşlem Başarılı Bir Şekilde Durduruldu ❌")
                return
            if usrnum == 5:
                await client.send_message(event.chat_id, f"{msg} \n\n {usrtxt}")
                await asyncio.sleep(1.5)
                usrnum = 0
                usrtxt = ""

print(">> Bot çalıyor merak etme 🚀 @OkkoOkan 'dan bilgi alabilirsin <<")
client.run_until_disconnected()
