# -*- coding: utf-8 -*-
"""
Pelicaptcha
===========

A pelican plugin to generate a captcha per article.
"""

import os.path
from pelican import contents, signals
import random
import string
from wheezy.captcha.image import captcha
from wheezy.captcha.image import background
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text
from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp

captcha_db = None
captcha_image = None
output_path = None
sample_input = None

def initialized(pelican):
    init_sample()
    init_captcha(pelican)
    open_captcha_db(pelican)

def init_sample():
    # all uppercase characters except for 'O', no special unicode chars
    characters = string.uppercase[0:14]
    characters = characters + string.uppercase[15:26]

    # all digits except for 0
    digits = string.digits[1:]

    global sample_input
    sample_input = characters + digits

def init_captcha(pelican):
    if not 'PELICAPTCHA_FONT' in pelican.settings:
        raise Exception('please configure a font using the PELICAPTCHA_FONT config variable')
    fonts = [ pelican.settings['PELICAPTCHA_FONT'] ]
    text_drawings = [ warp(), rotate(), offset() ]
    text_function = text(fonts=fonts, drawings=text_drawings)
    drawings = [ background(), text_function, curve(), smooth() ]
    global captcha_image
    captcha_image = captcha(drawings)

def open_captcha_db(pelican):
    global output_path
    output_path = pelican.settings['OUTPUT_PATH']
    path = os.path.join(output_path, 'captchas')

    global captcha_db
    captcha_db = open(path, 'w')

def finalized(pelican):
    captcha_db.close()

def generate_captcha(content):
    if isinstance(content, contents.Static):
        return
    generate_captcha_for_article(content)

def generate_captcha_for_article(article):
    sample = random.sample(sample_input, 5)
    generate_captcha_image(article.slug, sample)
    write_captcha_db(article.slug, sample)

def generate_captcha_image(slug, sample):
    filename = slug + '.jpg'
    path = os.path.join(output_path, filename)
    image = captcha_image(sample)
    image.save(path, 'JPEG', quality=100)

def write_captcha_db(slug, sample):
    captcha_db.write(slug)
    captcha_db.write('\t')
    for character in sample:
        captcha_db.write(character)
    captcha_db.write('\n')

def register():
    signals.initialized.connect(initialized)
    signals.finalized.connect(finalized)
    signals.content_object_init.connect(generate_captcha)
