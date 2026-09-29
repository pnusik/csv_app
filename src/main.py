from csv_logic import get_badcodes, get_csv_codes_iterator, stream_codes_as_csv
from exel_logic import stream_codes_as_exel
from file_select import select_file


def main():
    try:
        mode = None
        while True:
            print("Выберете режим:\n1.Создание кодов без исключений.\n2.С исключениями(браком)")
            mode = input().strip()
            if mode not in ["1", "2"]:
                print("Неизвестный режим")
            else: break

        print("Выбор файла от медузы")
        good_codes_path = select_file()

        badcodes = None
        if mode == "2":
            print("Укажите файл с бракованными кодами")
            badcodes_path = select_file()
            badcodes = get_badcodes(badcodes_path)

        shift, csv_iterator = get_csv_codes_iterator(good_codes_path, bad_codes=badcodes)

        with stream_codes_as_csv(f"shift_{shift}_csv_codes_full.csv") as csv, stream_codes_as_exel(f"shift_{shift}_exel_codes_short.xlsx") as exel:
            for code in csv_iterator:
                csv.writecode(code)
                exel.writecode(code)

    except Exception as e:  # noqa: BLE001
        print(f"\033[31m\nОШИБКА!!!\n{e}\033[0m")
    finally:
        input("Программа завершена.")


if __name__ == "__main__":
    main()