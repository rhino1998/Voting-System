"""This file contains miscellaneous utility functions
"""

#Misc imports
import os
import markdown
import bleach

#Pygments imports
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer, ScssLexer
from pygments.formatters import HtmlFormatter

#Werkzeug imports
from werkzeug.routing import BaseConverter

#WTForms imports
from wtforms.validators import ValidationError



def valid_chars(form, field):
    """Checks for valid characters
    """
    if special(field.data):
        raise ValidationError('Invalid Characters')
def special(text):
    """Determines if a string contains special characters
    """
    return not all(ord(c) < 128 for c in text)

def list_replace(items, item, index):
    """Replaces and makes a new list
    """
    temp = list(items)
    temp.pop(index)
    temp.insert(index, item)
    return temp

def list_remove(items, index):
    temp = list(items)
    temp.pop(index)
    return temp
#Captures html and parses markdown
def sanitize(text):
    return markdown.markdown(
        bleach.clean(text),
        extensions=['markdown.extensions.nl2br']
    )
def preview(text):
    """Captures html and parses markdown and truncates to end of first paragraph
    """
    return "".join(sanitize(text).partition('</p>')[:1])

def doc(path):
    """Gathers the documentation
    """
    file_ = open(path, 'r')
    content = file_.read()
    file_.close()
    try:
        lexer = get_lexer_for_filename(path, stripall=True)
    except:
        lexer = TextLexer(stripall=True)
    if path.endswith('.md'):
        return markdown.markdown(
            bleach.clean(content),
            extensions=['markdown.extensions.nl2br', 'markdown.extensions.toc']
        )
    elif path.endswith('.less'):
        lexer = ScssLexer(stripall=True)

    formatter = HtmlFormatter(
        linenos=True,
        cssclass='codehilight',
        noclobber_cssfile=True,
        title=path[path.rfind(os.sep)+1:]
    )
    return "<div class='table-responsive codehilight'>"+highlight(content, lexer, formatter)+"</div>"

def combine_results(results, submissions):
    """Adds results arrays together
    """
    if results != []:
        for submission in submissions:
            result = next((result for result in results if result['index'] == submission['index']), None)
            for entry in submission['data']:
                datum = next((datum for datum in result['data'] if datum[0] == entry[0]), None)
                if datum:
                    datum[1] += entry[1]
                else:
                    result['data'].append(entry)
            result['data'].sort(key=lambda x : x[1], reverse=True)
        return results
    else:
        return submissions

#Defines a new url variable type, File
class FileConverter(BaseConverter):

    def __init__(self, url_map):
        super(FileConverter, self).__init__(url_map)
        self.regex = '[^\s]*\.*[^\s]*'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return BaseConverter.to_url(value)
