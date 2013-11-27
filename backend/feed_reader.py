#!/usr/bin/env python

import feedparser
from HTMLParser import HTMLParser
import json
from datetime import datetime

class ImgParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.images = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    self.images.append(attr[1])

# read the file containing all the feed URLs
feeds_fp = open('feeds.json')
feeds = json.load(feeds_fp)
feeds_fp.close()

entries = []

def find_img(content):
    img_parser = ImgParser()
    img_parser.feed(content)
    img_parser.close()
    return img_parser.images

def iso_date(date_list):
    d = datetime(date_list[0], date_list[1], date_list[2], date_list[3], date_list[4], date_list[5])
    return '{:%Y-%m-%dT%H:%M:%S}'.format(d)


for person in feeds:
    try:
        d = feedparser.parse(person['feed_url'])
        for entry in d.entries:
            post = {}
            images = []
            post['name'] = person['name']
            post['title'] = entry.title
            post['link'] = entry.link
            post['published'] = iso_date(entry.published_parsed)
            post['id'] = entry.id
            if 'content' in entry:
                images = find_img(entry.content[0].value)
            else:
                images = find_img(entry.description)
            post['image'] = None
            if len(images) > 0:
                post['image'] = images[0]
            #if 'description' in entry:
            #    post['description'] = entry.description
            entries.append(post)
    except:
        print "error processing ", person['feed_url']

print json.dumps(entries)

