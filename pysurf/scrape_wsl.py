import os
from pathlib import Path
from urllib.parse import urlparse

import requests


def _path_maker(url, root_dir):
    directory = Path(root_dir)
    u = urlparse(url)
    directory = directory / u.netloc
    structure = u.path.split("/")
    filename = f"{structure[-1]}_calendar"
    for d in structure:
        directory = directory / d
    return directory, filename


p = _path_maker(
    "https://www.worldsurfleague.com/events/2019/mct",
    root_dir="C:\\Users\\Logan Programming\\documents\\surf\\pysurf",
)


def url_getter(
    url, root_dir="C:\\Users\\Logan Programming\\documents\\surf\\pysurf"
):
    directory, filename = _path_maker(url, root_dir)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    req_ses = requests.session()
    req = req_ses.get(url)
    # soup = bs4.BeautifulSoup(req.text, "html.parser")
    if req.status_code == 200:
        with open(directory / filename, "w", encoding="utf-8") as f:
            f.write(req.text)
            f.close()
    else:
        req.raise_for_status()


if __name__ == "__main__":
    try:
        abbreviations_list = [
            "mct",
            "wct",
            "mqs",
            "wqs",
            "mbwt",
            "wbwt",
            "mlt",
            "wlt",
            "mjun",
            "wjun",
            "spec",
        ]
        year = range(2012, 2019)
        for season in year:
            for abb in abbreviations_list:
                url_getter(
                    f"https://www.worldsurfleague.com/events/{season}/{abb}"
                )
    except requests.exceptions.RequestException:
        print("maybe retry???")

# pipenv run black -l79 .\scrape_wsl.py
