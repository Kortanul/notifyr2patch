import re
import html


class HtmlTransformer:
  NESTED_MARKUP_WRAPPER_TAG = '<tt>'

  NEW_LINE_PATTERN = re.compile(r'<br\s?/?>')
  NESTED_MARKUP_PATTERN = re.compile(r'^<tt>(.*)</tt>')

  @classmethod
  def contains_nested_markup(cls, html_string):
    return html_string.startswith(cls.NESTED_MARKUP_WRAPPER_TAG)

  def __init__(self, string):
    self.string = string

  def unpack_nested_markup(self):
    self.string = HtmlTransformer.NESTED_MARKUP_PATTERN.sub(r'\1', self.string)

    return self

  def unescape_markup(self):
    self.string = html.unescape(self.string)

    return self

  def remove_newlines(self):
    self.string = self.string.replace('\n', '')

    return self

  def decode_newlines(self):
    self.string = HtmlTransformer.NEW_LINE_PATTERN.sub('\n', self.string)

    return self

  def decode_spaces(self):
    self.string = self.string.replace('&nbsp;', ' ')

    return self

  def __str__(self):
    return self.string
