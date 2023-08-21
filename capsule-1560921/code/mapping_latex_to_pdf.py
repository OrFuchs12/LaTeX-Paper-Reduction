import main_parsing
import combining_tex_by_content_comparison_functions as combining_tex_by_content_comparison_functions

def run(latex_path,pdf_path,bib_path):
    """

    :param latex_path: path to tex file
    :param pdf_path: path to pdf file
    :param bib_path: path to bib file
    :return: mapping every tex element to its location in pdf
    """
    try:
        original_lines = []
        with open(latex_path, encoding='UTF-8') as file:
            # doc = file.read()

            foundHeader=False
            foundBottom=False
            for line in file:
                if foundHeader==False:
                    if line.startswith("\\begin{document}"):
                        foundHeader=True
                    original_lines.append("\n")
                else:
                    if foundBottom==False and line.startswith("\\end{document}"):
                        foundBottom=True
                    else:
                        if foundBottom==False:
                            original_lines.append(line)


        #tex parsing and tokenizing tree
        tags, lines = main_parsing.parse(latex_path, original_lines)

        tags_without_figures_and_tables = []
        figures = []
        tables = []
        algorithms = []
        figure_captions_set, table_captions_set = set(), set()
        current_figure = False
        for k, j in tags:
            if k[0].startswith("Figure"):
                current_figure = True
                current_table = False
                helper = list(k)
                helper.append("False")

                figures.append((tuple(helper), j))

            elif k[0].startswith("Table"):
                current_figure = False
                current_table = True
                helper = list(k)
                helper.append("False")
                tables.append((tuple(helper), j))

            elif k[0].startswith("CaptionFigure"):
                if current_figure:
                    previous_figure = list(figures[-1])
                    p1 = list(previous_figure[0])
                    p1[-1] = "True"
                    previous_figure[0] = tuple(p1)
                    figures[-1] = tuple(previous_figure)
                current_figure = False
                current_table = False
                # figures.append(k)
                figure_captions_set.add((k, j))
            elif k[0].startswith("CaptionTable"):
                if current_table:
                    previous_table = list(tables[-1])
                    p1 = list(previous_table[0])
                    p1[-1] = "True"
                    previous_table[0] = tuple(p1)
                    tables[-1] = tuple(previous_table)
                current_figure = False
                current_table = False
                # tables.append(k)
                table_captions_set.add((k, j))
            elif k[0].startswith("Algorithm"):
                current_figure = False
                current_table = False
                algorithms.append((k, j))
            else:
                current_figure = False
                current_table = False
                tags_without_figures_and_tables.append((k, j))

        new_lines = []
        for k in lines:
            if k[0].startswith("Caption"):
                continue
            new_lines.append(k)

        lines = new_lines

        results_lst = combining_tex_by_content_comparison_functions.running_from_outside(pdf_path, tags_without_figures_and_tables,
                                                                                 figures, tables, algorithms, lines,
                                                                                 figure_captions_set, table_captions_set)
        # for k in results_lst[:-1]:
        #     print("---")
        #     for key in k:
        #         print(f"{key}[]{k[key]}")
        return results_lst
    except Exception as e:
        print(e)
        return []

# if __name__=="__main__":
#
#     latex_path = ""
#     pdf_path= ""
#     bib_path= ""
#
#
#     results_lst = run(latex_path,pdf_path,bib_path)
#     for k in results_lst:
#         print("---")
#         for key in k:
#             print(f"{key}[]{k[key]}")
#     #
#     for k in results_lst:
#         print("------")
#         print(f"'Type': {k['Type']}, 'Lines:'")
#         print(f"LaTeX:      {k['LaTeX']}")
#         print(f"PDF:      ")
#         for line in k["pdf_array"]:
#             print(f"      {line}")
#         print("------")