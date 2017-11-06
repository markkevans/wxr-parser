#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from .. import parsers
import datetime
import os

class TestWXRParser(unittest.TestCase):


    def abs_path(self, file_name):
        """Return an absolute path to a file stored in tests directory"""
        d = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(d, file_name)

    def test_can_detect_wordpress_version_from_file(self):
        data = parsers.parse(self.abs_path("sample0.xml"), posts=False)
        self.assertEqual(data['site']['version'], "3.6")
        self.assertEqual(data['site']['blog_url'], "http://demo.wordpress-fr.net")


    def test_can_get_posts(self):
        data = parsers.parse(self.abs_path("sample0.xml"))
        self.assertEqual(len(data['posts']), 3)

    def test_can_parse_posts(self):

        posts = parsers.parse(self.abs_path("sample0.xml"))['posts']
        
        post = posts[0]

        self.assertEqual(post['title'], "Bonjour tout le monde&#160;!")
        self.assertEqual(post['creator'], "admin")
        self.assertEqual(post['id'], 1)
        self.assertEqual(post['status'], 'publish')
        self.assertEqual(post['comment_status'], 'open')
        self.assertEqual(post['ping_status'], 'open')
        self.assertEqual(post['id'], 1)
        self.assertEqual(post['password'], None)
        self.assertIn("puis lancez-vous&#160;!", post['content'])
        self.assertEqual(post['pub_date'], datetime.datetime(2011, 8, 8, 21, 52, 24))
        self.assertEqual(post['slug'], "bonjour-tout-le-monde")
        self.assertEqual(post['guid'], "http://demo.wordpress-fr.net/?p=1")
        self.assertEqual(post['link'], "http://demo.wordpress-fr.net/bonjour-tout-le-monde/")

        self.assertEqual(post['categories'], ['conferences', 'non-classe'])
        self.assertEqual(post['tags'], ['hello'])

    def test_can_parse_comments(self):
        posts = parsers.parse(self.abs_path("sample0.xml"))['posts']
        
        comments = posts[0]['comments']
        comment = comments[1]

        #     <wp:comment_content><![CDATA[Marketing and advertising and sales differ considerably, but have the exact same target. 
        self.assertEqual(comment['id'], 2)
        self.assertEqual(comment['author'], "Jjchaeldedo")
        self.assertEqual(comment['author_url'], "http://www.smgtv.co.uk/pandora-charms.html")
        self.assertEqual(comment['author_IP'], "193.201.224.38")
        self.assertEqual(comment['date'], datetime.datetime(2014, 10, 10, 20, 1, 20))
        self.assertIn("advertising and sales differ", comment['content'])


    def test_can_parse_categories(self):
        categories = parsers.parse(self.abs_path("sample0.xml"))['categories']

        self.assertEqual(len(categories), 2)

        category = categories['non-classe']
        self.assertEqual(category['slug'], "non-classe")
        self.assertEqual(category['title'], "Non classé")

        category = categories['conferences']
        self.assertEqual(category['slug'], "conferences")
        self.assertEqual(category['title'], "Conférences")

    def test_can_parse_tags(self):
        tags = parsers.parse(self.abs_path("sample0.xml"))['tags']

        self.assertEqual(len(tags), 2)

        tag = tags['hello']
        self.assertEqual(tag['slug'], "hello")
        self.assertEqual(tag['title'], "hello")

        tag = tags['un-mot-cle']
        self.assertEqual(tag['slug'], "un-mot-cle")
        self.assertEqual(tag['title'], "un mot clé")



if __name__ == '__main__':
    unittest.main()