from funcs import generate_tex_table
from funcs import generate_tex_image
from funcs import latex_head, latex_tail
from hw1_package.image_generation import get_image
from pdflatex import PDFLaTeX

@latex_head
@latex_tail
def easy(table):
    tex_table = generate_tex_table(table)
    return tex_table


@latex_head
def medium_start(table):
    tex_table = generate_tex_table(table)
    return tex_table

@latex_tail
def medium_end():
    get_image()
    tex_image = generate_tex_image('./AST.png')
    return tex_image

table = [[11, 127, 97, 564, 1, 89, 7, 29, 78],
         [8, 91, 88, 91, 31, 10, 5, 34, 991],
         [100, 25, 43, 789, 0, 71, 3, 19, 24]]

if __name__ == "__main__":
    # easy
    tex_table = easy(table)
    with open('./artifacts/table.tex', "w") as f:
        f.write(tex_table)

    # medium
    tex_table = medium_start(table)
    tex_image = medium_end()
    with open('pdf.tex', "w") as f:
        f.write(tex_table + tex_image)
    pdfl = PDFLaTeX.from_texfile('pdf.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)
