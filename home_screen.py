from path_object import PathObject
import os
import py_cui

class HomeScreen():

    parent = False
    widgets = {}

    anime_dir = False
    movies_dir = False
    tvshows_dir = False

    directories = []
    recently_watched = []

    dir_path = False
    dir_name = False


    def __init__(self, parent):
        self.parent = parent
        if 'directories' in self.parent.settings:
            for directory in self.parent.settings['directories']:
                self.directories.append(PathObject(directory['label'], directory['path'], False, directory['type']))



    def initialize_screen_elements(self):
        widget_set = self.parent.master.create_new_widget_set(8,6)
        self.widgets['directories'] = widget_set.add_scroll_menu('Directories', 0, 1, row_span=8, column_span=2)
        self.widgets['directories'].add_item_list(self.directories)
        self.widgets['directories'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['directories'].add_key_command(py_cui.keys.KEY_ENTER, self.open_directory)
        self.widgets['directories'].add_mouse_command(py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.open_directory)

        self.widgets['recently_watched'] = widget_set.add_scroll_menu('Recently Watched', 0, 3, row_span=3, column_span=3)
        self.widgets['recently_watched'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['recently_watched'].add_key_command(py_cui.keys.KEY_ENTER, self.open_recent)
        self.widgets['recently_watched'].add_mouse_command(py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.open_recent)
        self.set_recently_watched()

        self.widgets['menu_button'] = widget_set.add_button('Menu', 0, 0, command=self.show_menu)

        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)

        return widget_set

    def set_recently_watched(self):
        self.recently_watched = []
        if 'recently_watched' in self.parent.settings:
            for recent in self.parent.settings['recently_watched']:
                self.recently_watched.append(PathObject(recent['label'], recent['path'], next((x for x in self.directories if x.path == recent['parent_path']), False), recent['type']))
        self.widgets['recently_watched'].clear()
        self.widgets['recently_watched'].add_item_list(self.recently_watched)

    def show_menu(self):
        self.parent.master.show_menu_popup('Directory Options', ['Add Directory', 'Remove Directory', 'Remove Recently Watched'], self.process_menu, run_command_if_none=False)

    def process_menu(self, command):
        if command == 'Add Directory':
            self.show_dir_name_box();
        elif command == 'Remove Directory':
            self.show_remove_dir_list_menu();
        elif command == 'Remove Recently Watched':
            self.show_remove_recent_list_menu();
        return

    def open_directory(self):
        selected = self.widgets['directories'].get()
        self.parent.go_to(selected)

    def open_recent(self):
        selected = self.widgets['recently_watched'].get()
        self.parent.go_to(selected)

    def focus(self):
        self.parent.master.move_focus(self.widgets['directories'])

    def show_dir_name_box(self, text = False):
        self.parent.master.show_text_box_popup('Name?' + (text if text else ''), self.check_dir_name)

    def check_dir_name(self, text):
        if text == '':
            self.show_dir_name_box(' - Cannot be blank')
        elif any(x.label == text for x in self.directories):
            self.show_dir_name_box(' - A directory named "' + text + '" already exists.')
        else:
            self.dir_name = text
            self.show_dir_path_box()

    def show_dir_path_box(self, text = False):
        self.parent.master.show_text_box_popup('Path?' + (text if text else ''), self.check_dir_path)

    def check_dir_path(self, text):
        if text == '':
            self.show_dir_path_box(' - Cannot be blank')
        elif any(x.path == text for x in self.directories):
            self.show_dir_path_box(' - A directory with path "' + text + '" already exists.')
        else:
            self.dir_path = text
            self.show_dir_type_box()

    def show_dir_type_box(self):
        self.parent.master.show_yes_no_popup('Does this directory have directories with Episodes?', self.add_dir)

    def add_dir(self, has_episodes):
        dir_type = 'tvshow_dir' if has_episodes else 'movie_dir'
        self.directories.append(PathObject(self.dir_name, self.dir_path, False, dir_type))
        self.directories.sort(key=lambda x: x.label)
        self.widgets['directories'].clear()
        self.widgets['directories'].add_item_list(self.directories)
        self.parent.set_setting('directories', [x.to_dictionary() for x in self.directories])

    def show_remove_dir_list_menu(self):
        self.parent.master.show_menu_popup('Select Directory to Remove', self.directories, self.remove_dir, run_command_if_none=False)

    def remove_dir(self, text):
        self.directories.remove(text)
        self.widgets['directories'].clear()
        self.widgets['directories'].add_item_list(self.directories)
        self.parent.set_setting('directories', [x.to_dictionary() for x in self.directories])

    def show_remove_recent_list_menu(self):
        self.parent.master.show_menu_popup('Select Recently Watched to Remove', self.recently_watched, self.remove_recent, run_command_if_none=False)

    def remove_recent(self, text):
        self.recently_watched.remove(text)
        self.widgets['recently_watched'].clear()
        self.widgets['recently_watched'].add_item_list(self.recently_watched)
        self.parent.set_setting('recently_watched', [x.to_dictionary() for x in self.recently_watched])
