import time

import requests
from bs4 import BeautifulSoup
import pprint
import random

pp = pprint.PrettyPrinter(indent=4)

book_details = {
    'book': 'shoe dog',
    'author': 'phil knight'
}


def get_user_agent():
    """ Randomly pick a user agent to avoid being detected and blocked by modern websites """
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 '
        'Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 '
        'Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile '
        'Safari/537.36 '
    ]
    user_agent = random.choice(user_agents)
    return user_agent


def prepare_url_amazon(dict):
    return f'https://www.amazon.in/s?k=' + dict['book'] + ' book'


def prepare_url_goodreads(dict):
    return f'https://www.goodreads.com/search?q=' + dict['book'] + ' ' + dict['author']


def get_html_from_amazon():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 "
                      "Safari/537.36"
    }
    return requests.get(prepare_url_amazon(dict=book_details), headers=headers).text


response = get_html_from_amazon()
print(response)
soup = BeautifulSoup(response, 'lxml')

classes_amazon = {
    'root': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right',
    'bookTitle': 'a-size-medium a-color-base a-text-normal',
    'author': 'a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style',
    'rating': 'a-icon-alt',
    'numReviews': 'a-size-base s-underline-text',
    'price': ['a-row a-size-base a-color-base', 'a-offscreen'],
    'prime': 'a-icon a-icon-prime a-icon-medium'
}

results = soup.find_all('div', {'class': classes_amazon['root']})
print(len(results))
relevant_matches = []
for index, result in enumerate(results):
    dict = {}

    # fetch product title
    book_title = result.find(class_=classes_amazon['bookTitle']).text
    print(book_title)

    # fetch author
    author_exists = result.find(class_=classes_amazon['author'])
    if author_exists:
        author = author_exists.text
        if author.lower() == book_details['author']:
            dict['author'] = author
            dict['title'] = book_title

            # fetch rating
            rating_exists = result.find(class_=classes_amazon['rating'])
            if rating_exists:
                rating_book_reviews = rating_exists.text
                dict['rating'] = rating_book_reviews

            # fetch number of reviews
            numReviews_exists = result.find(class_=classes_amazon['numReviews'])
            if numReviews_exists:
                num_book_reviews = numReviews_exists.text
                dict['numReviews'] = num_book_reviews

            # fetch prices
            discPrice_exists = result.find(class_=classes_amazon['price'][0])
            if discPrice_exists:
                dict['discPrice'] = discPrice_exists.find(class_=classes_amazon['price'][1]).text[1:]

                if len(discPrice_exists.find_all(class_=classes_amazon['price'])) > 1:
                    dict['ogPrice'] = discPrice_exists.find_all(class_=classes_amazon['price'])[1].text[1:]

            # fetch prime availability
            prime_exists = result.find(class_=classes_amazon['prime'])
            if prime_exists:
                dict['prime'] = 'yes'
            relevant_matches.append(dict)
            print(str(index))

pp.pprint(relevant_matches)

print()

time.sleep(2)

response = requests.get(prepare_url_goodreads(book_details)).text
soup = BeautifulSoup(response, 'lxml')

matches = []
rows = soup.find_all('tr')
for row in rows:
    title = row.find('span').text
    # print(title)
    rating = row.find(class_="minirating").text
    # print(rating)
    author = row.find(class_="authorName").find('span').text
    # print(author)
    if author.lower() == book_details['author']:
        matches.append({
            'title': title,
            'author': author,
            'rating': rating
        })
    print()

pp.pprint(matches)