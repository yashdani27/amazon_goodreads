import time
import requests
from bs4 import BeautifulSoup
import pprint
import Constants
from Constants import classes_amazon

pp = pprint.PrettyPrinter(indent=4)

book_details = {
    'book': 'shoe dog',
    'author': 'phil knight'
}


def prepare_url_amazon(dict_book_details):
    return f'https://www.amazon.in/s?k=' + dict_book_details['book'] + ' book'


def get_amazon_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 "
                      "Safari/537.36"
    }
    return requests.get(prepare_url_amazon(dict_book_details=book_details), headers=headers).text


def get_data_from_amazon_html(response):
    soup = BeautifulSoup(response, 'lxml')

    results = soup.find_all('div', {'class': classes_amazon[Constants.ROOT]})
    print(len(results))
    relevant_matches = []
    for index, result in enumerate(results):
        dictionary = {}

        # fetch product title
        book_title = result.find(class_=classes_amazon[Constants.BOOK_TITLE]).text

        # fetch author
        author_exists = result.find(class_=classes_amazon[Constants.AUTHOR])
        if author_exists:
            author = author_exists.text
            if author.lower() == book_details[Constants.AUTHOR]:
                dictionary[Constants.AUTHOR] = author
                dictionary[Constants.BOOK_TITLE] = book_title

                # fetch rating
                rating_exists = result.find(class_=classes_amazon[Constants.RATING])
                if rating_exists:
                    rating_book_reviews = rating_exists.text
                    dictionary[Constants.RATING] = rating_book_reviews

                # fetch number of reviews
                numReviews_exists = result.find(class_=classes_amazon[Constants.NUM_REVIEWS])
                if numReviews_exists:
                    num_book_reviews = numReviews_exists.text
                    dictionary[Constants.NUM_REVIEWS] = num_book_reviews

                # fetch prices
                discPrice_exists = result.find(class_=classes_amazon[Constants.PRICE][0])
                if discPrice_exists:
                    dictionary[Constants.DISC_PRICE] = discPrice_exists.find(
                        class_=classes_amazon[Constants.PRICE][1]).text[1:]

                    if len(discPrice_exists.find_all(class_=classes_amazon[Constants.PRICE])) > 1:
                        dictionary[Constants.OG_PRICE] = \
                        discPrice_exists.find_all(class_=classes_amazon[Constants.PRICE])[1].text[1:]

                # fetch prime availability
                prime_exists = result.find(class_=classes_amazon[Constants.PRIME])
                if prime_exists:
                    dictionary[Constants.PRIME] = 'yes'
                relevant_matches.append(dictionary)
    return relevant_matches


def prepare_url_goodreads(dict_book_details):
    return f'https://www.goodreads.com/search?q=' + dict_book_details['book'] + ' ' + dict_book_details['author']


def get_goodreads_html():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 "
                      "Safari/537.36"
    }
    return requests.get(prepare_url_goodreads(dict_book_details=book_details), headers=headers).text


def get_data_from_goodreads_html(response):
    soup = BeautifulSoup(response, 'lxml')

    relevant_matches = []
    rows = soup.find_all('tr')
    for row in rows:
        title = row.find('span').text
        rating = row.find(class_="minirating").text
        author = row.find(class_="authorName").find('span').text
        if author.lower() == book_details['author']:
            relevant_matches.append({
                'title': title,
                'author': author,
                'rating': rating
            })
    return relevant_matches


data_amazon = get_data_from_amazon_html(get_amazon_html())
pp.pprint(data_amazon)
time.sleep(2)
data_goodreads = get_data_from_goodreads_html(get_goodreads_html())
