from bs4 import BeautifulSoup
import os
import requests
import shutil
from tqdm import tqdm


base_url = 'https://www.planespotters.net'
image_folder_latest = './latest'
image_folder_top_daily = './top_daily'


def get_html_parsed(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'}
    response = requests.get(url, headers=headers)

    html = response.text

    parsed_html = BeautifulSoup(html, 'lxml')

    return parsed_html


def get_page_urls_latest(url):
    parsed_html = get_html_parsed(url)

    main_content = parsed_html.find('main', {'id': 'content'})
    planes_grid = main_content.find('div', {'class': 'photo_card__grid'})
    urls = [elem.attrs['href']
            if elem.name is not None else None for elem in planes_grid.children]
    urls = list(filter(lambda x: x is not None, urls))
    urls = list(map(lambda x: f'{base_url}{x}', urls))

    return urls


def get_page_urls_top(url):
    parsed_html = get_html_parsed(url)

    main_content = parsed_html.find('main', {'id': 'content'})
    photogallery = main_content.find('div', {'id': 'photogallery'})
    urls = [list(elem.children)[1].attrs["href"]
            if elem.name is not None else None for elem in photogallery]
    urls = list(filter(lambda x: x is not None, urls))
    urls = list(map(lambda x: f'{base_url}{x}', urls))

    return urls


def get_image_urls_and_name(page_url):
    parsed_html = get_html_parsed(page_url)

    image_container = (parsed_html
                       .find('main', {'id': 'content'})
                       .find('div', {'class': 'photo_large__container'}))

    image_url = (image_container.find('img').attrs['src'])

    image_name = (image_container.find('h1').text)

    return image_url, image_name


def fetch_image(url, filename):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'}
    r = requests.get(url, stream=True, headers=headers)
    if r.status_code == 200:
        with open(filename, 'wb+') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def clear_folder(folder):
    files = os.listdir(folder)
    for file in files:
        file_path = os.path.join(folder, file)
        os.unlink(file_path)


def fetch_latest_images(folder):
    clear_folder(folder)

    print('Fetching latest images...')

    url = f'{base_url}/photos/latest'

    page_urls = get_page_urls_latest(url)

    print(f'Found {len(page_urls)} images.')

    print('Fetching image URLs...')
    image_urls_and_names = [get_image_urls_and_name(
        page_url) for page_url in tqdm(page_urls)]

    print('Fetching images...')
    for image_url, image_name in tqdm(image_urls_and_names):
        fetch_image(image_url, f'{folder}/{image_name}.jpg')

    print('Done.')


def fetch_daily_top_images(folder):
    clear_folder(folder)

    print('Fetching top images of the day...')

    url = f'{base_url}/photos/favorited/added/day'

    page_urls = get_page_urls_top(url)

    print(f'Found {len(page_urls)} images.')

    print('Fetching image URLs...')
    image_urls_and_names = [get_image_urls_and_name(
        page_url) for page_url in tqdm(page_urls)]

    print('Fetching images...')
    for image_url, image_name in tqdm(image_urls_and_names):
        fetch_image(image_url, f'{folder}/{image_name}.jpg')

    print('Done.')


def ensure_folders_exist():
    for directory in [image_folder_latest, image_folder_top_daily]:
        if not os.path.exists(directory):
            os.makedirs(directory)


if __name__ == '__main__':
    ensure_folders_exist()
    fetch_latest_images(image_folder_latest)
    fetch_daily_top_images(image_folder_top_daily)
