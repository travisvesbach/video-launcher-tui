from path_object import PathObject
import os
import py_cui
import threading

class IndexScreen():

    parent = False
    widgets = {}

    path = False
    search_text = False
    sort_by = 'Alphabetical'

    def __init__(self, parent):
        self.parent = parent

    def initialize_screen_elements(self):
        widget_set = self.parent.master.create_new_widget_set(8,6)
        self.parent.master.set_status_bar_text('Focus - Enter | Back - Bcksp | Info/Help - ctrl+i| Navigate - Arrows')
        self.add_key_commands(widget_set)

        self.widgets['back_btn'] = widget_set.add_button('Back', 0, 0, command=self.back)
        self.widgets['search_btn'] = widget_set.add_button('Search', 1, 0, command=self.show_search)

        self.widgets['genre_filter'] = widget_set.add_checkbox_menu('Genre', 2, 0, row_span=4)
        self.widgets['genre_filter'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.set_genre_filters()
        self.add_key_commands(self.widgets['genre_filter'])

        self.widgets['filter_btn'] = widget_set.add_button('Filter', 6, 0, command=self.load)

        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)

        self.widgets['index'] = widget_set.add_scroll_menu('Directories', 0, 1, row_span=8, column_span=3)
        self.widgets['index'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['index'].set_on_selection_change_event(self.update_details)
        self.widgets['index'].add_key_command(py_cui.keys.KEY_ENTER, self.open)
        self.widgets['index'].add_mouse_command(py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.open)
        self.add_key_commands(self.widgets['index'])

        self.widgets['plot'] = widget_set.add_text_block('Plot', 0, 4, row_span=5, column_span=2)
        self.widgets['plot'].set_selectable(False)
        self.add_key_commands(self.widgets['plot'])

        self.widgets['details'] = widget_set.add_text_block('Details', 5, 4, row_span=3, column_span=2)
        self.widgets['details'].set_selectable(False)
        self.add_key_commands(self.widgets['details'])

        return widget_set

    def add_key_commands(self, target):
        target.add_key_command(py_cui.keys.KEY_BACKSPACE, self.back)
        target.add_key_command(py_cui.keys.KEY_CTRL_X, exit)
        target.add_key_command(py_cui.keys.KEY_CTRL_I, self.toggle_help)
        target.add_key_command(py_cui.keys.KEY_CTRL_W, self.show_search)
        target.add_key_command(py_cui.keys.KEY_CTRL_S, self.show_sort)
        target.add_key_command(py_cui.keys.KEY_CTRL_UP, self.genre_back)
        target.add_key_command(py_cui.keys.KEY_CTRL_DOWN, self.genre_next)
        target.add_key_command(py_cui.keys.KEY_CTRL_LEFT, self.genre_toggle)
        target.add_key_command(py_cui.keys.KEY_CTRL_RIGHT, self.load)

    def focus(self, target = 'index'):
        self.parent.master.move_focus(self.widgets[target])

    def focus_genre_filter(self):
        self.focus('genre_filter')

    def show_search(self):
        self.parent.master.show_text_box_popup('Search', self.search)

    def show_sort(self):
        self.parent.master.show_menu_popup('Sort', ['Alphabetical', 'Last Watched', 'Year'], self.sort, run_command_if_none=False)

    def toggle_help(self):
        if self.widgets['plot'].get_title() == 'Help':
            self.update_details()
        else:
            message = 'backspace - back\nctrl+h - toggle help\nctrl+s - sort\nctrl+w - search\nctrl+up/down - up/down in genre\nctrl+left - toggle genre\nctrl+right - apply filters\nctrl+x - exit\n'
            self.widgets['plot'].set_title('Help')
            self.widgets['plot'].clear()
            self.widgets['plot'].set_color(py_cui.YELLOW_ON_BLACK)
            self.widgets['plot'].set_text(message)

    def search(self, text):
        self.search_text = text
        self.load(self.path)

    def load(self, path = False):
        reset_genres = True if not self.path else False
        self.path = path if path else self.path
        if not self.path.options:
            self.parent.master.show_loading_icon_popup('Please Wait', 'Loading ' + self.path.label)
            threading.Thread(target=self.load_options).start()
        self.reset(reset_genres)

    def load_options(self):
        self.path.set_options(True)
        self.parent.master.stop_loading_popup()
        self.reset(True)

    def reset(self, reset_genres = False):
        self.set_genre_filters(reset_genres)
        self.widgets['index'].set_title(self.path.label)
        self.widgets['index'].clear()
        self.widgets['plot'].clear()
        self.widgets['details'].clear()
        if self.path.options:
            self.widgets['index'].add_item_list(self.filter_options())
        self.focus()
        self.update_details()

    def filter_options(self):
        filtered_genres = [key for key,value in self.widgets['genre_filter']._selected_item_dict.items() if value == True]
        options = self.path.options if self.path else []
        if len(filtered_genres) > 0:
            options = [option for option in options if set(filtered_genres).issubset(set(option.genre))]
        if self.search_text:
            options = [option for option in options if self.search_text.lower() in option.display_name().lower()]
        if self.sort_by == 'Last Watched':
            options = sorted(options, key=lambda k: (k.last_watched is not False, k.last_watched), reverse=True)
        if self.sort_by == 'Year':
            options = sorted(options, key=lambda k: (k.year is None, k.year))
        return options

    def update_details(self):
        self.widgets['plot'].set_title('Plot')
        self.widgets['plot'].clear()
        self.widgets['plot'].set_color(py_cui.WHITE_ON_BLACK)
        selected = self.widgets['index'].get()
        if selected and selected.plot:
            width = self.widgets['plot'].get_absolute_stop_pos()[0] - self.widgets['plot'].get_absolute_start_pos()[0] - 6
            self.widgets['plot'].set_text(selected.display_plot(width))
            self.widgets['details'].set_text(selected.display_details())

    def back(self):
        self.search_text = False
        self.path = False
        self.parent.go_to()

    def open(self):
        selected = self.widgets['index'].get()
        self.parent.go_to(selected)

    def set_genre_filters(self, reset = False):
        filtered_genres = [key for key,value in self.widgets['genre_filter']._selected_item_dict.items() if value == True]
        self.widgets['genre_filter'].clear()
        filters = []
        options = (self.filter_options() if not reset else (self.path.options if self.path else None))
        if options and len(options) > 0:
            genre = {genre for option in options for genre in option.genre}
            filters = filters + sorted(genre)
        filters = sorted(list(set(filters + filtered_genres)))
        self.widgets['genre_filter'].add_item_list(filters)
        if not reset:
            for genre in filtered_genres:
                self.widgets['genre_filter'].toggle_item_checked(genre)

    def sort(self, sort):
        self.sort_by = sort
        self.load()

    def genre_back(self):
        self.widgets['genre_filter']._scroll_up()

    def genre_next(self):
        self.widgets['genre_filter']._scroll_down(self.widgets['genre_filter'].get_viewport_height())

    def genre_toggle(self):
        self.widgets['genre_filter'].toggle_item_checked(self.widgets['genre_filter'].get())
