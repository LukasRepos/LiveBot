import math
from typing import List


def table(data: List[str], columns: int, padding=1):
    cut_point = math.ceil(len(data) / columns)
    table = [[] for _ in range(cut_point)]
    curr_line = -1
    for i in range(max(len(data), columns * cut_point)):
        if i < len(data):
            d = data[i]
            relative_index = data.index(d) % columns
            if relative_index == 0:
                curr_line += 1
            table[curr_line].append(d)
        else:
            table[curr_line].append("")

    formated_table = [[] for _ in range(cut_point)]
    table_T = list(zip(*table))
    column_max = [max([len(ln) for ln in line]) for line in table_T]

    for ln_index, line in enumerate(table):
        for col_index, (en_index, entry) in zip(range(len(column_max)), enumerate(line)):
            formated_table[ln_index].append(entry + " " * (column_max[col_index] - len(entry)))

    result = "\n".join([(" " * padding).join(line) for line in formated_table])
    return result
