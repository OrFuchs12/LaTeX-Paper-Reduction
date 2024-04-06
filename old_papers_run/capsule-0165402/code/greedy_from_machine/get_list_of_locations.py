
def run(latex_path):

    lidor = []
    with open(latex_path, encoding='UTF-8') as file:
        # doc = file.read()

        foundHeader = False
        foundBottom = False
        for line in file:
            if foundHeader == False:
                if line.startswith("\\begin{document}"):
                    foundHeader = True
                lidor.append("\n")
            else:
                if foundBottom == False and line.startswith("\\end{document}"):
                    foundBottom = True
                else:
                    if foundBottom == False:
                        lidor.append(line)


    dct={"CaptionFigure":[],"CaptionTable":[],"Figure":[],"Table":[],"Algorithm":[],"Paragraph":[],
         "Par":[],"Formula":[],"Section":[],"SubSection":[],"Enum":[],"FigureSpecific":[],"TableSpecific":[],
         "AlgorithmSpecific":[]}

    lineIndex=1
    scope=""
    current_scope=""
    for original_line in lidor:
        line=original_line.replace("\n","")
        line=line.replace(" ","")
        if line=="": #separation_line
            current_scope=""

        if line.startswith("\\section{"):
            dct["Section"].append(lineIndex)
            scope = ""
            current_scope="Section"

        elif line.startswith("\\subsection{"):
            dct["SubSection"].append(lineIndex)
            scope = ""
            current_scope="SubSection"

        elif line.startswith("\\begin{figure}"):
            scope = "Figure"
            current_scope="Figure"
            if line.find("[")!=-1:
                helperstr=line.split("[")[1]
                helperstr=helperstr.split("]")[0]
                dct["FigureSpecific"].append((lineIndex, helperstr))
            else:
                dct["Figure"].append(lineIndex)

        elif line.startswith("\\begin{table}"):
            scope = "Table"
            current_scope="Table"

            if line.find("[") != -1:
                helperstr = line.split("[")[1]
                helperstr = helperstr.split("]")[0]
                dct["TableSpecific"].append((lineIndex, helperstr))
            else:
                dct["Table"].append(lineIndex)

        elif line.startswith("\\begin{algorithm}"):
            scope = ""
            current_scope="Algorithm"

            if line.find("[") != -1:
                helperstr = line.split("[")[1]
                helperstr = helperstr.split("]")[0]
                dct["AlgorithmSpecific"].append((lineIndex, helperstr))
            else:
                dct["Algorithm"].append(lineIndex)

        elif line.startswith("\\[") or line.startswith("\\begin{equation"):
            dct["Formula"].append(lineIndex)
            scope = ""
            current_scope="Formula"

        elif line.startswith("\\begin{enumerate"):
            dct["Enum"].append(lineIndex)
            scope = ""
            current_scope="Enum"

        elif line.startswith("\\paragraph{"):
            dct["Paragraph"].append(lineIndex)
            scope = ""
            current_scope="Paragraph"

        elif line.startswith("\\caption{"):
            if scope=="Figure":
                dct["CaptionFigure"].append(lineIndex)
            elif scope=="Table":
                dct["CaptionTable"].append(lineIndex)
            scope = ""
            current_scope="Caption"

        else:
            if line!="":
                if current_scope=="":
                    dct["Par"].append(lineIndex)
                    current_scope="Par"

        lineIndex+=1

    for k in dct:
        print(f"{k}: {dct[k]}")

    return dct

if __name__=="__main__":

    run("C:\\Users\\adito\\PycharmProjects\\Overleaf_project\\pdf-tests\\61508_1.tex")