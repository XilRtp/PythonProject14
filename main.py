from urllib.parse import urlparse
import requests
from dotenv import load_dotenv
import os
import argparse


def shorten_link(url, secret):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {"Authorization": f"Bearer {secret}"}
    payload = {"long_url": url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["id"]


def count_clicks(bitlink, secret):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {"Authorization": f"Bearer {secret}"}
    payload = {"unit": "month"}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(bitlink, secret):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {"Authorization": f"Bearer {secret}"}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Сокращение ссылок')
    parser.add_argument('--url', help='Введите ссылку: ')
    args = parser.parse_args()
    parsed_url = urlparse(args.url)
    parsed_url = f"{parsed_url.netloc}{parsed_url.path}"
    secret = os.environ['BITLY_TOKEN']
    try:
        if is_bitlink(parsed_url, secret):
            print(count_clicks(parsed_url, secret))
        else:
            print(shorten_link(args.url, secret))
    except requests.exceptions.HTTPError:
        print("Проверьте ссылку")


if __name__ == "__main__":
    main()
