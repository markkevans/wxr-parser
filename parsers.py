#-*- coding: utf-8 -*-

from lxml import etree
import email.utils
import datetime



class Parser(object):

    def __call__(self, raw_data, **kwargs):
        """Trigger the actual parsing process"""
        try:
            # try to parse raw_data as xml
            self.tree = etree.fromstring(raw_data)

        except etree.ParseError:
            # this is not valid XML, so it's probably a file path
            # me must get file content

            self.tree = etree.ElementTree(file=raw_data)

        self.nsmap = self.get_nsmap(self.tree)
        
        # getting wordpress version
        if kwargs.get("site", True):
            parsed_data = {}
            parsed_data['site'] = self.parse_site_data(self.tree)            

        if kwargs.get("categories", True):
            parsed_data['categories'] = self.parse_categories(self.tree.findall("//*/category[@domain='category']", namespaces=self.nsmap))

        if kwargs.get("tags", True):
            parsed_data['tags'] = self.parse_tags(self.tree.findall("//*/category[@domain='post_tag']", namespaces=self.nsmap))

        if kwargs.get("posts", True):
            parsed_data['posts'] = self.parse_posts(self.tree.findall("channel/item[wp:post_type='post']", namespaces=self.nsmap))

        if kwargs.get("attachments", True):
            parsed_data['attachments'] = self.parse_posts(self.tree.findall("channel/item[wp:post_type='attachment']", namespaces=self.nsmap))

        return parsed_data


    def get_nsmap(self, tree):        
        nsmap = {}
        for ns in tree.xpath('//namespace::*'):
            if ns[0]: # Removes the None namespace, neither needed nor supported.
                nsmap[ns[0]] = ns[1]

        return nsmap

    def parse_site_data(self, tree):

        site_data = {}
        # get site version
        site_data['version'] = tree.find('channel/generator').text.split('v=')[-1]
        site_data['blog_url'] = tree.find('channel/wp:base_blog_url', namespaces=self.nsmap).text

        return site_data

    def parse_categories(self, categories):
        parsed_categories = {}
        for item in categories:
            slug = item.get('nicename')
            if slug not in parsed_categories:
                category = {}
                category['title'] = item.text
                category['slug'] = slug
                parsed_categories[slug] = category

        return parsed_categories

    def parse_tags(self, tags):
        parsed_tags = {}
        for item in tags:
            slug = item.get('nicename')
            if slug not in parsed_tags:
                tag = {}
                tag['title'] = item.text
                tag['slug'] = slug
                parsed_tags[slug] = tag

        return parsed_tags

    def parse_posts(self, posts):
        parsed_posts = []

        for item in posts:
            post = {}
            post['title'] = self.html_entities(item.find('title').text)
            post['slug'] = self.html_entities(item.find('wp:post_name', namespaces=self.nsmap).text)
            post['guid'] = self.html_entities(item.find('guid').text)
            post['id'] = int(item.find('wp:post_id', namespaces=self.nsmap).text)
            post['status'] = item.find('wp:status', namespaces=self.nsmap).text
            post['comment_status'] = item.find('wp:comment_status', namespaces=self.nsmap).text
            post['ping_status'] = item.find('wp:ping_status', namespaces=self.nsmap).text
            post['password'] = item.find('wp:post_password', namespaces=self.nsmap).text
            post['link'] = self.html_entities(item.find('link').text)
            post['content'] = self.html_entities(item.find('content:encoded', namespaces=self.nsmap).text)
            post['creator'] = item.find('dc:creator', namespaces=self.nsmap).text
            post['parent'] = int(item.find('wp:post_parent', namespaces=self.nsmap).text)
            
            # warning, the pub date is not timezone aware
            raw_date = item.find('wp:post_date', namespaces=self.nsmap).text
            parsed_date = datetime.datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')
            post['pub_date'] = parsed_date

            # get post categories
            post['categories'] = []
            for category in item.findall("category[@domain='category']"):
                post['categories'].append(category.get('nicename'))

            # get post tags
            post['tags'] = []
            for tag in item.findall("category[@domain='post_tag']"):
                post['tags'].append(tag.get('nicename'))

            post['comments'] = self.parse_comments(item.findall("wp:comment", namespaces=self.nsmap))
            post['meta'] = self.parse_post_meta(item.findall("wp:postmeta", namespaces=self.nsmap))

            parsed_posts.append(post)       

        return parsed_posts

    def parse_comments(self, comments):
        parsed_comments = []
        for item in comments:
            comment = {}
            comment['id'] = int(item.find('wp:comment_id', namespaces=self.nsmap).text)
            comment['author'] = item.find('wp:comment_author', namespaces=self.nsmap).text
            comment['author_url'] = item.find('wp:comment_author_url', namespaces=self.nsmap).text
            comment['author_IP'] = item.find('wp:comment_author_IP', namespaces=self.nsmap).text
            comment['content'] = item.find('wp:comment_content', namespaces=self.nsmap).text
            comment['approved'] = item.find('wp:comment_approved', namespaces=self.nsmap).text
                
            # warning, the pub date is not timezone aware
            raw_date = item.find('wp:comment_date', namespaces=self.nsmap).text
            parsed_date = datetime.datetime.strptime(raw_date, '%Y-%m-%d %H:%M:%S')
            comment['date'] = parsed_date

            parsed_comments.append(comment)

        return parsed_comments

    def parse_post_meta(self, meta):
        parsed_meta = []
        for item in meta:
            data = {}
            data['id'] = item.find('wp:meta_key', namespaces=self.nsmap).text
            data['value'] = item.find('wp:meta_value', namespaces=self.nsmap).text
            parsed_meta.append(data)

        return parsed_meta

    def html_entities(self, string):
        """Convert unicode to htmlentities"""
        if string is not None:
            return string.encode('ascii', 'xmlcharrefreplace').decode('utf-8')
        return string


parse = Parser()
    
