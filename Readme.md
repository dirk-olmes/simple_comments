Simple comments
===============

This is a plugin for [Pelican](http://docs.getpelican.com) that manages comments as simple files. Comments are generated along with the page.

Usage
-----

Enable this plugin in your `pelicanconf.py` like this

    PLUGIN_PATH = '/path/to/checkou/of/simple_comments'
    PLUGINS = [ 'simple_comments' ]

Configure the location of your comments folder in your `pelicanconf.py`

    COMMENT_PATH = '/path/to/your/comments'

Update your theme to include the comments on each page

    {% if article.comments %}
        {% for comment in article.comments %}
            <div>{{ comment.Author }}</div>
            <div>{{ comment.Date }}</div>
            <div>{{ comment.text }}</div>
        {% endfor %}
    {% endif %}


Comment format
--------------

Inside COMMENT_PATH, comments are organized in a directory structure. Each directory represents a blog post, comments are stored as individual files

    /comments
    ├── blog-post1
    │   ├── comment1
    │   └── comment2
    │── blog-post2
    └   └── comment1

Each blog post begins with metadata, followed by an empty line and finally the comment itself

    Author: the-author@test.com
    Date: 2001-01-01 12:00:00

    this is a very sensible blog post comment


Creating comments
-----------------
The plugin doesn't care how comments are created as long as they follow the directory structure and file format specified above.