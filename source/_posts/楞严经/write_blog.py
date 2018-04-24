#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

root_dir = os.getcwd()

def get_pic_files(root_dir):

    print(root_dir)

    pic_files = []
    files = os.listdir(root_dir)
    for i in range(0, len(files)):
        f = files[i]
        ext = os.path.splitext(f)[1]
        if ext=='.jpg' or ext=='.png':
            pic_files.append(f)

    return pic_files

def md_pic_link(f):
    #pic_link = '{%% asset_img %s %%}' % f
    pic_link = '![%s](楞严经/%s)' % (f,f)
    return pic_link

pic_files = get_pic_files(root_dir)

parent_path = os.path.dirname(root_dir)

with open(os.path.join(parent_path, '楞严经.md'), 'w') as mdf:
    mdf.write('---\n')
    mdf.write('title: 楞严经\n')
    mdf.write('date: 2017-10-01 10:03:37\n')
    mdf.write('categories: Budhi\n')
    mdf.write('tags:\n')
    mdf.write('    - 楞严经\n')
    mdf.write('---\n')
    mdf.write('\n')
    mdf.write('\n')
    for i in range(0, len(pic_files)):
        mdf.write(md_pic_link(pic_files[i])+'\n')