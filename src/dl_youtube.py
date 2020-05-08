import subprocess
from pathlib import Path

from src.utils import read_csv


def cut_stream(in_path: str, out_path: str, start: str, end: str):
    subprocess.run([
        'ffmpeg',
        '-y',
        '-ss', start,
        '-i', in_path,
        '-to', end,
        '-copyts',
        "-write_xing", "0",
        out_path
    ])


def download_portion(out_path: str, video_url: str, start: str, end: str):
    out = subprocess.check_output([
        'youtube-dl',
        '--get-url',
        '--format', 'bestaudio',
        video_url
    ])
    audio_url = out.decode('utf-8').strip()

    cut_stream(audio_url, out_path, start, end)


def main(csv_path: str, out_dir: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for row in read_csv(csv_path):
        out_path = f'{out_dir}/{row["Title"]}.mp3'
        url = row['URL']
        start = row['From']
        end = row['To']
        download_portion(out_path, url, start, end)


main(csv_path='config/youtube.csv', out_dir='output')
