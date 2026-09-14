import logging
import os
import sys

from triangle import compute_triangle

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"


def configure_logging():
    os.makedirs("Logs", exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("Logs/file_txt.log", encoding="utf-8"),
        ],
    )


def main():
    configure_logging()
    logging.info("Логгер успешно сконфигурирован")
    logging.info("Приложение запущено")

    try:
        print("Введите длину стороны A:", end=" ")
        side_a = input().strip()
        print("Введите длину стороны B:", end=" ")
        side_b = input().strip()
        print("Введите длину стороны C:", end=" ")
        side_c = input().strip()

        params = {"сторона A": side_a, "сторона B": side_b, "сторона C": side_c}
        logging.info("Получен запрос: A=%r, B=%r, C=%r", side_a, side_b, side_c)

        kind, coords = compute_triangle(side_a, side_b, side_c)

        if kind == "":
            logging.error("Неуспешный запрос: нечисловые данные. Параметры: %s",
                          params)
        elif kind == "не треугольник":
            logging.warning("Неуспешный запрос: данные не образуют треугольник. "
                            "Параметры: %s", params)
        else:
            logging.info("Успешный запрос: параметры %s, результат: тип='%s', "
                         "координаты=%s", params, kind, coords)

        print(f"Тип треугольника: {kind}")
        print(f"Координаты вершин: {coords}")

    except EOFError:
        logging.error("Неуспешный запрос: ввод завершился раньше ожидаемого "
                      "(EOF)")
    except KeyboardInterrupt:
        logging.warning("Приложение остановлено пользователем")
    except Exception as ex:
        logging.exception("Неуспешный запрос: непредвиденная ошибка: %s", ex)
    finally:
        logging.info("Приложение завершено")


if __name__ == "__main__":
    main()