from collections.abc import Iterable

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.cell.cell import TYPE_STRING


class stream_codes_as_exel:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __enter__(self):
        self.wb = Workbook(write_only=True)
        self.ws = self.wb.create_sheet(title="рез")
        return self

    def writecode(self, code: str):
        value = code.split("")[0]
        cell = WriteOnlyCell(self.ws, value=value)
        # Принудительно устанавливаем текстовый тип
        cell.data_type = TYPE_STRING
        
        self.ws.append([cell])

    def __exit__(self, exc_type, exc, tb):
        self.wb.save(self.filename)

