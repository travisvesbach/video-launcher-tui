from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import os

class PathObject:
    def __init__(self, label, path, parent = False, directory_type = False, set_options = False):
        self.label = label
        self.path = path
        self.parent = parent
        self.nfo_path = False
        self.title = False
        self.original_title = False
        self.watched = False
        self.last_watched = False
        self.type = directory_type
        self.plot = False
        self.year = False
        self.tagline = False
        self.runtime = False
        self.trailer = False
        self.genre = []
        self.country = False
        self.airing = False
        self.options = False
        self.season_count = False
        self.special_count = False
        self.episode_count = False
        self.season = False
        self.episode = False
        if set_options and os.path.isdir(self.path):
            self.set_options()

        self.find_nfo()

    def __str__(self):
        return self.display_name_prefex() + self.display_name()

    def display_name_prefex(self):
        output = ''
        if self.type and '_dir' not in self.type and self.type != 'season':
            if self.watched == 'true':
                output = output + '\u2713'
            elif self.watched == 'in-progress':
                output = output + '\u25B6'
            else:
                output = output + ' '
            output = output + ' | '
        if self.type == 'episode':
            output = output + str(self.episode).zfill(len(str(len(self.parent.options)))) + '. '
        return output


    def display_name(self):
        return self.title if self.title else self.label

    def display_plot(self, width = False):
        if width:
            output = ""
            for index, letter in enumerate(self.plot):
                if index != 0 and index % width == 0:
                    output += '\n'
                output += letter
            return output
        else:
            return self.plot

    def display_details(self):
        output = ''
        output += ('Year: ' + self.year + '\n' if self.year else '')
        output += ('Country: ' + self.country + '\n' if self.country else '')
        output += ('Genre: ' + ', '.join(self.genre) + '\n' if len(self.genre) > 0 else '')
        output += ('Runtime: ' + self.runtime + ' minutes\n' if self.runtime else '')
        output += ('Seasons: ' + str(self.season_count) + '\n' if self.season_count else '')
        output += ('Episodes: ' + str(self.episode_count) + '\n' if self.episode_count else '')
        output += ('Last Watched: ' + datetime.strftime(self.last_watched, '%m/%d/%Y') + '\n' if self.last_watched else '')
        return output

    def play_path(self):
        if self.type == 'movie':
            return self.options[0].path
        if self.type == 'episode':
            return self.path

    def find_nfo(self):
        path = False
        if self.type == 'tvshow':
            path = Path(self.path + '/tvshow.nfo')
        elif self.type == 'movie':
            path = Path(self.path + '/movie.nfo')
        elif self.type == 'episode':
            path = Path(os.path.splitext(self.path)[0] + '.nfo')
        if path and path.is_file():
            self.read_nfo(path)

    def read_nfo(self, path):
        self.nfo_path = path
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            if child.tag == 'title':
                self.title = child.text
            elif child.tag == 'iswatched':
                self.watched = child.text
            elif child.tag == 'lastwatched':
                self.last_watched = datetime.strptime(child.text, '%m/%d/%Y')
            elif child.tag == 'plot':
                self.plot = child.text
            elif child.tag == 'originaltitle' and child.text != self.title:
                self.original_title = child.text
            elif child.tag == 'year':
                self.year = child.text
            elif child.tag == 'tagline':
                self.tagline = child.text
            elif child.tag == 'runtime':
                self.runtime = child.text
            elif child.tag == 'trailer':
                self.trailer = child.text
            elif child.tag == 'genre':
                self.genre.append(child.text)
            elif child.tag == 'country':
                self.country = child.text
            elif child.tag == 'airing':
                self.airing = child.text
            elif child.tag == 'season':
                self.season = child.text
            elif child.tag == 'episode':
                self.episode = child.text

    def set_options(self, recursive = False):
        dir_contents = []
        for entry in Path(self.path).iterdir():
            if not str(entry).endswith(('.jpg','.png', '.srt','.nfo')):
                directory_type = False
                if '_dir' in self.type:
                    directory_type = self.type.split('_')[0]
                elif self.type == 'movie':
                    directory_type = 'movie'
                elif self.type == 'tvshow':
                    directory_type = 'season'
                elif self.type == 'season':
                    directory_type = 'episode'
                dir_contents.append(PathObject(entry.name, str(entry), self, directory_type, recursive))

        if self.type == 'season':
            self.options = sorted(dir_contents, key=lambda k: int(k.episode))
        else:
            self.options = sorted(dir_contents, key=lambda k: k.title)

        if self.type == 'tvshow':
            season_count = 0
            episode_count = 0
            special_count = 0
            for season in dir_contents:
                season_count = season_count + (1 if 'Season' in season.label else 0)
                special_count = special_count + (1 if 'Special' in season.label else 0)
                episode_count = episode_count + (len(season.options) if season.options else 0)
            self.season_count = season_count if season_count > 0 else False
            self.special_count = special_count if special_count > 0 else False
            self.episode_count = episode_count if episode_count > 0 else False


    def play(self):
        self.toggle_watched('true', True)
        os.startfile(self.play_path())

    def toggle_watched(self, status = None, update_parent = False):
        if status != None:
            self.watched = status
            self.last_watched = False if self.watched == 'false' else datetime.now()
        elif self.watched == 'true':
            self.watched = 'false'
            self.last_watched = False
        else:
            self.watched = 'true'
            self.last_watched = datetime.now()

        self.update_nfo()

        if self.type == 'tvshow' or self.type == 'season':
            for option in self.options:
                option.toggle_watched(self.watched)
        if self.type == 'episode' and update_parent:
            self.parent.parent.toggle_watched_from_child()

    def toggle_watched_from_child(self):
        watched_count = 0
        for season in self.options:
            for episode in season.options:
                if episode.watched == 'true':
                    watched_count = watched_count + 1
        if watched_count == self.episode_count:
            self.watched = 'true'
            self.last_watched = datetime.now()
        elif watched_count > 0 and watched_count < self.episode_count:
            self.watched = 'in-progress'
            self.last_watched = datetime.now()
        else:
            self.watched = 'false'
            self.last_watched = False
        self.update_nfo()

    def update_nfo(self):
        if self.nfo_path:
            tree = ET.parse(self.nfo_path)
            root = tree.getroot()
            if len(tree.findall('lastwatched')) > 0 and self.last_watched == False:
                root.remove(tree.findall('lastwatched')[0])
            elif len(tree.findall('lastwatched')) > 0 and self.last_watched:
                tree.findall('lastwatched')[0].text = self.last_watched.strftime("%m/%d/%Y")
            elif len(tree.findall('lastwatched')) == 0 and self.last_watched:
                child = ET.Element('lastwatched')
                child.text = self.last_watched.strftime("%m/%d/%Y")
                root.append(child)
            if len(tree.findall('iswatched')) > 0:
                tree.findall('iswatched')[0].text = self.watched
            else:
                child = ET.Element('iswatched')
                child.text = self.watched
                root.append(child)
            tree.write(self.nfo_path)
