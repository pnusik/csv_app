import os
import sys

from plyer import filechooser


class FileNotSelectedError(Exception):
    pass

def select_file() -> str:
    """Выбор файла юзером"""
    if getattr(sys, "frozen", False):
        # Если скрипт скомпилирован в .exe
        current_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # Если запускается обычный .py файл
        current_dir = os.path.dirname(os.path.abspath(__file__))

    if not callable(filechooser.open_file):
        raise TypeError("Выбор файла не доступен, plyer не заработал ._.")

    path = filechooser.open_file(
        title="Выберите файл",
        path=current_dir,
        filters=[("csv файл", "*.csv")],
    )

    if not path:
        raise TypeError("Файл не выбран")

    return str(path[0]) # type: ignore


print(select_file())