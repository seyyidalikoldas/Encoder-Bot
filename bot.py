import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import time
from downloader import download_magnet_with_progress
from encoder import encode_video

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")
    await tree.sync()

@tree.command(name="indir", description="Magnet link ile video indir")
@app_commands.describe(magnet_link="İndirmek istediğiniz magnet link", filename="Kaydedilecek dosya adı (uzantısız)")
async def slash_indir(interaction: discord.Interaction, magnet_link: str, filename: str):
    await interaction.response.send_message("📥 İndirme başlatılıyor...")

    msg = await interaction.followup.send("📶 İndirme ilerlemesi: %0")

    last_percent = -1
    last_update = 0

    def progress_callback(percent):
        nonlocal last_percent, last_update
        now = time.time()
        if percent != last_percent and (now - last_update > 5 or percent == 100):
            last_percent = percent
            last_update = now
            asyncio.run_coroutine_threadsafe(
                msg.edit(content=f"📶 İndirme ilerlemesi: %{percent}"), bot.loop
            )

    loop = asyncio.get_event_loop()
    success, message = await loop.run_in_executor(
        None, download_magnet_with_progress, magnet_link, progress_callback, filename
    )

    if success:
        await interaction.followup.send(f"✅ `{message}` başarıyla indirildi!")
    else:
        await interaction.followup.send("❌ Hata oluştu: " + message)

@tree.command(name="encode", description="Intro, video ve altyazıdan MP4 dosyası oluşturur")
@app_commands.describe(
    intro="Intro video adı (örn. intro.mp4)",
    episode="Ana bölüm videosu (örn. bölüm37.mkv)",
    subtitle_file="Altyazı dosyası (.ass uzantılı)",
    subtitle_name="Sunucuda kaydedilecek altyazı adı (örn. kusuriya37.ass)",
    output="Çıktı dosya adı (varsayılan: output.mp4)"
)
async def slash_encode(
    interaction: discord.Interaction,
    intro: str,
    episode: str,
    subtitle_file: discord.Attachment,
    subtitle_name: str,
    output: str = "output.mp4"
):
    await interaction.response.send_message("🎬 Encode işlemi başlatıldı...")

    # Altyazı dosyasını kaydet
    os.makedirs("subs", exist_ok=True)
    subtitle_path = os.path.join("subs", subtitle_name)
    await subtitle_file.save(subtitle_path)

    msg = await interaction.followup.send("🛠️ İşleniyor: 0s")
    start_time = time.time()

    async def progress_updater():
        while True:
            elapsed = int(time.time() - start_time)
            try:
                await msg.edit(content=f"🛠️ İşleniyor: {elapsed} saniye geçti")
                await asyncio.sleep(5)
            except discord.NotFound:
                break

    progress_task = asyncio.create_task(progress_updater())

    # Dosya yollarını düzelt
    intro_path = os.path.join("downloads", intro)
    episode_path = os.path.join("downloads", episode)

    success, message = await encode_video(intro_path, episode_path, subtitle_path, output, interaction)

    progress_task.cancel()
    try:
        await progress_task
    except asyncio.CancelledError:
        pass

    if success:
        await interaction.followup.send(content=message)
    elif message:
        if len(message) > 1500:
            message = message[-1500:]
        await interaction.followup.send(f"❌ Encode hatası:\n```")


bot.run("")#discord botu tokeninizi girin buraya
