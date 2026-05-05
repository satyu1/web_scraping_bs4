import requests
import bs4
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text
    except requests.exceptions.HTTPError as e:
        print(e)
        return None

def parse_html(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    return soup


def get_largest_image_url(image):
    srcset = image.get("srcset", "")
    if srcset:
        candidates = [part.strip().split(" ")[0] for part in srcset.split(",") if part.strip()]
        if candidates:
            url = candidates[-1]
        else:
            url = image.get("src", "")
    else:
        url = image.get("src", "")
    if url.startswith("//"):
        url = "https:" + url
    return url


def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    r = requests.get(url, headers=headers, stream=True)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return filename


def main():
    url = "https://en.wikipedia.org/wiki/Main_Page"
    html = get_html(url)
    if html:
        soup = parse_html(html)
        image = soup.select_one("a.mw-file-description[title='American bison'] img.mw-file-element")
        if image is not None:
            image_url = get_largest_image_url(image)
            filename = "american_bison.jpg"
            try:
                saved_path = download_image(image_url, filename)
                print(f"Downloaded image to: {saved_path}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image: {e}")
        else:
            print("American bison image not found")

if __name__ == "__main__":
    main()
