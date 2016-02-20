# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from subprocess import call


def play_media(file_path):
    call(['mplayer', file_path])
