WXR-parser is a very simple parser for Wordpress eXtended RSS files, writtent in Python.

Feed it with a WXR file and it will return data about posts, categories, tags and comments, inside a dictionary, so you can use this data in your own projects.

Compatibility
=============

WXR-parser has been tested under Python 2.7 and 3.4.

Installation
============

The recommanded install process is using `pip`, which will also handle any dependencies::

    pip install wxr-parser

If you install it manually, you should also install `lxml <http://lxml.de/>`_.

Usage
=====

You can use the parser with the following instructions::

    import wxr_parser

    # parse a file
    parsed_data = wxr_parser.parse('path_to_your_wxr.xml')

You can also parse a string containing WXR data.

Output
======

WXR-parser returns a standard Python dictionary, with following keys:

- `site`: data about the website. Not fully implemented.
- `categories`: categories data (described below)
- `tags`: tags data (described below)
- `posts`: posts data (described below)

Categories
**********

A dictionary of parsed categories, with categories nicenames as keys::

    parsed_data['categories']

    # output
    {
        'a-category': {'slug': 'a-category',
                       'title': 'A category'},
        'another-category': {'slug': 'another-category',
                             'title': 'Another category'},
        'uncategorized': {'slug': 'uncategorized',
                          'title': 'Uncategorized'}
    }

Tags
****

A dictionary of parsed tags, with tags nicenames as keys::

    parsed_data['tags']

    # output
    {
        'another-tag': {'slug': 'another-tag',
                        'title': 'another tag'},
        'arbitrary-tag': {'slug': 'arbitrary-tag',
                          'title': 'arbitrary tag'},
        'some-tag': {'slug': 'some-tag',
                     'title': 'Some tag'}
    }

Posts
*****

A list of dictionaries, each dictionary corresponding to a parsed post::

    # get the first parsed post
    parsed_data['posts'][0]

    # output

    {
        'categories': ['uncategorized'],
        'comment_status': 'open',
        'comments': [{'author': 'Mr WordPress',
                      'author_IP': None,
                      'author_url': 'http://wordpress.org/',
                      'content': 'Hi, this is a comment.<br />To delete a comment, just log in and view the post&#039;s comments. There you will have the option to edit or delete them.',
                      'date': datetime.datetime(2012, 7, 1, 18, 32, 32),
                      'id': 1}],
        'content': u'Welcome to WordPress. This is your first post. Edit or delete it, then start blogging!',
        'creator': 'admin',
        'guid': u'http://demo.opensourcecms.com/wordpress/?p=1',
        'id': 1,
        'link': u'http://demo.opensourcecms.com/wordpress/?p=1',
        'password': None,
        'ping_status': 'open',
        'pub_date': datetime.datetime(2012, 7, 1, 18, 32, 32),
        'slug': u'hello-world',
        'status': 'publish',
        'tags': [],
        'title': u'Hello world!'
    }


Changelog
=========

0.1 - 12/10/2014
****************

Initial release.

Contributions
=============

Contributions and feedback are welcome. You can fork the project and send me a link to your forked repo so I can merge it.

Feel free to email me at <contact@eliotberriot.com>. 

License
=======

The project is licensed under BSD licence.


