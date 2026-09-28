from collections.abc import Iterable

from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell
from openpyxl.cell.cell import TYPE_STRING


def stream_codes_as_exel(filename: str, codes_stream: Iterable[str]) -> None:
    wb = Workbook(write_only=True)
    ws = wb.create_sheet(title="рез")


    for code in codes_stream:
        value = code.split("")[0]
        cell = WriteOnlyCell(ws, value=value)

        # Принудительно устанавливаем текстовый тип
        cell.data_type = TYPE_STRING
        
        ws.append([cell])

    wb.save(filename)

