import argparse
import ssl
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen


def find_page_parser(url):
    match url.netloc:
        case "www.canyon.com":
            from .canyon import parse_page

            return parse_page
        case _:
            raise ValueError(f"No parser found for {url.netloc}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="GeometryWebscraper",
        description="Web scraper which parses geometry data from the web page",
    )
    parser.add_argument("url")
    parser.add_argument("-m", "--model", required=True, help="Bike model name")
    parser.add_argument("-c", "--csv", help="Output csv file")
    args = parser.parse_args()
    url = urlparse(args.url)
    model = args.model
    csv_arg = args.csv
    parse_page = find_page_parser(url)

    disable_ssl_certificate_validation()

    build_path = Path("build")
    build_path.mkdir(exist_ok=True)

    html = Path(build_path / f"{model}.html")
    with urlopen(args.url) as source, open(html, "wb") as target:
        target.write(source.read())

    out_csv = Path(csv_arg or build_path / f"{model}_geometry.csv")
    out_csv.parent.mkdir(exist_ok=True, parents=True)
    parse_page(html, out_csv)
    print(f"CSV written to: {out_csv}")


def disable_ssl_certificate_validation():
    ssl._create_default_https_context = ssl._create_unverified_context


if __name__ == "__main__":
    main()
