import subprocess
import os
import time
import re

def download_magnet_with_progress(magnet_link, progress_callback=None, custom_name=None, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    aria2_path = r"C:\Users\seicode\Downloads\aria2-1.37.0-win-64bit-build1\aria2c.exe"

    percent_regex = re.compile(r"\((\d+)%\)")

    command = [
        aria2_path,
        "--seed-time=0",
        "--dir=" + output_dir,
        "--console-log-level=notice",
        "--summary-interval=1",
        magnet_link
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    final_filename = None

    for line in process.stdout:
        if progress_callback:
            match = percent_regex.search(line)
            if match:
                percent = int(match.group(1))
                progress_callback(percent)

        if "Download complete:" in line:
            match = re.search(r'Download complete: (.*)', line)
            if match:
                final_filename = match.group(1).strip()

    process.wait()

    if process.returncode != 0:
        return False, "aria2c başarısız oldu veya dosya bulunamadı."

    if not final_filename or not os.path.isfile(final_filename):
        return False, "Dosya adı tespit edilemedi."

    # Dosya adını değiştir
    if custom_name:
        new_path = os.path.join(output_dir, custom_name + ".mkv")
        try:
            os.rename(final_filename, new_path)
        except Exception as e:
            return False, f"Dosya adı değiştirilemedi: {e}"
        return True, custom_name + ".mkv"
    else:
        return True, os.path.basename(final_filename)
