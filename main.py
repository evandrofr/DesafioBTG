import re
import time
from functools import wraps

import pandas as pd


def timeit(log_string: str):
    """ Decorator that logs a function time elapsed, with a custom message """

    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = function(*args, **kwargs)
            time_elapsed = f'{(time.perf_counter() - start):.2f}'
            print(log_string.format(time_elapsed=time_elapsed))
            return result
        return wrapper
    return real_decorator


def read_rain_file(file_path: str) -> pd.DataFrame:
    with open(file_path, 'r') as f:
        raw_file = f.readlines()

    list_dados = [line.split() for line in raw_file]
    float_raw_lines = [list(map(float, raw_line)) for raw_line in list_dados]
    return pd.DataFrame(float_raw_lines, columns=['lat', 'long', 'data_value'])


def read_contour_file(file_path: str) -> pd.DataFrame:
    line_split_comp = re.compile(r'\s*,')

    with open(file_path, 'r') as f:
        raw_file = f.readlines()

    l_raw_lines = [line_split_comp.split(raw_file_line.strip()) for raw_file_line in raw_file]
    l_raw_lines = list(filter(lambda item: bool(item[0]), l_raw_lines))
    float_raw_lines = [list(map(float, raw_line))[:2] for raw_line in l_raw_lines]
    header_line = float_raw_lines.pop(0)
    assert len(float_raw_lines) == int(header_line[0])
    return pd.DataFrame(float_raw_lines, columns=['lat', 'long'])


def apply_contour(contour_df: pd.DataFrame, rain_df: pd.DataFrame) -> pd.DataFrame:
    pass


def main() -> None:
    contour_df: pd.DataFrame = read_contour_file('PSATCMG_CAMARGOS.bln')
    rain_df: pd.DataFrame = read_rain_file('forecast_files/ETA40_p011221a021221.dat')
    contour_df: pd.DataFrame = apply_contour(contour_df, rain_df)


if __name__ == '__main__':
    main()
