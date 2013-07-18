Simple comments
===============

This is a plugin for [Pelican](http://docs.getpelican.com) that manages comments as simple files. Comments are generated along with the page.

Usage
-----

Enable this plugin in your `pelicanconf.py` like this

    PLUGIN_PATH = '/path/to/checkout/of/simple_comments'
    PLUGINS = [ 'simple_comments' ]

Configure the location of your comments folder in your `pelicanconf.py`. If you use just a folder name here, the path will be relative to your `pelicanconf.py`.

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
The plugin doesn't care how comments are created as long as they follow the directory structure and file format specified above. Note especially the date format used - the plugin expects exactly this format.

I use a simple php script (see the `php` folder) to create the comments but any other means will do, too.

Turning off comments
--------------------
The plugin adds an `allowcomments` key to each article's metadata. As comments are enabled by default, its value is `True`. If you want to turn off comments for a certain article, specify `AllowComments` with value `False` in the article's metadata.
