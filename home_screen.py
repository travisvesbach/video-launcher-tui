from path_object import PathObject
import os
import py_cui

class HomeScreen():

    parent = False
    widgets = {}
    # options = {}

    anime_dir = False
    movies_dir = False
    tvshows_dir = False

    def __init__(self, parent):
        self.parent = parent

        self.anime_dir = PathObject('Anime', os.getenv('ANIME_DIR'), False, 'tvshow_dir')
        self.movies_dir = PathObject('Movies', os.getenv('MOVIES_DIR'), False, 'movie_dir')
        self.tvshows_dir = PathObject('TV Shows', os.getenv('TVSHOWS_DIR'), False, 'tvshow_dir')


    def initialize_screen_elements(self):
        widget_set = self.parent.master.create_new_widget_set(8,6)
        self.widgets['index'] = widget_set.add_scroll_menu('Directories', 0, 1, row_span=8, column_span=3)
        self.widgets['index'].add_item_list([self.anime_dir, self.movies_dir, self.tvshows_dir])
        self.widgets['index'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['index'].add_key_command(py_cui.keys.KEY_ENTER, self.open_directory)
        self.widgets['index'].add_mouse_command(py_cui.keys.LEFT_MOUSE_CLICK, self.open_directory)

        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)

        return widget_set

    def open_directory(self):
        selected = self.widgets['index'].get()
        self.parent.go_to(selected)


    def focus(self):
        self.parent.master.move_focus(self.widgets['index'])
