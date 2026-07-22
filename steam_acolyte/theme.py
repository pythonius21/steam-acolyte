from PyQt5.QtGui import QIcon, QPixmap

import importlib.resources
from types import SimpleNamespace


def load_theme():
    return SimpleNamespace(
        window_style = load_text_resource('window.css'),
        window_icon = load_icon_resource('acolyte.svg'),
        delete_icon = load_icon_resource('delete.svg'),
        user_icon = load_icon_resource('user.svg', 48, 48),
        plus_icon = load_icon_resource('plus.svg', 48, 48),
    )


def load_text_resource(name):
    return importlib.resources.files(__package__).joinpath(name).read_text()


def load_icon_file(filename, *size):
    icon = QIcon(filename)
    if not icon.isNull():
        if size:
            return icon.pixmap(*size)
        return icon
    return QPixmap()


def load_icon_resource(name, *size):
    ref = importlib.resources.files(__package__).joinpath(name)
    with importlib.resources.as_file(ref) as p:
        return load_icon_file(str(p), *size)
