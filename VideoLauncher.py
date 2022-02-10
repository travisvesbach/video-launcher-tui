import py_cui
from pathlib import Path
from path_object import PathObject
import os
from home_screen import HomeScreen
from index_screen import IndexScreen


class VideoLauncher:

    # class variables
    home_screen = False
    index_screen = False

    home_screen_set = False
    index_screen_set = False
    # back = []
    # current = home_dir
    # elements = {}
    widget_sets = {}
    current_widget_set = False
    # options = {}
    # search_text = False

    # We add type annotations to our master PyCUI objects for improved intellisense
    def __init__(self, master: py_cui.PyCUI):

        self.master = master

        # create widget sets
        self.home_screen = HomeScreen(self)
        self.index_screen = IndexScreen(self)

        self.home_screen_set = self.home_screen.initialize_screen_elements()
        self.index_screen_set = self.index_screen.initialize_screen_elements()

        self.set_widget_set(self.home_screen_set)



        self.master.toggle_unicode_borders()
        self.master.set_widget_cycle_key(py_cui.keys.KEY_TAB)
        self.master.set_status_bar_text('Focus - Enter | Back - Bcksp | Search - ctrl+w | Navigate - Arrows')


        # self.widget_sets['index'] = self.master.create_new_widget_set(8,6)
        # self.widget_sets['movie'] = self.master.create_new_widget_set(8, 6)
        # self.widget_sets['tvshow'] = self.master.create_new_widget_set(8, 6)

        # home elements
        # self.elements['home_dir_list'] = self.widget_sets['home'].add_scroll_menu('Directories', 0, 1, row_span=8, column_span=3)

        # index elements
        # self.elements['index_search_btn'] = self.widget_sets['index'].add_button('Search', 1, 0, command=self.show_search)
        # self.elements['index_dir_list'] = self.widget_sets['index'].add_scroll_menu('List', 0, 1, row_span=8, column_span=3)
        # self.elements['index_dir_list'].set_on_selection_change_event(self.set_summary)
        # self.elements['index_plot_box'] = self.widget_sets['index'].add_text_block('Plot', 0, 4, row_span=8, column_span=2)
        # self.widget_sets['index'].add_key_command(py_cui.keys.KEY_CTRL_W, self.show_search)
        # self.elements['index_dir_list'].add_key_command(py_cui.keys.KEY_CTRL_W, self.show_search)

        # tvshow elements
        # self.elements['tvshow_plot_box'] = self.widget_sets['tvshow'].add_text_block('Plot', 0, 1, row_span=8, column_span=3)
        # self.elements['tvshow_details_box'] = self.widget_sets['tvshow'].add_text_block('Details', 0, 4, row_span=8, column_span=2)

        # # movie elements
        # self.elements['movie_play_btn'] = self.widget_sets['movie'].add_button('Play', 1, 0, command=self.click_play)
        # self.elements['movie_watched_btn'] = self.widget_sets['movie'].add_button('Toggle Watched', 2, 0, command=self.click_watched)
        # self.elements['movie_plot_box'] = self.widget_sets['movie'].add_text_block('Plot', 0, 1, row_span=8, column_span=3)
        # self.elements['movie_details_box'] = self.widget_sets['movie'].add_text_block('Details', 0, 4, row_span=8, column_span=2)


        # self.set_commands_and_defaults()
        # self.set_widget_set(self.widget_sets['home'])
        # self.open_dir(self.current)

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
            self.index_screen.open(path)

        # if self.current == self.home_dir:
        #     self.search_text = False
        #     self.set_widget_set(self.widget_sets['home'])
        # elif self.current_widget_set != self.widget_sets['index']:
        #     self.set_widget_set(self.widget_sets['index'])
        # if path.type:
        #     if path.type == 'movie':
        #         self.open_movie()
        #     elif path.type == 'tvshow':
        #         self.open_tvshow()
        # else:
        #     if not self.current.path in self.options:
        #         self.add_dir_list()
        #     if self.current == self.home_dir:
        #         # print(len(self.options[self.current.path]))
        #         self.set_widget_set(self.widget_sets['home'])
        #         self.elements['home_dir_list'].clear()
        #         self.elements['home_dir_list'].add_item_list(self.options[self.current.path])
        #     else:
        #         self.set_widget_set(self.widget_sets['index'])
        #         self.elements['index_dir_list'].clear()
        #         self.elements['index_plot_box'].clear()
        #         self.elements['index_dir_list'].add_item_list(self.filter_options(self.options[self.current.path]))
        #         self.set_summary()












    # def show_search(self):
    #     self.master.show_text_box_popup('Search', self.search)

    # def search(self, text):
    #     self.search_text = text
    #     self.open_dir(self.current)

    def click_dir_list(self):
        if self.current == self.home_dir:
            selected = self.elements['home_dir_list'].get()
        else:
            selected = self.elements['index_dir_list'].get()

        if len(self.back) == 0 or selected.path != self.back[-1].path:
            self.back.append(self.current)
        elif selected == self.back[-1]:
            self.back.pop()
        self.open_dir(selected)

    def click_play(self):
        self.current.play()
        self.update_details()

    def click_watched(self):
        self.current.toggle_watched()
        self.update_details()

    def update_details(self):
        if self.current_widget_set == self.widget_sets['movie']:
            self.elements['movie_details_box'].clear()
            self.elements['movie_details_box'].set_text(self.current.display_details())
            self.elements['movie_watched_btn'].set_title('Mark ' + ('Unwatched' if self.current.watched == 'true' else 'Watched'))

    def go_back(self):
        if len(self.back) > 0:
            self.current = self.back[-1]
            self.back.pop()
            self.open_dir(self.current)

    def add_dir_list(self):
        self.options[self.current.path] = self.current.get_dir_list()

    def open_dir(self, path):
        self.current = path
        if self.current == self.home_dir:
            self.search_text = False
            self.set_widget_set(self.widget_sets['home'])
        elif self.current_widget_set != self.widget_sets['index']:
            self.set_widget_set(self.widget_sets['index'])
        if path.type:
            if path.type == 'movie':
                self.open_movie()
            elif path.type == 'tvshow':
                self.open_tvshow()
        else:
            if not self.current.path in self.options:
                self.add_dir_list()
            if self.current == self.home_dir:
                # print(len(self.options[self.current.path]))
                self.set_widget_set(self.widget_sets['home'])
                self.elements['home_dir_list'].clear()
                self.elements['home_dir_list'].add_item_list(self.options[self.current.path])
            else:
                self.set_widget_set(self.widget_sets['index'])
                self.elements['index_dir_list'].clear()
                self.elements['index_plot_box'].clear()
                self.elements['index_dir_list'].add_item_list(self.filter_options(self.options[self.current.path]))
                self.set_summary()


    def filter_options(self, options):
        if self.search_text:
            return [option for option in options if self.search_text.lower() in option.display_name().lower()]
        else:
            return options


    def open_tvshow(self):
        if self.current_widget_set != self.widget_sets['tvshow']:
            self.set_widget_set(self.widget_sets['tvshow'])
        self.elements['tvshow_plot_box'].clear()
        if self.current.plot:
            width = self.elements['tvshow_plot_box'].get_absolute_stop_pos()[0] - self.elements['tvshow_plot_box'].get_absolute_start_pos()[0] - 6
            self.elements['tvshow_plot_box'].set_text(self.current.display_plot(width))
        self.elements['tvshow_details_box'].clear()
        self.elements['tvshow_details_box'].set_text(self.current.display_details())

    def open_movie(self):
        if self.current_widget_set != self.widget_sets['movie']:
            self.set_widget_set(self.widget_sets['movie'])
        self.elements['movie_plot_box'].clear()
        if self.current.plot:
            width = self.elements['movie_plot_box'].get_absolute_stop_pos()[0] - self.elements['movie_plot_box'].get_absolute_start_pos()[0] - 6
            self.elements['movie_plot_box'].set_text(self.current.display_plot(width))
        self.elements['movie_details_box'].clear()
        self.elements['movie_details_box'].set_text(self.current.display_details())
        self.elements['movie_watched_btn'].set_title('Mark ' + ('Unwatched' if self.current.watched == 'true' else 'Watched'))


    # def set_summary(self):
    #     self.elements['index_plot_box'].clear()
    #     selected = self.elements['index_dir_list'].get()
    #     if selected.plot:
    #         width = self.elements['index_plot_box'].get_absolute_stop_pos()[0] - self.elements['index_plot_box'].get_absolute_start_pos()[0] - 6
    #         self.elements['index_plot_box'].set_text(selected.display_plot(width))
