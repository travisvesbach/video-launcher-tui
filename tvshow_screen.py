from path_object import PathObject
import os
import py_cui
import threading

class TvshowScreen():

    parent = False
    widgets = {}

    path = False
    search_text = False

    def __init__(self, parent):
        self.parent = parent

    def initialize_screen_elements(self):
        widget_set = self.parent.master.create_new_widget_set(8,6)
        self.add_key_commands(widget_set)

        self.widgets['back_btn'] = widget_set.add_button('Back', 0, 0, command=self.back)
        self.widgets['episodes_btn'] = widget_set.add_button('Episodes', 1, 0, command=self.click_episode_list)
        self.widgets['watched_btn'] = widget_set.add_button('Toggle Watched', 2, 0, command=self.click_watched)
        self.widgets['play_btn'] = widget_set.add_button('Play Next', 3, 0, command=self.click_play)
        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)

        self.widgets['plot'] = widget_set.add_text_block('Plot', 0, 1, row_span=8, column_span=3)
        self.widgets['plot'].set_selectable(False)
        self.add_key_commands(self.widgets['plot'])

        self.widgets['details'] = widget_set.add_text_block('Details', 0, 4, row_span=8, column_span=2)
        self.widgets['details'].set_selectable(False)
        self.add_key_commands(self.widgets['details'])

        return widget_set

    def add_key_commands(self, target):
        target.add_key_command(py_cui.keys.KEY_BACKSPACE, self.back)
        target.add_key_command(py_cui.keys.KEY_CTRL_X, exit)
        target.add_key_command(py_cui.keys.KEY_CTRL_I, self.toggle_help)

    def load(self, path):
        self.path = path
        self.widgets['plot'].clear()
        if not self.path.episode_count:
            self.parent.master.show_loading_icon_popup('Please Wait', 'Loading Episodes')
            threading.Thread(target=self.load_options).start()
        if self.path.plot:
            width = self.widgets['plot'].get_absolute_stop_pos()[0] - self.widgets['plot'].get_absolute_start_pos()[0] - 6
            self.widgets['plot'].set_text(self.path.display_plot(width))
        self.update_details()

    def load_options(self):
        self.path.set_options(True)
        self.parent.master.stop_loading_popup()
        self.update_details()

    def back(self):
        self.parent.go_to(self.path.parent if self.path else False)

    def click_episode_list(self):
        self.parent.go_to(self.path, True)

    def click_watched(self):
        self.parent.master.show_yes_no_popup('This will update all episodes.  Continue?', self.toggle_watched)

    def click_play(self):
        self.path.play()
        self.update_details()
        self.parent.set_recently_watched(self.path)

    def toggle_help(self):
        if self.widgets['details'].get_title() == 'Help':
            self.update_details()
        else:
            message = 'backspace - back\nctrl+h - help\nctrl+x - exit\n'
            self.widgets['details'].set_title('Help')
            self.widgets['details'].clear()
            self.widgets['details'].set_color(py_cui.YELLOW_ON_BLACK)
            self.widgets['details'].set_text(message)

    def toggle_watched(self, proceed = False):
        if proceed:
            self.path.toggle_watched()
            self.update_details()

    def update_details(self):
        self.widgets['details'].set_title('Details')
        self.widgets['details'].set_color(py_cui.WHITE_ON_BLACK)
        self.widgets['details'].clear()
        self.widgets['details'].set_text(self.path.display_details())
        self.widgets['watched_btn'].set_title('Mark ' + ('Unwatched' if self.path.watched == 'true' else 'Watched'))
