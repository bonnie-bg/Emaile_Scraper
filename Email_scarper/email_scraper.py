# usr/bin/python3
from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re
from colorama import init
from termcolor import colored, cprint


class bcolors:
    GREEN = "\033[62m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


def banner():
    print(bcolors.RED + "+[+[+[ Email scraper v1.0 ]+]+]+")
    print(bcolors.RED + "+[+[+[ made with codes ]+]+]+")
    print(
        bcolors.GREEN
        + """   
          ___           o               ,__  ,___,           ,___,   __
         [   ._ _  / \  | |       [```` (     [    )    /\   |     ) [__  |,,``.
         [___[ | )/---\ | |__     [..,  (     [  .`    /--\  |.....  [__  |        
         [___                     ,,,,] (,__  [   `,         |
      *.________________________________________________________________________,' (Email scraper)`--' """
    )
    print(
        bcolors.YELLOW + "+]+]+] Enter Target URL To scan: https://mas.bg.ac.rs ]+]+]+"
    )


banner()
print(bcolors.RED)
user_url = str(input("+] Enter Target URL To scan: "))
urls = deque([user_url])

scraped_urls = set()
emails = set()

count = 0
try:
    while len(urls):
        count += 1
        if count == 50:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)

        path = url[: url.rfind("/") + 1] if "/" in parts.path else url

        print("[%d processing %s" % (count, url))

        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue
        new_emails = set(
            re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I)
        )
        emails.update(new_emails)
        soup = BeautifulSoup(response.text, features="lxml")
        for anchor in soup.find_all("a"):
            link = anchor.attrs["href"] if "href" in anchor.attrs else ""
            if link.startswith("/"):
                link = base_url + link
            elif not link.startswith("http"):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)
except KeyboardInterrupt:
    print("-] closing!")

for mail in emails:
    print(mail)
