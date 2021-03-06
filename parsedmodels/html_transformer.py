import re
import html


class HtmlTransformer:
  NESTED_MARKUP_WRAPPER_TAG = '<tt>'

  NEW_LINE_PATTERN = re.compile(r'<br\s?/?>')

  NESTED_MARKUP_PATTERN = \
    re.compile(r'^<tt>(.*)</tt>$', flags=re.MULTILINE|re.DOTALL)

  @classmethod
  def contains_nested_markup(cls, html_string):
    return html_string.startswith(cls.NESTED_MARKUP_WRAPPER_TAG)

  def __init__(self, string):
    self.string = string

  def unpack_nested_markup(self):
    self.string = self.NESTED_MARKUP_PATTERN.sub(r'\1', str(self)).strip()

    return self

  def unescape_markup(self):
    self.string = html.unescape(self.string)

    return self

  def remove_newlines(self):
    self.string = self.string.replace('\n', '')

    return self

  def decode_newlines(self):
    self.string = self.NEW_LINE_PATTERN.sub('\n', self.string)

    return self

  def decode_nonbreaking_spaces(self):
    self.string = self.string.replace('&nbsp;', ' ').replace(u'\u00A0', ' ')

    return self

  def __str__(self):
    return self.string
