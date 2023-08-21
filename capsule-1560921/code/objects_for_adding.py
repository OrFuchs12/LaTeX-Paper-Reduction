from random import choice
from string import ascii_lowercase
from essential_generators import DocumentGenerator
import re
import random

gen = DocumentGenerator()


def text(length, with_punc):
    """
        Generate a random sentence.
        Parameters:
        ----------
        length : int
            characters length of the sentence
        with_punc : bool
            with or without punctuation
    """
    res = ''
    punc = ['.', ',']

    if with_punc:
        replacements = [(' ,', ','), (' \.', '.'), (' +', ' '), ('\.,', '.'), (',\.', ','), ('\.+', '.'), (',+', ',')]
    else:
        replacements = [(' +', ' ')]

    while len(res) < length:
        s = gen.paragraph()
        temp = re.sub(r'[^a-zA-Z ]+', '', s)
        temp=temp.replace("f","")
        if with_punc:
            N = random.randint(5, 9)
            lst = temp.split()
            for i in range(N, len(lst), N):
                lst.insert(i, random.choice(punc))
            temp = ' '.join(lst)

        for old, new in replacements:
            temp = re.sub(old, new, temp)

        temp=temp.replace("f", "")
        res += ' ' + temp

    return res[1:length] + "\n"


def section():
    """
        Generate a section tag.
        Parameters:
        ----------
        None
    """
    str = "\\section{Section}\n"
    return str


def sub_section():
    """
        Generate a sub-section tag.
        Parameters:
        ----------
        None
    """
    str = "\\subsection{SubSection}\n"
    return str


def paragraph(n):
    """
        Generate a paragraph tag with random text.
        Parameters:
        ----------
        n : int
            characters length of the paragraph
    """
    temp = text(n, True)
    str = "\\paragraph{Paragraph}\n"
    str += f"{temp}\n"
    return str


def figure(picture_path, width, height, caption_len, with_caption, param=None):
    """
        Generate a figure.
        Parameters:
        ----------
        picture_path : string
            path to the picture
        width : float
            width of the picture
        height : float
            height of the picture
        caption_len : int
            characters length of the caption
        with_caption : bool
            with or without caption
        param : char
            positioning parameter
    """
    str = "\\"
    if param:
        str += "begin{figure}[" + f"{param}" + "]\n"
    else:
        str += "begin{figure}\n"

    str += "\\centering\n"
    str += f"\\includegraphics[width={width}\\columnwidth, height={height}\\paperheight]{{{picture_path}}}\n"

    if with_caption:
        caption = text(caption_len, False)
        str += "\\caption{" + caption + "}\n"

    str += "\\end{figure}\n "
    return str


def table(n_rows, n_cols, col_width, caption_len, with_caption=None, param=None):
    """
        Generate a table.
        Parameters:
        ----------
        n_rows : int
            number of rows of the table
        n_cols : int
            number of columns of the table
        col_width : float
            width of the column in the table
        caption_len : int
            characters length of the caption
        with_caption : bool
            with or without caption
        param : char
            positioning parameter
    """
    if param:
        _str = "\\begin{table}[" + f"{param}" + "]\n"
    else:
        _str = "\\begin{table}\n"

    _str += "\\begin{adjustbox}{width=" + str(col_width) + "\columnwidth}\n"

    temp = ('|l' * n_cols) + '|'

    _str += "\\begin{tabular}{" + f"{temp}" + "}\n"
    _str += "\\hline\n"

    temp = ['& \\multicolumn{1}{c|}{\\textbf{' + f'{i}' + '}} ' for i in range(n_cols - 1)]
    temp = ''.join(temp)
    _str += "\\textbf{plan} " + temp + "\\\\ \hline\n"

    for i in range(n_rows - 1):
        temp = [f"& ({j},0) " for j in range(n_cols - 1)]
        temp = ''.join(temp)
        _str += "\\textbf{$a_" + f"{i}" + "$}  " + temp + "\\\\ \hline\n"

    _str += "\\end{tabular}\n"
    _str += "\\end{adjustbox}\n"

    if with_caption:
        caption = text(caption_len, False)
        _str += "\\caption{" + caption + "}\n"

    _str += "\\end{table}\n"
    return _str


def algorithm(num_lines, param=None):
    """
        Generate an algorithm.
        Parameters:
        ----------
        num_lines : int
            number of rows of the algorithm
        param : char
            positioning parameter
    """
    if param:
        str = "\\begin{algorithm}[" + f"{param}" + "]\n"
    else:
        str = "\\begin{algorithm}\n"

    str += "\\caption{An algorithm with caption}\n"
    str += "\\begin{algorithmic}\n"
    str += "\\While{$N \\neq 0$}\n"
    str += "\    \State $N \\gets N - 1$\n" * (num_lines - 2)
    str += "\\EndWhile\n"
    str += "\\end{algorithmic}\n"
    str += "\\end{algorithm}\n"
    return str


def equation(version):
    """
        Generate an equation.
        Parameters:
        ----------
        version : int
            version of the equation
    """
    if version == 0:
        str = "\\[\\bigvee_{g\\in G} (C^g \\wedge\\ \\bigwedge_{a\\in \\triangle}\\ \\neg h(a)\\ \\wedge\\ \\bigwedge_{a\\notin \\triangle}" \
              "\\ h(a)\\ \\wedge\\ \\{O_j^g\\}_{j=1}^{|A|} \\nvdash\\ \\bot )\\]\n"

    elif version == 1:
        str = "\\[ x^n + y^n = z^n \\]\n"

    elif version == 2:
        str = "\\[\\lim_{h \\rightarrow 0 } \\frac{f(x+h)-f(x)}{h}\\]\n"

    elif version == 3:
        str = "\\[ \\frac{n!}{k!(n-k)!} = \\binom{n}{k} \\]\n"

    elif version == 4:
        str = "\\[ \\int_{a}^{b}{x^{a}y^{b}} \\]\n"

    elif version == 5:
        str = "\\[ \\frac{1+\\frac{a}{b}}{1+\\frac{1}{1+\\frac{1}{a}}} \\]\n"

    elif version == 6:
        str = "\\[ \\sin^2(a)+\\cos^2(a) = 1 \\]\n"

    elif version == 7:
        str = "\\begin{equation}\n"
        str += "spct_{i,j} =\n"
        str += "\\begin{cases}\n"
        str += "1, & \\text{$\\neg af(a_j,g_i) \\wedge \\neg gf(g_i)$}" + "\\" * 2 + "\n"
        str += "0, & \\text{$af(a_j,g_i) \\wedge \\neg gf(g_i)$}" + "\\" * 2 + "\n"
        str += "0, & \\text{$\\neg af(a_j,g_i) \\wedge gf(g_i)$}\n"
        str += "\\end{cases}\n"
        str += "\\end{equation}\n"

    elif version == 8:
        str = "\\begin{equation}\n"
        str += "spct_{i,j} =\n"
        str += "\\begin{cases}\n"
        str += "1, & \\text{$\\neg af(a_j,g_i) \\wedge \\neg gf(g_i)$}" + "\\" * 2 + "\n"
        str += "0, & \\text{$af(a_j,g_i) \\wedge \\neg gf(g_i)$}" + "\\" * 2 + "\n"
        str += "0, & \\text{$\\neg af(a_j,g_i) \\wedge gf(g_i)$}" + "\\" * 2 + "\n"
        str += "1, & \\text{$af(a_j,g_i) \\wedge gf(g_i)$}\n"
        str += "\\end{cases}\n"
        str += "\\end{equation}\n"

    else:
        str = "\\begin{equation}   f =\n"
        str += "\\begin{cases} True, & X \\neq 0" + "\\" * 2 + '\n'
        str += "False, & otherwise\n"
        str += "\\end{cases}\n"
        str += "\\end{equation}\n"

    return str


def enum(n):
    """
        Generate an enumerate list.
        Parameters:
        ----------
        n : int
            length of the enumerate list
    """
    len_of_enum = [x for x in range(50, 200, 10)]
    lst = [text(i, True) for i in len_of_enum]

    str = "\\begin{enumerate}\n"

    for i in range(n):
        temp = random.choice(lst)
        str += "\\item " + temp + "\n"

    str += "\\end{enumerate}\n"
    return str


def definition(n):
    """
        Generate a definition.
        Parameters:
        ----------
        n : int
            characters length of the definition
    """
    temp = text(n, True)

    str = "\\begin{definition}\n"
    str += temp + '\n'
    str += "\\end{definition}\n"
    return str


############# No need #############
"""
def random_text(length):
    return "".join(choice(ascii_lowercase) for i in range(length))
"""
"""
def abstract_paragraph(n):
    temp = "content " * n
    temp = temp[:-1]
    str="\\begin{abstract}\n"
    str+=f"{temp}\n"
    str+="\end{abstract}\n"
    return str
"""
"""
def sub_sub_section():
    str = "\\subsubsection{SubSubSection}\n"
    return str
"""
"""
def sub_figure(picture_path, n, vertical, caption_len):
    str = "\\begin{figure}\n"
    str += "\\centering\n"

    for i in range(n):

        str += "\\begin{subfigure}{.49\columnwidth}\n"
        str += "\\centering\n"
        str += "\\caption{}\n"
        str += "\\includegraphics[width=1\linewidth]{" + f"{picture_path}" + "}\n"
        str += "\\end{subfigure}\n"
        if vertical:
            str += '\n'

    temp = text(caption_len, False)
    str += "\\caption{" + temp + "}\n"
    str += "\\end{figure}\n"
    return str
"""
"""
def matrix(n_rows, n_cols):
    str = "$\\begin{vmatrix}\n"

    temp = "1 & " * (n_cols-1) + "1" + "\\"*2
    row = temp + '\n'
    str += row * (n_rows-1)
    str += temp[:-2] + '\n'

    str += "\\end{vmatrix}$\n"
    return str
"""