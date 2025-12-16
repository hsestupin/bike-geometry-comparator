import argparse
import ssl
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def find_crawler(url):
    match url.netloc:
        case "www.canyon.com":
            from .canyon import crawl

            return crawl
        case _:
            raise ValueError(f"No crawler found for {url.netloc}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="GeometryCrawler",
        description="Web crawler which parses geometry data from the web page",
    )
    parser.add_argument("url")
    parser.add_argument("-m", "--model", required=True, help="Bike model name")
    args = parser.parse_args()
    url = urlparse(args.url)
    model = args.model
    crawl = find_crawler(url)

    disable_ssl_certificate_validation()

    html = Path(f"build/{model}.html")
    with urlopen(args.url) as source, open(html, "wb") as target:
        target.write(source.read())

    out_csv = Path(f"build/{model}_geometry.csv")
    crawl(html, out_csv)
    print(f"CSV written to: {out_csv}")


def disable_ssl_certificate_validation():
    ssl._create_default_https_context = ssl._create_unverified_context


if __name__ == "__main__":
    main()
