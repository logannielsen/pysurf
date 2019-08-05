import requests

requests = requests.Session()
requests.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit"
    "/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
url = "https://httpbin.org/get"


def http_get(url):
    """Receives a url and performs a GET request,
    returns the html dom as text
    """
    return requests.get(url).text


# writing the data to a file
def write_request_to_file():
    """write request to file"""


# determine if a file exists and return it or return None

# using the data, either requested or archived
