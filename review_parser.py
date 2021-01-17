# This Python file uses the following encoding: utf-8

import requests
from lxml import html


class ReviewParser:
    def __init__(self, title_str):
        a = title_str.split()
        title = '+'.join(a)
        print(title)
        url = 'https://www.goodreads.com/search?utf8=%E2%9C%93&search%5Bquery%5D='+title+'&commit=Search&search_type' \
                                                                                         '=books '
        print(url)
        page = 1
        text = self.load_page(url, page)

        tree = html.fromstring(text)

        book_list_lxml = tree.xpath('//a[@class = "bookTitle"]/span/text()')[0]
        print(book_list_lxml)

        url_link = tree.xpath('//a[@class = "bookTitle"]/@href')[0]
        book_url = 'https://www.goodreads.com'+url_link
        print(book_url)

        author = tree.xpath('//a[@class = "authorName"]/span/text()')[0]
        print(author)

        page += 1
        book_page = self.load_page(book_url, page)

        self.book_tree = html.fromstring(book_page)

    def load_page(self, url, page):
        r = requests.get(url)
        r_text = r.text
        with open('./page_%d.html' % page, 'wb') as output_file:
            output_file.write(r_text.encode('utf-8'))
        with open('./page_%d.html' % page, encoding='utf-8') as input_file:
            text = input_file.read()
        return text

    def get_reviews(self, book_tree):
        reviews = []
        for i in range(10):
            review_list_lxml = book_tree.xpath('//div[@class = "friendReviews elementListBrown"]')[i]
            rew = review_list_lxml.xpath('.//span/span[1]/text()')
            reviews.extend(rew)
            text = ''.join(reviews)
        return text
