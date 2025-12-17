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
    parser.add_argument("-c", "--csv", help="Output csv file")
    args = parser.parse_args()
    url = urlparse(args.url)
    model = args.model
    csv_arg = args.csv
    crawl = find_crawler(url)

    disable_ssl_certificate_validation()

    build_path = Path("build")
    build_path.mkdir(exist_ok=True)

    html = Path(build_path / f"{model}.html")
    with urlopen(args.url) as source, open(html, "wb") as target:
        target.write(source.read())

    out_csv = csv_arg or Path(build_path / f"{model}_geometry.csv")
    crawl(html, out_csv)
    print(f"CSV written to: {out_csv}")


def disable_ssl_certificate_validation():
    ssl._create_default_https_context = ssl._create_unverified_context


if __name__ == "__main__":
    main()
