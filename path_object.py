from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import os

class PathObject:
    def __init__(self, label, path, parent = False, set_options = False):
        self.label = label
        self.path = path
        self.parent = parent
        self.nfo_path = False
        self.title = False
        self.original_title = False
        self.watched = False
        self.last_watched = False
        self.type = False
        self.plot = False
        self.year = False
        self.tagline = False
        self.runtime = False
        self.trailer = False
        self.genre = []
        self.country = False
        self.airing = False
        self.options = self.set_options() if set_options else False

        self.find_nfo()

    def __str__(self):
        return self.display_name()

    def display_name(self):
        output = ''
        if self.type:
            if self.watched == 'true':
                output = output + ' \u2713 '
            elif self.watched == 'in-progress':
                output = output + ' \u25B6 '
            else:
                output = output + '   '

            if self.last_watched:
                output = output + ' ' + self.last_watched + ' '
            else:
                output = output + '            '

            output = output + ' | '
            if self.title:
                output = output + self.title
            else:
                output = output + self.label
        else:
            output = self.label

        return output

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
        output += ('Last Watched: ' + self.last_watched + '\n' if self.last_watched else '')
        return output

    def play_path(self):
        if self.type == 'movie':
            return self.get_dir_list()[0].path


    def find_nfo(self):
        path = Path(self.path + '/tvshow.nfo')
        if path.is_file():
            self.type = 'tvshow'
            self.read_nfo(path)
            return
        path = Path(self.path + '/movie.nfo')
        if path.is_file():
            self.type = 'movie'
            self.read_nfo(path)
            return
        path = Path(os.path.splitext(self.path)[0] + '.nfo')
        if path.is_file():
            self.type = 'episode'
            self.read_nfo(path)
        if self.parent and self.parent.type == 'tvshow':
            self.type = 'season'
        if self.parent and self.parent.type == 'season':
            self.type = 'episode'


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
                self.last_watched = datetime.strftime(datetime.strptime(child.text, '%m/%d/%Y'), '%m/%d/%Y')
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

    def set_options(self, recursive = False):
        dir_contents = []
        for entry in Path(self.path).iterdir():
            if not str(entry).endswith('.jpg') and not str(entry).endswith('.png') and not str(entry).endswith('.srt') and not str(entry).endswith('.nfo'):
                dir_contents.append(PathObject(entry.name, str(entry), self, recursive))
        self.options = dir_contents

    def play(self):
        # set watched and last_watched
        self.watched = 'true'
        self.last_watched = datetime.now().strftime("%m/%d/%Y")
        tree = ET.parse(self.nfo_path)
        root = tree.getroot()
        if len(tree.findall('lastwatched')) > 0:
            tree.find('lastwatched').text = self.last_watched
        else:
            child = ET.Element('lastwatched')
            child.text = self.last_watched
            root.append(child)
        if len(tree.findall('iswatched')) > 0:
            tree.find('iswatched').text = self.watched
        else:
            child = ET.Element('iswatched')
            child.text = self.watched
            root.append(child)
        tree.write(self.nfo_path)
        # if episode, update show's last watched
        # open video
        os.startfile(self.play_path())

    def toggle_watched(self):
        if self.watched == 'true':
            self.watched = 'false'
            self.last_watched = False
        else:
            self.watched = 'true'
            self.last_watched = datetime.now().strftime("%m/%d/%Y")

        tree = ET.parse(self.nfo_path)
        root = tree.getroot()
        if len(tree.findall('lastwatched')) > 0 and self.last_watched == False:
            root.remove(tree.findall('lastwatched')[0])
        elif len(tree.findall('lastwatched')) > 0 and self.last_watched:
            tree.findall('lastwatched')[0].text = self.last_watched
        elif len(tree.findall('lastwatched')) == 0 and self.last_watched:
            child = ET.Element('lastwatched')
            child.text = self.last_watched
            root.append(child)
        if len(tree.findall('iswatched')) > 0:
            tree.findall('iswatched')[0].text = self.watched
        else:
            child = ET.Element('iswatched')
            child.text = self.watched
            root.append(child)
        tree.write(self.nfo_path)
