import py_cui
from pathlib import Path
from path_object import PathObject
import os
from home_screen import HomeScreen
from index_screen import IndexScreen
from movie_screen import MovieScreen
from tvshow_screen import TvshowScreen
from episode_list_screen import EpisodeListScreen
import time
import json

# from pprint import pprint
# pprint(vars(selected))


class VideoLauncher:

    # class variables
    home_screen = False
    index_screen = False
    movie_screen = False
    tvshow_screen = False
    episode_list_screen = False

    home_screen_set = False
    index_screen_set = False
    movie_screen_set = False
    tvshow_screen_set = False
    episode_list_screen_set = False

    settings = {}
    settings_file = 'settings.json'

    # We add type annotations to our master PyCUI objects for improved intellisense
    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        self.settings = json.load(open(self.settings_file, 'r'))

        # create widget sets
        self.home_screen = HomeScreen(self)
        self.index_screen = IndexScreen(self)
        self.movie_screen = MovieScreen(self)
        self.tvshow_screen = TvshowScreen(self)
        self.episode_list_screen = EpisodeListScreen(self)

        self.home_screen_set = self.home_screen.initialize_screen_elements()
        self.index_screen_set = self.index_screen.initialize_screen_elements()
        self.movie_screen_set = self.movie_screen.initialize_screen_elements()
        self.tvshow_screen_set = self.tvshow_screen.initialize_screen_elements()
        self.episode_list_screen_set = self.episode_list_screen.initialize_screen_elements()

        self.master.apply_widget_set(self.home_screen_set)
        self.home_screen.focus()

        self.master.toggle_unicode_borders()
        self.master.set_widget_cycle_key(py_cui.keys.KEY_TAB)


    def go_to(self, path = False, episodes = False):
        if not path:
            self.master.apply_widget_set(self.home_screen_set)
            self.home_screen.focus()
        elif not path.parent:
            self.master.apply_widget_set(self.index_screen_set)
            self.index_screen.load(path)
        elif path.type == 'movie':
            self.master.apply_widget_set(self.movie_screen_set)
            self.movie_screen.load(path)
        elif path.type == 'tvshow' and not episodes:
            self.master.apply_widget_set(self.tvshow_screen_set)
            self.tvshow_screen.load(path)
        elif path.type == 'tvshow' and episodes:
            self.master.apply_widget_set(self.episode_list_screen_set)
            self.episode_list_screen.load(path)

    def save_settings(self):
        with open(self.settings_file, 'w') as file_object:
            json.dump(self.settings, file_object)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()
