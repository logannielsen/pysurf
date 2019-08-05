import os
from pathlib import Path
from urllib.parse import urlparse

import requests

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
path = (
    "C:\\Users\\Logan Programming\\documents\\surf\\pysurf\\"
    "www.worldsurfleague.com\\events\\"
)
year = range(2017, 2018)


def make_soup(abbreviations_list, path, year):
    for season in year:
        for abb in abbreviations_list:
            for filename in os.listdir(os.path.join(path, f"{season}\\{abb}")):
                print(filename)


def produce_completed(soup):
    for completed_event in soup.find_all(
        class_="tour-event tour-event--completed"
    ):
        yield completed_event


def produce_event_detail(completed_event):
    return completed_event.find(class_="tour-event-detail")


def get_href(soup):
    for completed in produce_completed(soup):
        yield produce_event_detail(completed).find("a")["href"]


def event_path_maker(url, root_dir):
    directory = Path(root_dir)
    u = urlparse(url)
    structure = u.netloc.split("/")
    file_dir = structure.pop[-2:]
    directory = directory / structure
    structure = u.path.split("/")
    filename = f"{file_dir[-1]}"
    # for d in structure:
    #     directory = directory / d
    return directory, filename


def event_getter(
    url, root_dir="C:\\Users\\Logan Programming\\documents\\surf\\pysurf"
):
    directory, filename = event_path_maker(url, root_dir)
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


def build_url_list(soup):
    urls = get_href(soup)
    for url in urls:
        event_getter(url)
        print("*" * 100)


soup = make_soup(abbreviations_list, path, year)
for page in soup:
    build_url_list(page)

# pipenv run python render_event.py
