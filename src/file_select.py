import os
import sys
from tkinter import Tk, filedialog


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


    root = Tk()
    root.withdraw()
    # Поднимаем диалоговое окно поверх всех остальных окон
    root.attributes("-topmost", True)

    path = filedialog.askopenfilename(
        title="Выберите файл",
        initialdir=current_dir,
        filetypes=[("CSV файлы", "*.csv"), ("Все файлы", "*.*")],
    )
    root.destroy()
    if not path:
        raise FileNotSelectedError("Файл не был выбран.")

    return os.path.normpath(path)
