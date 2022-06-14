import requests
from bs4 import BeautifulSoup
import pprint
pp = pprint.PrettyPrinter(indent=4)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 "
                  "Safari/537.36"}
book = 'shoe dog'
author_given = 'phil knight'
print(book.replace(' ', '+'))
print(author_given.replace(' ', '+'))
# book = book.replace(' ', '+') + '+' + author_given.replace(' ', '+')
query = book + ' ' + author_given
url_amazon = f'https://www.amazon.in/s?k=' + book + '+book'
print(url_amazon)
url_goodreads = f'https://www.goodreads.com/search?q={query}'
print(url_goodreads)
response = requests.get(url_amazon, headers=headers).text

soup = BeautifulSoup(response, 'lxml')

results = soup.find_all('div', {'class': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right'})
print(len(results))

relevant_matches = []

for index, result in enumerate(results):
    dict = {}
    book_title = result.find(class_="a-size-medium a-color-base a-text-normal").text
    print(book_title)
    if result.find(class_="a-size-base a-link-normal s-underline-text s-underline-link-text s-link-style"):
        author = result.find(class_="a-size-base a-link-normal s-underline-text s-underline-link-text"
                                    " s-link-style").text
        if author.lower() == author_given:
            dict['author'] = author
            print('Author:', dict['author'])
            book_title = result.find(class_="a-size-medium a-color-base a-text-normal").text
            dict['title'] = book_title

            if result.find(class_="a-icon-alt"):
                rating_book_reviews = result.find(class_="a-icon-alt").text
                dict['rating'] = rating_book_reviews
            if result.find(class_="a-size-base s-underline-text"):
                num_book_reviews = result.find(class_="a-size-base s-underline-text").text
                dict['numReviews'] = num_book_reviews
                # print('Number of reviews:', num_book_reviews)
            if result.find(class_="a-row a-size-base a-color-base"):
                # print('Discounted price:',
                #       result.find(class_="a-row a-size-base a-color-base").find(class_="a-offscreen").text[1:])
                dict['discPrice'] = result.find(class_="a-row a-size-base a-color-base").find(class_="a-offscreen").text[1:]
                if len(result.find(class_="a-row a-size-base a-color-base").find_all(class_="a-offscreen")) > 1:
                    dict['ogPrice'] = result.find(class_="a-row a-size-base a-color-base").find_all(class_="a-offscreen")[1].text[1:]
            if result.find(class_="a-icon a-icon-prime a-icon-medium"):
                dict['prime'] = 'yes'
            relevant_matches.append(dict)
            print(str(index))

pp.pprint(relevant_matches)

print()

response = requests.get(url_goodreads).text
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
    if author.lower() == author_given:
        matches.append({
            'title': title,
            'author': author,
            'rating': rating
        })
    print()

pp.pprint(matches)

# print(results)


# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
