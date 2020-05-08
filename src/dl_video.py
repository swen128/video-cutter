import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.utils import read_csv


def cut_stream(in_path: str, out_path: str, start: str, end: str):
    subprocess.run([
        'ffmpeg',
        '-y',
        '-ss', start,
        '-i', in_path,
        '-to', end,
        '-copyts',
        out_path
    ])


def mux(video_path: str, audio_path: str, out_path: str):
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c', 'copy',
        out_path
    ])


def download_portion(in_path: str, out_path: str, start: str, end: str):
    out = subprocess.check_output([
        'youtube-dl',
        '--get-url',
        '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
        in_path
    ])
    video_url, audio_url = out.decode('utf-8').strip().split('\n')

    with NamedTemporaryFile(suffix='.mp4') as video_file:
        with NamedTemporaryFile(suffix='.m4a') as audio_file:
            cut_stream(video_url, video_file.name, start, end)
            cut_stream(audio_url, audio_file.name, start, end)
            mux(video_file.name, audio_file.name, out_path)


def main(csv_path: str, out_dir: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for i, row in enumerate(read_csv(csv_path)):
        out_path = f'{out_dir}/{row["Title"]}.mp4'
        url = row['URL']
        start = row['From']
        end = row['To']
        download_portion(url, out_path, start, end)


main(csv_path='config/videos.csv', out_dir='output')
