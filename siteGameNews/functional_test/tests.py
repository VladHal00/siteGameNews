from selenium import webdriver
from django.core.files import File
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from homeblog.models import Article
from datetime import datetime
import pytz
import os


class BlogTests(LiveServerTestCase):

    # создать такой-то браузер для теста/добавить ложную статью/создать автора и проверить на наличие
    def setUp(self):
        self.browser = webdriver.Chrome()
        Article.objects.create(
            title='title 1',
            summary='summary 1',
            full_text='full_text 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='title-1',
            category='category-1',
            og_image=File(open('test_images/test_image_1.png', 'rb'))
        )
        Article.objects.create(
            title='title 2',
            summary='summary 2',
            full_text='full_text 2',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-2',
            category='category-1',
            og_image=File(open('test_images/test_image_1.png', 'rb'))
        )
        Article.objects.create(
            title='title 3',
            summary='summary 3',
            full_text='full_text 3',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-3',
            category='category-2',
            og_image=File(open('test_images/test_image_2.png', 'rb'))
        )

    # тест пройдет, закрыть браузер
    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        footer = self.browser.find_element(By.CLASS_NAME, 'footer')
        self.assertTrue(footer.location['y'] > 500)

    # тест проверка на заголовок
    def test_home_page_header(self):
        self.browser.get(self.live_server_url)
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('Amateur Gaming Community', header.text)

    # под шапкой блога расположены статьи
    def test_home_page_blog(self):
        self.browser.get(self.live_server_url)
        article_list = self.browser.find_element(By.CLASS_NAME, 'article-list')
        self.assertTrue(article_list)

    # У каждой статьи есть заголовок и один абзац с текстом
    def test_home_page_articles_look_correct(self):
        self.browser.get(self.live_server_url)
        article_title = self.browser.find_element(
            By.CLASS_NAME,
            'article-title')
        article_text = self.browser.find_element(
            By.CLASS_NAME,
            'article-text')
        self.assertTrue(article_title)
        self.assertTrue(article_text)

    # кликабельная ссылка на перевод статьи в full text в посте
    def test_home_page_article_title_link_leads_to_article_page(self):
        self.browser.get(self.live_server_url)
        article = self.browser.find_element(
            By.CLASS_NAME,
            'article')
        article_title = article.find_element(
            By.CLASS_NAME,
            'article-title')
        article_title_text = article_title.text
        article_link = article_title.find_element(By.TAG_NAME, 'a')
        href = article_link.get_attribute('href')
        self.browser.get(href)
        article_page_title = self.browser.find_element(
            By.CLASS_NAME,
            'article-title')
        self.assertEqual(article_title_text, article_page_title.text)

    def test_article_link_without_slash_works(self):
        self.browser.get(self.live_server_url)
        article = self.browser.find_element(
            By.CLASS_NAME,
            'article')
        article_title = article.find_element(
            By.CLASS_NAME,
            'article-title')
        article_title_text = article_title.text
        article_link = article_title.find_element(By.TAG_NAME, 'a')
        href = article_link.get_attribute('href')
        if href[-1] == '/':
            href = href[:-1]  # removing trailing slash
        self.browser.get(href)
        article_page_title = self.browser.find_element(By.CLASS_NAME,
                                                       'article-title')
        self.assertEqual(article_title_text, article_page_title.text)

    def test_article_page_header_has_link_that_leads_to_home(self):
        self.browser.get(self.live_server_url)
        initial_url = self.browser.current_url
        article = self.browser.find_element(
            By.CLASS_NAME,
            'article')
        article_title = article.find_element(
            By.CLASS_NAME,
            'article-title')
        article_link = article_title.find_element(By.TAG_NAME, 'a')
        href = article_link.get_attribute('href')
        self.browser.get(href)
        page_header = self.browser.find_element(
            By.CLASS_NAME,
            'avatar-top')
        href_back = page_header.find_element(
            By.TAG_NAME, 'a').get_attribute('href')
        self.browser.get(href_back)
        final_url = self.browser.current_url
        self.assertEqual(initial_url, final_url)

    def test_category_page_displays_correct_articles(self):
        self.browser.get(self.live_server_url)
        article = self.browser.find_element(
            By.CLASS_NAME,
            'article')
        article_footer = article.find_element(
            By.CLASS_NAME,
            'article-footer')
        category_link = article_footer.find_element(By.TAG_NAME, 'a')
        category = category_link.text
        self.browser.get(category_link.get_attribute('href'))
        page = self.browser.find_element(
            By.TAG_NAME,
            'body')
        self.assertIn(category, self.browser.title)
        self.assertIn(category, page.text)
