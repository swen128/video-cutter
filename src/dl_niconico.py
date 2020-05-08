import subprocess
import time
from pathlib import Path

import ffmpeg
from toolz import groupby

from src.utils import read_csv


def download_whole_video(out_path: str, url: str, max_retries: int = 50, retry_interval_sec: int = 1):
    is_completed: bool = False
    retry_count: int = 0

    while (not is_completed) and retry_count < max_retries:
        result = subprocess.run(['youtube-dl', '-o', out_path, url])
        is_completed = result.returncode == 0
        retry_count += 1
        time.sleep(retry_interval_sec)


def cut_mp3(in_path: str, out_path: str, start: str, end: str):
    input = ffmpeg.input(in_path, ss=start, to=end)
    out = ffmpeg.output(input, out_path, format='mp3')
    ffmpeg.run(out)


def main(csv_path: str, out_dir: str):
    csv = read_csv(csv_path)
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    for url, rows in groupby('URL', csv).items():
        tmp_path = f'{out_dir}/tmp'
        download_whole_video(tmp_path, url)

        for row in rows:
            out_path = f'{out_dir}/{row["Title"]}.mp3'
            print(out_path)
            start = row["From"]
            end = row["To"]
            cut_mp3(tmp_path, out_path, start, end)


main(csv_path='config/niconico.csv', out_dir='output')
