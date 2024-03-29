import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3
import sys
import argparse
import colorama
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

VERSION = "v1.0.0"


class LinkChecker():

    def __init__(self, base_url, depth, no_threads, timeout, verify, verbosity):
        self.base_url = base_url
        self.base_url_domain = urlparse(self.base_url).netloc
        self.depth = depth
        self.no_threads = no_threads
        self.timeout = timeout
        self.session = requests.Session()
        self.bl_count = 0
        self.no_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.lock = threading.Lock()
        self.i_links = set()
        self.e_links = set()
        self.s_links = set()
        self.s_list = social_list
        self.verify = verify
        self.verbosity = verbosity
        self.RED = colorama.Fore.RED
        self.RED_BACK = colorama.Back.RED
        self.GREEN = colorama.Fore.GREEN
        self.LIGHTBLUE = colorama.Fore.LIGHTBLUE_EX
        self.LIGHTGREEN = colorama.Fore.LIGHTGREEN_EX
        self.CYAN = colorama.Fore.CYAN

    def banner(self, version):
        # Function to print the banner and version
        banner = """

                               ███                     █████    
                          ░░░                     ░░███      
 ████████  █████ ████     █████  ██████    ██████  ░███ █████
░░███░░███░░███ ░███     ░░███  ░░░░░███  ███░░███ ░███░░███
 ░███ ░███ ░███ ░███      ░███   ███████ ░███ ░░░  ░██████░  
 ░███ ░███ ░███ ░███      ░███  ███░░███ ░███  ███ ░███░░███
 ░███████  ░░███████      ░███ ░░████████░░██████  ████ █████
 ░███░░░    ░░░░░███      ░███  ░░░░░░░░  ░░░░░░  ░░░░ ░░░░░
 ░███       ███ ░███  ███ ░███                              
 █████     ░░██████  ░░██████                                
░░░░░       ░░░░░░    ░░░░░░                                
    """
        print(banner)
        print("Author:     nosafesys")
        print(f"Version:    {version}\n")
        print("Follow my socials:")
        print("Github: https://github.com/nosafesys")
        print("Twitter: https://twitter.com/nosafesys")
        print("Instagram: https://instagram.com/_vaxbyv/\n")

    def init_colorama(self):
        colorama.init(autoreset=True)

    def target_info(self):
        print("-"*100)
        print(f":: Target URL       {self.base_url}")
        print(f":: Depth            {self.depth}")
        print(f":: Threads          {self.no_threads}")
        print(f":: Timeout          {self.timeout}")
        print(f":: Verify SSL/TLS   {self.verify}")
        print("-"*100)
        print("\n")

    def check_status(self, url):
        # Function to check the status of a URL and identify broken links
        try:
            r = requests.get(url, timeout=self.timeout, verify=self.verify)
            if r.status_code == 404:
                with self.lock:
                    self.bl_count += 1
                print(f"{self.RED}{url} 404 NOT FOUND")
        except Exception as e:
            print(f"{self.RED_BACK}[!] An error occured in check_status(): {e}")

    def close(self):
        # Function to close HTTP session
        self.session.close()

    def threader(self):
        # Function to create a thread pool for checking the status of links
        try:
            with ThreadPoolExecutor(max_workers=self.no_threads) as executor:
                executor.map(self.check_status, self.s_links)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print(f"{self.RED_BACK}[!] An error occured in threader_a(): {e}")

    def is_social(self, url):
        # Function to check if a URL belongs to a social media domain
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            for social_domain in self.s_list:
                if social_domain in domain:
                    return True
        except Exception as e:
            print(f"{self.RED_BACK}[!] An error occured in is_social(): {e}")

    def fetch_links(self, url):
        # Function to fetch and process links from a given URL
        try:
            links = set()
            r = self.session.get(url, timeout=self.timeout, verify=self.verify)
            soup = BeautifulSoup(r.content, "html.parser")
            a_elements = soup.find_all("a")
            for element in a_elements:
                href = urljoin(url, element.get("href"))
                parsed_href = urlparse(href)
                if parsed_href.scheme != "http" and parsed_href.scheme != "https":
                    continue
                link = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                domain = urlparse(link).netloc
                if link in self.i_links or link in self.e_links:
                    continue
                elif self.base_url_domain in domain:
                    if self.verbosity == 1:
                        pass
                    elif self.verbosity == 2:
                        print(f"{self.LIGHTGREEN}[~] Internal link found: {link}")
                    else:
                        print(f"{self.LIGHTGREEN}[~] Internal link found: {link} (source: {url})")
                    self.i_links.add(link)
                    links.add(link)
                else:
                    if self.verbosity == 1:
                        pass
                    elif self.verbosity == 2:
                        print(f"{self.LIGHTBLUE}[~] External link found: {link}")
                    else:
                        print(f"{self.LIGHTBLUE}[~] External link found: {link} (source: {url})")
                    self.e_links.add(link)
            return links
        except Exception as e:
            print(f"{self.RED_BACK}[!] An error occured in fetch_links(): {e}")

    def crawl(self, url):
        # Function to perform the crawling operation
        try:
            for link in self.fetch_links(url):
                self.crawl(link)
        except Exception as e:
            print(f"{self.RED_BACK}[!] An error occured in crawl(): {e}")

    def summary(self):
        # Function to generate a summary of the crawling results
        try:
            print(f"Search ended at {datetime.now()}")
            print("-"*100)
            print("SOCIAL LINKS:")
            for external_link in self.e_links:
                if self.is_social(external_link):
                    self.s_links.add(external_link)
            if not self.s_links:
                print("[*] No social links found")
            if self.s_links:
                for social_link in self.s_links:
                    print(f"{self.CYAN}[->] {social_link}")
            print("-"*100)
            print("BROKEN LINKS:")
            if self.s_links:
                self.threader()
            if self.bl_count == 0:
                print("[*] No broken links found")
            print("-"*100)
            print("SUMMARY:")
            print(f"[+] Internal links: {len(self.i_links)}")
            print(f"[+] External links: {len(self.e_links)}")
            print(f"[+] Broken links: {self.bl_count}")
            total_urls = len(self.i_links) + len(self.e_links)
            print(f"[+] Total URLs: {total_urls}\n")
        except Exception as e:
            print(f"{self.RED_BACK}[!] An error occured in crawl(): {e}")


def main():
    # Main function to create a new LinkChecker instance
    try:
        parser = argparse.ArgumentParser(description="A quick way to crawl for broken links on a domain")
        parser.add_argument("-u", "--url", help="Specify the target URL")
        parser.add_argument("-t", "--threads", help="Set no. of threads to be run at a time (default:10)", default=10, type=int)
        parser.add_argument("-d", "--depth", help="Specify depth of links to be crawled (default:1)", default=1, type=int, choices=range(1, 4))
        parser.add_argument("-o", "--timeout", help="Specify timeout for each HTTP request (default:5)", default=5, type=int)
        parser.add_argument("-r", "--verify", help="Verify SSL certificates (More secure, but more prone to errors)", action="store_true")
        parser.add_argument("-v", "--verbosity", help="Verbosity level (default:2)", default=2, type=int, choices=(range(1, 4)))
        parser.add_argument("-l", "--list", help="Print default list", action="store_true")
        parser.add_argument("--version", action="version", version=f"PyJack {VERSION}")
        args = parser.parse_args()
        if args.list:
            print(social_list)
            sys.exit()
        else:
            if not args.url:
                parser.error("the following arguments are required: url")
            base_url = args.url
            depth = args.depth
            no_threads = args.threads
            timeout = args.timeout
            verbosity = args.verbosity
            verify = args.verify
        linkchecker = LinkChecker(base_url, depth, no_threads, timeout, verify, verbosity)
        linkchecker.init_colorama()
        linkchecker.banner(VERSION)
        linkchecker.target_info()
        print(f"Search started at {datetime.now()}")
        if linkchecker.depth == 1:
            linkchecker.fetch_links(linkchecker.base_url)
        elif linkchecker.depth == 2:
            for link in linkchecker.fetch_links(linkchecker.base_url):
                linkchecker.fetch_links(link)
        elif linkchecker.depth == 3:
            linkchecker.crawl(linkchecker.base_url)
        linkchecker.close()
        linkchecker.summary()
    except KeyboardInterrupt:
        linkchecker.close()
        linkchecker.summary()
    except Exception as e:
        print(f"{linkchecker.RED_BACK}[!] An error occured: {e}")


if __name__ == "__main__":
    with open("social_list.txt", "r") as f:
        social_list = [line.strip() for line in f.readlines()]
    main()
