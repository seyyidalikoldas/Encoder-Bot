import subprocess
import os
import asyncio
from uploader import upload_to_drive

async def run_ffmpeg_async(command):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()

async def encode_video(intro, episode, subtitle, output, interaction):
    temp_episode = "temp_subtitled.mp4"

    # Girdi dosyalarının varlığını kontrol et
    if not os.path.exists(intro):
        return False, f"❌ Intro dosyası bulunamadı: {intro}"
    if not os.path.exists(episode):
        return False, f"❌ Bölüm dosyası bulunamadı: {episode}"
    if not os.path.exists(subtitle):
        return False, f"❌ Altyazı dosyası bulunamadı: {subtitle}"

    subtitle_path = subtitle.replace("\\", "/")
    if not subtitle_path.startswith("subs/"):
        subtitle_path = os.path.join("subs", subtitle).replace("\\", "/")

    subtitle_filter = f"ass='{subtitle_path}'"
    command_sub = [
        "ffmpeg", "-y", "-i", episode,
        "-vf", subtitle_filter,
        "-c:v", "libx264",
        "-c:a", "copy",
        temp_episode
    ]

    rc1, out1, err1 = await run_ffmpeg_async(command_sub)
    if rc1 != 0:
        return False, f"❌ Altyazı ekleme başarısız:\n\n{err1[-1000:]}"

    command_concat = [
        "ffmpeg", "-y",
        "-i", intro,
        "-i", temp_episode,
        "-filter_complex",
        "[0:v]scale=1920:1080[v0];[1:v]scale=1920:1080[v1];[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]",
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-c:a", "aac",
        output
    ]

    rc2, out2, err2 = await run_ffmpeg_async(command_concat)

    try:
        os.remove(temp_episode)
    except Exception as e:
        print(f"Geçici dosya silinemedi: {e}")

    if rc2 != 0:
        return False, f"❌ Encode başarısız:\n\n{err2[-1000:]}"

    try:
        drive_link = upload_to_drive(output)
        return True, f"✅ Encode tamamlandı!\n🔗 [Google Drive'da Aç]({drive_link})"
    except Exception as e:
        return True, f"✅ Encode tamamlandı fakat Drive yükleme başarısız oldu:\n{e}"
