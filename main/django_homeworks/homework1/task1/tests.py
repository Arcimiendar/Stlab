from random import randint
import time

from django.test import TestCase

from .models import Item
from selenium import webdriver


class UrlTests(TestCase):
    URLS_302 = [
        '',
        'shops/0/more',
        'shops/0/',
        'items/0/',
        'departments/0/',
    ]
    URLS_200 = [
        '/message'
    ]

    def test_urls(self):
        for url in self.URLS_302:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
        for url in self.URLS_200:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_overflow(self):
        objects = Item.objects.filter(is_sold=True)
        for item in objects:
            item.delete()
        response = self.client.get('')
        self.assertRedirects(response, expected_url='/message')

    def test_creating(self):
        driver = webdriver.Firefox()
        for i in range(randint(1, 40)):
            driver.get('http://127.0.0.1:8000/items/1/create')
            element = driver.find_element_by_id('id_name')
            element.send_keys('item test')
            element = driver.find_element_by_id('id_price')
            element.send_keys(str(randint(1, 1000)))
            time.sleep(0.1)
            buttons = driver.find_elements_by_tag_name('input')
            submit = buttons[-1]
            submit.submit()

        time.sleep(0.5)
        a_tags = driver.find_elements_by_id('IKEA: tables: item test')
        a_tag_count = len(a_tags)
        print(a_tag_count)
        a_tags[0].click()
        driver.find_element_by_tag_name('input').submit()
        a_tag_count -= 1

        for i in range(a_tag_count):
            driver.get('http://127.0.0.1:8000/shops/1/')
            driver.get('http://127.0.0.1:8000/shops/1/')

            elements = driver.find_elements_by_id('IKEA: tables: item test')
            self.assertNotEqual(len(elements), 0)  # if there is nothing of new items on page
            elements[0].click()

            driver.find_element_by_tag_name('input').submit()

        driver.close()
