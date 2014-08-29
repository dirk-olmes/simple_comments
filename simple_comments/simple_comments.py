# -*- coding: utf-8 -*-
"""
Simple comments
===============

A pelican plugin to read comments from files in the filesystem.
"""

import codecs
import os
import os.path
from pelican import contents, signals

comment_path = None

def initialized(pelican):
    global comment_path
    if 'COMMENT_PATH' in pelican.settings:
        comment_path = pelican.settings['COMMENT_PATH']
        if not os.path.isabs(comment_path):
            base_path = pelican.settings['PATH']
            comment_path = os.path.join(base_path, comment_path)

def read_comments_for_content(content):
    if isinstance(content, contents.Static):
        return
    read_comments_for_article(content)

def read_comments_for_article(article):
    init_metadata(article)
    article_path = os.path.join(comment_path, article.slug)
    if not os.path.exists(article_path):
        return
    comments = read_comments(article_path)
    sort_function = lambda dict: dict['Date']
    comments.sort(key=sort_function)
    article.comments = comments

def init_metadata(article):
    if 'allowcomments' in article.metadata:
        value = article.metadata['allowcomments'].lower()
        article.metadata['allowcomments'] = value in ('true', 'yes', '1')
    else:
        article.metadata['allowcomments'] = True

def read_comments(article_path):
    comments = []
    for path, _, comment_files in os.walk(article_path):
        for comment_file in comment_files:
            comment = read_comment(path, comment_file)
            comments.append(comment)
    return comments

def read_comment(path, filename):
    comment_file = os.path.join(path, filename)
    comment, text = read_metadata_and_text(comment_file)
    comment['text'] = text
    return comment

def read_metadata_and_text(comment_file):
    metadata = {}
    text = ''
    reading_meta = True
    with codecs.open(comment_file, encoding='utf-8') as f:
        for line in f:
            if len(line.strip()) == 0 and reading_meta:
                reading_meta = False
            if reading_meta:
                index = line.index(':')
                key = line[0:index]
                value = line[index+1:].strip()
                metadata[key] = value
            else:
                text = text + line
    return metadata, text

def register():
    signals.initialized.connect(initialized)
    signals.content_object_init.connect(read_comments_for_content)
