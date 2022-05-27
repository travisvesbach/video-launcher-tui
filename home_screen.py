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

    directories = []

    dir_path = False
    dir_name = False


    def __init__(self, parent):
        self.parent = parent
        # self.anime_dir = PathObject('Anime', os.getenv('ANIME_DIR'), False, 'tvshow_dir')
        # self.movies_dir = PathObject('Movies', os.getenv('MOVIES_DIR'), False, 'movie_dir')
        # self.tvshows_dir = PathObject('TV Shows', os.getenv('TVSHOWS_DIR'), False, 'tvshow_dir')
        if 'directories' in self.parent.settings:
            for directory in self.parent.settings['directories']:
                self.directories.append(PathObject(directory['label'], directory['path'], False, directory['type']))



    def initialize_screen_elements(self):
        widget_set = self.parent.master.create_new_widget_set(8,6)
        self.widgets['directories'] = widget_set.add_scroll_menu('Directories', 0, 1, row_span=8, column_span=2)
        # self.widgets['directories'].add_item_list([self.anime_dir, self.movies_dir, self.tvshows_dir])
        self.widgets['directories'].add_item_list(self.directories)
        self.widgets['directories'].set_selected_color(py_cui.GREEN_ON_BLACK)
        self.widgets['directories'].add_key_command(py_cui.keys.KEY_ENTER, self.open_directory)
        self.widgets['directories'].add_mouse_command(py_cui.keys.LEFT_MOUSE_DBL_CLICK, self.open_directory)

        self.widgets['add_dir_button'] = widget_set.add_button('Add Directory', 0, 0, command=self.show_dir_name_box)


        self.widgets['exit_btn'] = widget_set.add_button('Exit', 7, 0, command=exit)
        self.widgets['exit_btn'].set_color(py_cui.RED_ON_BLACK)

        return widget_set

    def settings(self):
        self.parent.go_to('settings')

    def open_directory(self):
        selected = self.widgets['directories'].get()
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
