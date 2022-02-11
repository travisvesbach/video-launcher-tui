import py_cui
from pathlib import Path
from path_object import PathObject
import os
from home_screen import HomeScreen
from index_screen import IndexScreen
from movie_screen import MovieScreen

# from pprint import pprint
# pprint(vars(selected))


class VideoLauncher:

    # class variables
    home_screen = False
    index_screen = False
    movie_screen = False

    home_screen_set = False
    index_screen_set = False
    movie_screen_set = False
    current_widget_set = False

    # We add type annotations to our master PyCUI objects for improved intellisense
    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        # create widget sets
        self.home_screen = HomeScreen(self)
        self.index_screen = IndexScreen(self)
        self.movie_screen = MovieScreen(self)

        self.home_screen_set = self.home_screen.initialize_screen_elements()
        self.index_screen_set = self.index_screen.initialize_screen_elements()
        self.movie_screen_set = self.movie_screen.initialize_screen_elements()

        self.set_widget_set(self.home_screen_set)

        self.master.toggle_unicode_borders()
        self.master.set_widget_cycle_key(py_cui.keys.KEY_TAB)
        self.master.set_status_bar_text('Focus - Enter | Back - Bcksp | Search - ctrl+w | Navigate - Arrows')




    def set_widget_set(self, widget_set):
        self.master.apply_widget_set(widget_set)
        self.current_widget_set = widget_set
        if widget_set == self.home_screen_set:
            self.home_screen.focus()
        elif widget_set == self.index_screen_set:
            self.index_screen.focus()


    def go_to(self, path = False):
        if not path:
            self.set_widget_set(self.home_screen_set)

        elif not path.parent:
            self.set_widget_set(self.index_screen_set)
            self.index_screen.load(path)
        elif path.type == 'movie':
            self.set_widget_set(self.movie_screen_set)
            self.movie_screen.load(path)




    def open_tvshow(self):
        if self.current_widget_set != self.widget_sets['tvshow']:
            self.set_widget_set(self.widget_sets['tvshow'])
        self.elements['tvshow_plot_box'].clear()
        if self.current.plot:
            width = self.elements['tvshow_plot_box'].get_absolute_stop_pos()[0] - self.elements['tvshow_plot_box'].get_absolute_start_pos()[0] - 6
            self.elements['tvshow_plot_box'].set_text(self.current.display_plot(width))
        self.elements['tvshow_details_box'].clear()
        self.elements['tvshow_details_box'].set_text(self.current.display_details())

