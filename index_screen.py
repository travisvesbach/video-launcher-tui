from path_object import PathObject
import os
import py_cui

class IndexScreen():

    parent = False
    widgets = {}

    path = False
    search_text = False

    def __init__(self, parent):
        self.parent = parent

    def initialize_screen_elements(self):
        widget_set = self.parent.master.create_new_widget_set(8,6)

        widget_set.add_key_command(py_cui.keys.KEY_BACKSPACE, self.back)
        widget_set.add_key_command(py_cui.keys.KEY_CTRL_W, self.show_search)

        self.widgets['index'] = widget_set.add_scroll_menu('Directories', 0, 1, row_span=8, column_span=3)
        self.widgets['index'].add_key_command(py_cui.keys.KEY_ENTER, self.open)
        self.widgets['index'].add_mouse_command(py_cui.keys.LEFT_MOUSE_CLICK, self.open)
        self.widgets['index'].add_key_command(py_cui.keys.KEY_BACKSPACE, self.back)
        self.widgets['index'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['index'].add_key_command(py_cui.keys.KEY_CTRL_W, self.show_search)
        self.widgets['index'].set_on_selection_change_event(self.show_summary)

        self.widgets['plot'] = widget_set.add_text_block('Plot', 0, 4, row_span=8, column_span=2)
        self.widgets['plot'].add_key_command(py_cui.keys.KEY_BACKSPACE, self.back)
        self.widgets['plot'].set_selectable(False)

        self.widgets['back_btn'] = widget_set.add_button('Back', 0, 0, command=self.back)
        self.widgets['search_btn'] = widget_set.add_button('Search', 1, 0, command=self.show_search)
        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)


        return widget_set


    def focus(self):
        self.parent.master.move_focus(self.widgets['index'])

    def back(self):
        self.parent.go_to()

    def show_search(self):
        self.parent.master.show_text_box_popup('Search', self.search)

    def search(self, text):
        self.search_text = text
        self.open(self.path)

    def open(self, path):
        self.path = path

        if not path.options:
            path.set_options(True)

        self.widgets['index'].set_title(path.label)
        self.widgets['index'].clear()
        self.widgets['plot'].clear()
        self.widgets['index'].add_item_list(self.filter(path.options))
        self.focus()
        self.show_summary()

    def filter(self, options):
        if self.search_text:
            return [option for option in options if self.search_text.lower() in option.display_name().lower()]
        else:
            return options

    def show_summary(self):
        self.widgets['plot'].clear()
        selected = self.widgets['index'].get()
        if selected.plot:
            width = self.widgets['plot'].get_absolute_stop_pos()[0] - self.widgets['plot'].get_absolute_start_pos()[0] - 6
            self.widgets['plot'].set_text(selected.display_plot(width))
