import errno
import itertools
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

requests = requests.Session()
requests.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
        "/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }
)
url = "https://httpbin.org/get"


def http_get_response(url):
    """Receives a url and performs a GET request,
    returns the html dom as text
    """
    r = requests.get(url)
    r.raise_for_status()
    return r


def http_get_text(url):
    return http_get_response(url).text


def http_get_json(url):
    """need to write test"""
    return http_get_response(url).json


def create_file_path_calendar(tour, year, root=None):
    directory = Path(os.path.join(root, tour))
    year = str(year)
    return directory, year


def surf_season_tuple_builder():
    ABBR_LIST = [
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
    year = range(2018, 2019)
    return itertools.product(ABBR_LIST, year)


# writing the data to a file
def create_file_path_event(url, tour, year, root=None):
    """generate file path and name"""
    u = urlparse(url)
    structure = u.path.split("/")
    directory = Path(os.path.join(root, tour, str(year)))
    filename = f"{structure[-2]}"
    return directory, filename


def create_file_path_event_results(url, tour, year, root=None):
    """generate file path and name"""
    results_url = f"{url}/results"
    u = urlparse(url)
    structure = u.path.split("/")
    directory = Path(os.path.join(root, tour, str(year)))
    filename = f"{structure[-2]}_results"
    return directory, filename, results_url


def create_dirs(path):
    """checks if a directory exists and if not creates one"""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            # wtf?
            # https://stackoverflow.com/questions/12517451/
            if exc.errno != errno.EEXIST:
                raise


def get_tourn_html(url, tour, year):
    skip_urls = [
        "https://www.wslfounderscup.com",
        "http://us.oneill.com/cwc/",
        "oneill.com/cwc/?page_id=1946",
        (
            "https://www.worldsurfleague.com/events/2013/mjun/560/"
            "vans-us-open-junior-pro"
        ),
        "http://www.ripcurlproargentina.com",
        (
            "http://www.worldsurfleague.com/events/2017/mqs/2565/"
            "south-to-south-pres-itacare-surf-sound-festival/live"
        ),
    ]
    if url not in skip_urls:
        # print(url)
        [
            event_directory,
            event_filename,
            results_url,
        ] = create_file_path_event_results(url, tour, year, "results")
        create_dirs(event_directory)
        if not Path(os.path.join(event_directory, event_filename)).is_file():
            event_req = http_get_text(results_url)
            save_file(event_directory, event_filename, event_req)


def save_file(path, filename, req_text):
    """need to test"""
    with open(path / filename, "w", encoding="utf-8") as f:
        f.write(req_text)


def yield_completed_events(tour_season_event_file):
    """ takes a season events file (eg, mct 2007) and yields all completed
    events"""
    class_list = [
        "tour-event tour-event--completed",
        "tour-event tour-event--completed tour-event--has-category",
    ]
    # "tour-event tour-event--upcoming" is a class
    # - need to figure out how to handle this
    for completed_class in class_list:
        for completed_event in tour_season_event_file.find_all(
            class_=completed_class
        ):
            yield completed_event


def open_souped_file(directory, filename):
    with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
        event_file = f.read()
        return BeautifulSoup(event_file, "html.parser")


def produce_event_detail(completed_event):
    return completed_event.find(class_="tour-event-detail")


def get_href(tour_season_event_file):
    for completed in yield_completed_events(tour_season_event_file):
        yield produce_event_detail(completed).find("a")["href"]


def get_round_id(event_directory, event_filename):
    result_page = open_souped_file(event_directory, event_filename)
    event_rounds = result_page.find_all(
        class_="post-event-watch-round-nav__item"
    )
    round_url_list = []
    for event_round in event_rounds:
        suff = event_round.find("a")["href"]
        round_url_list.append(f"https://www.worldsurfleague.com{suff}")
    return round_url_list


def create_round_file_path(round_url_list, tour, year):
    for round_result_url in round_url_list:
        split_url = round_result_url.split("?")
        directory, filename = create_file_path_event_round_results(
            round_result_url, tour, year, split_url[1], "round_results"
        )
        yield directory, filename, round_result_url


def save_round_results_to_file(directory, filename, round_result_url):
    create_dirs(directory)
    if not Path(os.path.join(directory, filename)).is_file():
        event_req = http_get_text(round_result_url)
        save_file(directory, filename, event_req)


def create_file_path_event_round_results(url, tour, year, roundId, root=None):
    """generate file path and name"""
    u = urlparse(url)
    structure = u.path.split("/")
    directory = Path(os.path.join(root, tour, str(year)))
    filename = f"{structure[-3]}_{roundId}"
    return directory, filename
