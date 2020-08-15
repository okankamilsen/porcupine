import tkinter

from porcupine import get_main_window
from porcupine.plugins.urls import find_urls


def test_find_urls(porcusession):
    text = tkinter.Text(get_main_window())
    text.insert('end', '''\
          https://github.com/Akuli/porcupine/
          https://github.com/Akuli/porcupine/ bla bla
"See also https://github.com/Akuli/porcupine/"
         'https://github.com/Akuli/porcupine/ bla'
         (http://example.com/)
         {http://example.com/}      <-- this might occur in Tcl code, for example
         [http://example.com/]
         <http://example.com/>
         (http://example.com/))()
        ("http://example.com/")bla
        "(http://example.com/)" :)
         (http://example.com/ )   <-- often used with tools that don't understand parenthesized urls
''')

    porcupine_len = len('https://github.com/Akuli/porcupine/')
    example_len = len('http://example.com/')

    assert [(text.index(start), text.index(end)) for start, end in find_urls(text)] == [
        ('1.10', f'1.{10 + porcupine_len}'),
        ('2.10', f'2.{10 + porcupine_len}'),
        ('3.10', f'3.{10 + porcupine_len}'),
        ('4.10', f'4.{10 + porcupine_len}'),
        ('5.10', f'5.{10 + example_len}'),
        ('6.10', f'6.{10 + example_len}'),
        ('7.10', f'7.{10 + example_len}'),
        ('8.10', f'8.{10 + example_len}'),
        ('9.10', f'9.{10 + example_len}'),
        ('10.10', f'10.{10 + example_len}'),
        ('11.10', f'11.{10 + example_len}'),
        ('12.10', f'12.{10 + example_len}'),
    ]
