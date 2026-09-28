import itertools
import multiprocessing as mp

from csv_logic import get_badcodes, get_csv_codes_iterator, stream_codes_as_csv
from exel_logic import stream_codes_as_exel
from file_select import select_file


def main():
    mode = None
    while True:
        print("Выберете режим:\n1.Создание кодов без исключений.\n2.С исключениями(браком)")
        mode = int(input())
        if mode not in [1, 2]:
            print("Неизвестный режим")
        else: break

    print("Выбор файла от медузы")
    good_codes_path = select_file()

    badcodes = None
    if mode == 2:
        print("Укажите файл с бракованными кодами")
        badcodes_path = select_file()
        badcodes = get_badcodes(badcodes_path)

    csv_iterator = get_csv_codes_iterator(good_codes_path, bad_codes=badcodes)
    it1, it2 = itertools.tee(csv_iterator, 2)

    stream_codes_as_csv("csv_codes_full.csv", it1)
    stream_codes_as_exel("exel_codes_short.xlsx", it2)

    input("Программа завершена.")





if __name__ == "__main__":
    main()