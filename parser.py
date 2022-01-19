import os
import requests
import csv
import logging

from bs4 import BeautifulSoup


def get_page(url: str) -> bytes:
    '''Returns the content of the page at the given url'''
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        logger.exception(error)
    page = response.content

    return page


def get_lyrics(page: bytes) -> zip:
    '''Retrieves the lyrics from the page.
    Returns a zip object containing the pairs
    ('original song string', 'translated song string')

    '''
    soup = BeautifulSoup(page, 'lxml')
    original_lyrics = soup.select(selector='.string_container .original')
    translate_lyrics = soup.select(selector='.string_container .translate')
    lyrics = zip(original_lyrics, translate_lyrics)

    return lyrics


def get_filename(path: str, extension='') -> str:
    '''Separates the filename from the path,
    and returns it with the specified extension (empty string by default)

    '''
    filename = os.path.basename(path)
    filename = os.path.splitext(filename)[0] + extension

    return filename


def csv_writer(data: zip, path: str) -> None:
    '''Writes the lyrics to the .csv file at the specified path,
    alternating between the original lines and the translated lines

    '''
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        try:
            for line_original, line_translate in data:
                writer.writerow([line_original.string.strip()])
                writer.writerow([line_translate.string.strip()])
        except csv.Error as error:
            logger.exception(error)


def main(url: str) -> None:
    page = get_page(url)
    lyrics = get_lyrics(page)
    filename = get_filename(url, '.csv')
    csv_writer(lyrics, filename)


if __name__ == '__main__':
    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    logger = logging.getLogger(name='logger')
    main(url=r'https://www.amalgama-lab.com/songs/m/metallica/battery.html')
