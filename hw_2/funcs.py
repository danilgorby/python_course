from functools import reduce


def latex_head(func):
    head = "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n"

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        return head + result
    return inner


def latex_tail(func):
    tail = "\\end{document}"

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        return result + tail
    return inner


def generate_tex_table(table):
    column_num = len(table[0])
    table_head = f"\\begin{{table}}[h!]\n\\begin{{tabular}}{{|{'c|' * column_num}}}\n\\hline\n"
    new_lines = map(lambda z: reduce(lambda x, y: f'{x} & {y}', z), table)
    new_lines = map(lambda x: f'{x} \\\\ \hline\n', new_lines)
    body = reduce(lambda x, y: x + y, new_lines)
    table_tail = "\end{tabular}\n\end{table}\n"
    return table_head + body + table_tail


def generate_tex_image(img_path):
    img_head = "\\begin{figure}[h!]\n\\begin{center}\n"
    body = f"\includegraphics[width=16cm]{{{img_path}}}\n"
    img_tail = "\\end{center}\n\\end{figure}\n"
    return img_head + body + img_tail
