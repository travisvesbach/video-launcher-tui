from path_object import PathObject
import os
import py_cui

class EpisodeListScreen():

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

        self.widgets['seasons'] = widget_set.add_scroll_menu('Seasons', 1, 0, row_span=4, column_span=1)
        self.widgets['seasons'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['seasons'].set_on_selection_change_event(self.update_episode_list)
        self.add_key_commands(self.widgets['seasons'])

        self.widgets['watched_btn'] = widget_set.add_button('Play', 5, 0, command=self.click_play)
        self.widgets['watched_btn'] = widget_set.add_button('Toggle Watched', 6, 0, command=self.click_watched)

        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)

        self.widgets['episodes'] = widget_set.add_scroll_menu('Episodes', 0, 1, row_span=8, column_span=3)
        self.widgets['episodes'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['episodes'].set_on_selection_change_event(self.update_details)
        self.widgets['episodes'].add_key_command(py_cui.keys.KEY_ENTER, self.click_play)
        self.add_key_commands(self.widgets['episodes'])

        self.widgets['plot'] = widget_set.add_text_block('Plot', 0, 4, row_span=6, column_span=2)
        self.widgets['plot'].set_selectable(False)
        self.add_key_commands(self.widgets['plot'])

        self.widgets['details'] = widget_set.add_text_block('Details', 6, 4, row_span=2, column_span=2)
        self.widgets['details'].set_selectable(False)
        self.add_key_commands(self.widgets['details'])

        return widget_set

    def add_key_commands(self, target):
        target.add_key_command(py_cui.keys.KEY_BACKSPACE, self.back)
        target.add_key_command(py_cui.keys.KEY_CTRL_X, exit)
        target.add_key_command(py_cui.keys.KEY_CTRL_I, self.toggle_help)
        target.add_key_command(py_cui.keys.KEY_CTRL_UP, self.season_back)
        target.add_key_command(py_cui.keys.KEY_CTRL_DOWN, self.season_next)
        target.add_key_command(py_cui.keys.KEY_CTRL_W, self.click_watched)

    def focus(self, target = 'episodes'):
        self.parent.master.move_focus(self.widgets[target])

    def load(self, path):
        self.path = path
        self.widgets['seasons'].clear()
        self.widgets['episodes'].clear()
        self.widgets['details'].clear()
        self.widgets['seasons'].add_item_list(self.path.options)
        self.update_episode_list()
        self.update_details()
        self.focus()

    def back(self):
        self.parent.go_to(self.path)

    def click_play(self):
        self.widgets['episodes'].get().play()
        self.update_details()

        self.parent.set_recently_watched(self.path)

    def click_watched(self):
        self.widgets['episodes'].get().toggle_watched(None, True)
        self.update_details()

    def toggle_help(self):
        if self.widgets['plot'].get_title() == 'Help':
            self.update_details()
        else:
            message = 'backspace - back\nctrl+h - help\nctrl+up/down - up/down in season\nctrl+w - toggle watched\nctrl+x - exit\n'
            self.widgets['plot'].set_title('Help')
            self.widgets['plot'].clear()
            self.widgets['plot'].set_color(py_cui.YELLOW_ON_BLACK)
            self.widgets['plot'].set_text(message)

    def update_episode_list(self):
        self.widgets['episodes'].clear()
        selected = self.widgets['seasons'].get()
        if selected.options:
            self.widgets['episodes'].add_item_list(selected.options)
        self.update_details()

    def update_details(self):
        self.widgets['plot'].set_title('Plot')
        self.widgets['plot'].set_color(py_cui.WHITE_ON_BLACK)
        self.widgets['plot'].clear()
        self.widgets['details'].clear()
        selected = self.widgets['episodes'].get()
        if selected.plot:
            width = self.widgets['plot'].get_absolute_stop_pos()[0] - self.widgets['plot'].get_absolute_start_pos()[0] - 6
            self.widgets['plot'].set_text(selected.display_plot(width))
        self.widgets['details'].set_text(selected.display_details())
        self.widgets['watched_btn'].set_title('Mark ' + ('Unwatched' if selected.watched == 'true' else 'Watched'))

    def season_back(self):
        self.widgets['seasons']._scroll_up()
        self.update_episode_list()

    def season_next(self):
        self.widgets['seasons']._scroll_down(self.widgets['seasons'].get_viewport_height())
        self.update_episode_list()
