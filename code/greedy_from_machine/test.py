import perry
import combining_tex_by_content_comparison_functions_h as combining_tex_by_content_comparison_functions
from Last_2_pages_rows_extract import convert_Latex_to_rows_list

def run(latex_path,pdf_path,bib_path):
    try:
        # lidor = Lidor_part.read_file(latex_path, bib_path)
        lidor = convert_Latex_to_rows_list(latex_path, pdf_path)
        print("Finished converting Latex to rows list")
        # lidor = []
        # with open(latex_path, encoding='UTF-8') as f:
        #     file = f.read()
        #     file = file.split("\n")
        #     foundHeader=False
        #     foundBottom=False
        #     for line in file:
        #         line = line.lstrip()
        #         if foundHeader==False:
        #             if line.startswith("\\begin{document}"):
        #                 foundHeader=True
        #             lidor.append("\n")
        #         else:
        #             if foundBottom==False and line.startswith("\\end{document}"):
        #                 foundBottom=True
        #             elif foundBottom == False and line == "":
        #                 continue
        #             else:
        #                 if foundBottom==False:
        #                     lidor.append(line)



        print("starting parsing")
        tags, lines = perry.parse(latex_path, lidor)
        print("finished parsing")
        
        tags_without_figures_and_tables = []
        figures = []
        tables = []
        algorithms = []
        figure_captions_set, table_captions_set = set(), set()
        current_figure = False
        #tags = tags[0][1:]
        #tags = (tags,)
        #print(tags)
        #print(lines)
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

        print("starting combining")
        adi = combining_tex_by_content_comparison_functions.running_from_outside(pdf_path, tags_without_figures_and_tables,
                                                                                 figures, tables, algorithms, lines,
                                                                                 figure_captions_set, table_captions_set)
        print("finished combining")
        # for k in adi[:-1]:
        #     print("---")
        #     for key in k:
        #         print(f"{key}[]{k[key]}")
        return adi
    except Exception as e:
        print(e)
        return []

if __name__=="__main__":

    latex_path = "C:\\Users\\adito\\Desktop\\given\\5067_1.tex"
    #latex_path= "C:\\Users\\adito\\PycharmProjects\\Overleaf_project\\pdf-tests\\1043_1.tex"
    pdf_path= "C:\\Users\\adito\\PycharmProjects\\Overleaf_project\\pdf-tests\\61508_1.pdf"
    bib_path= "C:\\Users\\adito\\PycharmProjects\\Overleaf_project\\pdf-tests\\bibliography.bib"


    adi = run(latex_path,pdf_path,bib_path)
    for k in adi:
        print("---")
        for key in k:
            print(f"{key}[]{k[key]}")
    #
    for k in adi:
        print("------")
        print(f"'Type': {k['Type']}, 'Lines:'")
        print(f"LaTeX:      {k['LaTeX']}")
        print(f"PDF:      ")
        for line in k["pdf_array"]:
            print(f"      {line}")
        print("------")