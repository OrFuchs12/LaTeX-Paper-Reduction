import re

commands_dict_with_corresponding_text = {}
figure_ref_id_and_caption_dict = {}
table_ref_id_and_caption_dict = {}
section_ref_id_and_num = {}
definition_ref_id_and_num = {}
all_refs_ids = {}
article_id_to_author_year = {}
#special_char_dict = {"alpha":"α","beta":"β","gamma":"γ","Gamma":"Γ","delta":"δ","Delta":"Δ","epsilon":"ε","varepsilon":"ε","zeta":"ζ","eta":"η","theta":"θ","vartheta":"θ","Theta":"Θ","iota":"ι","kappa":"κ","lambda":"λ","Lambda":"Λ","mu ":"μ","nu ":"ν","xi":"ξ","Xi":"Ξ","pi":"π","Pi":"Π","rho":"ρ","varrho":"ρ","sigma":"σ","tau":"τ","Sigma":"Σ","upsilon":"υ","Upsilon":"Υ","phi":"φ","varphi":"φ","Phi":"Φ","chi":"χ","psi":"ψ","Psi":"Ψ","omega":"ω","Omega":"Ω","leftarrow":"","rightarrow":"","leftrightarrow":"","uparrow":"","Uparrow":"","leftrightarrow":"","mapsto":"","nearrow":"","swarrow":"","leftharpoonup":"","leftharpoondown":"","Leftarrow":"","Rightarrow":"","rightleftharpoons":"","downarrow":"","Downarrow":"","Updownarrow":"","longmapsto":"","searrow":"","nwarrow":"","rightharpoonup":"","rightharpoondown":"","infty ":"","Re ":"","nabla ":"","partial ":"","emptyset ":"","wp":"","neg ":"","square":"","blacksquare":"","forall ":"","Im":"","exists ":"","nexists ":"","varnothing":"","complement":"","cdots":"","surd":"","triangle":"","times ":"","div ":"","cup ":"","leq ":"","in ":"","notin ":"","simeq ":"","wedge":"","oplus ":"","Box ":"","equiv ":"","cdot ":"","cap ":"","neq ":"","geq ":"","perp ":"","subset ":"","approx ":"","vee ":"","otimes ":"","boxtimes ":"","cong ":"","langle ":"","rangle ":""} #NEED TO ADD AT THE END
#PART 1
def remove_unnecessary_stuff(doc): #working insane
    new_doc = []

    begin_document_found = False
    found_table = False
    found_figure = False
    found_subfigure = False
    found_caption = False #for subfigures to see if we need to write them out when called

    caption = ""
    fig_label = ""

    figure_num = 0
    subfigure_num = 0
    table_num = 0

    section_num = 0
    subsection_num = 0
    subsubsection_num = 0

    definition_num = 0


    iffalse_found = False
    for line in doc:
        num_of_curly_brackets = 0
        inside_curly_brackets = False

        if not begin_document_found:
            if line.startswith("\\newcommand{"): #find the commands and replace them
                command_pos = 0
                key = ""
                value = ""
                for charindex in range(len(line)):
                    if line[charindex] == "{":
                        command_pos +=1
                        continue
                    if line[charindex] == "}":
                        continue
                    if command_pos == 1:
                        key += line[charindex]
                    if command_pos == 3:
                        if(line[charindex] != '\n'):
                            value += line[charindex]
                commands_dict_with_corresponding_text[key] = value
            if line.startswith("\\iffalse"):
                iffalse_found = True
            if line.startswith("\\fi"):
                iffalse_found = False
            if line.startswith("\\title{"):
                if(iffalse_found == False):
                    new_doc.append(line)
            if line.startswith("\\begin{document}"):
                begin_document_found = True
            continue

        new_line = ""
        if line.find("%") != -1 and line.find("%") < line.find("\n"): #if we have a comment in the line
            for charindex in range(len(line)):
                if line[charindex] == "%" and line[charindex-1] == "\\":
                    new_line += line[charindex] #if we find an actual % sign (presentage) then we will continue to look for the comment (%)
                    continue
                if line[charindex] == "%":
                    break

                new_line += line[charindex]
        else:
            new_line = line

        # to find the labels for each definition, we will assume that a label for a definition will come in the same declaration line of the definition
        if new_line.startswith("\\begin{definition}"):
            definition_num += 1
            if new_line.find("\\label{") != -1:
                start_index = new_line.find("\\label{")
                for charindex in range(start_index,len(new_line)):
                    if new_line[charindex] == "}":
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            inside_curly_brackets = False
                            break
                    if inside_curly_brackets == True:
                        caption += new_line[charindex]
                    if new_line[charindex] == "{":
                        num_of_curly_brackets += 1
                        inside_curly_brackets = True
                        continue
                definition_ref_id_and_num[caption] = (definition_num,'')
                all_refs_ids[caption] = (definition_num,'')

            new_doc.append(new_line)
            caption = ""
            continue



        #to find the labels for each section, we will assume that a label for a section will come in the same declaration line of the section
        if new_line.startswith("\\section{"):
            section_num += 1
            subsection_num = 0
            subsubsection_num = 0
            if new_line.find("\\label{") != -1:
                start_index = new_line.find("\\label{")
                for charindex in range(start_index,len(new_line)):
                    if new_line[charindex] == "}":
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            inside_curly_brackets = False
                            break
                    if inside_curly_brackets == True:
                        caption += new_line[charindex]
                    if new_line[charindex] == "{":
                        num_of_curly_brackets += 1
                        inside_curly_brackets = True
                        continue
                section_ref_id_and_num[caption] = (section_num,'')
                all_refs_ids[caption] = (section_num,'')

            new_doc.append(new_line)
            caption = ""
            continue

        if new_line.startswith("\\subsection{"):
            subsection_num += 1
            subsubsection_num = 0
            if new_line.find("\\label{") != -1:
                start_index = new_line.find("\\label{")
                for charindex in range(start_index, len(new_line)):
                    if new_line[charindex] == "}":
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            inside_curly_brackets = False
                            break
                    if inside_curly_brackets == True:
                        caption += new_line[charindex]
                    if new_line[charindex] == "{":
                        num_of_curly_brackets += 1
                        inside_curly_brackets = True
                        continue
                section_ref_id_and_num[caption] = (str(section_num) + "." + str(subsection_num), '')
                all_refs_ids[caption] = (str(section_num) + "." + str(subsection_num), '')

            new_doc.append(new_line)
            caption = ""
            continue

        if new_line.startswith("\\subsubsection{"):
            subsubsection_num += 1
            if new_line.find("\\label{") != -1:
                start_index = new_line.find("\\label{")
                for charindex in range(start_index, len(new_line)):
                    if new_line[charindex] == "}":
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            inside_curly_brackets = False
                            break
                    if inside_curly_brackets == True:
                        caption += new_line[charindex]
                    if new_line[charindex] == "{":
                        num_of_curly_brackets += 1
                        inside_curly_brackets = True
                        continue
                section_ref_id_and_num[caption] = (str(section_num) + "." + str(subsection_num) + "." + str(subsubsection_num), '')
                all_refs_ids[caption] = (str(section_num) + "." + str(subsection_num) + "." + str(subsubsection_num), '')

            new_doc.append(new_line)
            caption = ""
            continue

        if new_line.startswith("\\begin{table}"): #we will not find comments on lines with \\begin{figure} should be easy to fix
            found_table = True
            table_num += 1
            new_doc.append(new_line)
            continue
        if found_table == True:
            if (new_line.startswith("\\caption")):
                for charindex in range(len(new_line)):
                    if new_line[charindex] == "}":
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            inside_curly_brackets = False
                            break
                    if inside_curly_brackets == True:
                        caption += new_line[charindex]
                    if new_line[charindex] == "{":
                        num_of_curly_brackets += 1
                        inside_curly_brackets = True
                        continue

            if (new_line.startswith("\\label")):
                for charindex in range(len(new_line)):
                    if new_line[charindex] == "}":
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            inside_curly_brackets = False
                            break
                    if inside_curly_brackets == True:
                        fig_label += new_line[charindex]
                    if new_line[charindex] == "{":
                        num_of_curly_brackets += 1
                        inside_curly_brackets = True
                        continue
            if (new_line.startswith("\\end{table}")):
                found_table = False
                table_ref_id_and_caption_dict[fig_label] = (table_num, caption)
                all_refs_ids[fig_label] = (table_num, caption)
                caption = ""
                fig_label = ""

        if new_line.startswith("\\begin{figure}"):
            found_figure = True
            figure_num += 1
            subfigure_num = 0
            new_doc.append(new_line)
            continue
        if found_figure == True:
            if found_subfigure == True:
                if (new_line.strip().startswith("\\caption")): #removing leading spaces
                    found_caption = True
                    for charindex in range(len(new_line)):
                        if new_line[charindex] == "}":
                            num_of_curly_brackets -= 1
                            if (num_of_curly_brackets == 0):
                                inside_curly_brackets = False
                                break
                        if inside_curly_brackets == True:
                            caption += new_line[charindex]
                        if new_line[charindex] == "{":
                            num_of_curly_brackets += 1
                            inside_curly_brackets = True
                            continue

                if (new_line.strip().startswith("\\label")):
                    for charindex in range(len(new_line)):
                        if new_line[charindex] == "}":
                            num_of_curly_brackets -= 1
                            if (num_of_curly_brackets == 0):
                                inside_curly_brackets = False
                                break
                        if inside_curly_brackets == True:
                            fig_label += new_line[charindex]
                        if new_line[charindex] == "{":
                            num_of_curly_brackets += 1
                            inside_curly_brackets = True
                            continue

                if (new_line.strip().startswith("\\end{subfigure}")):
                    found_subfigure = False
                    figure_ref_id_and_caption_dict[fig_label] = (str(figure_num) + chr(ord('`')+subfigure_num), caption,found_caption)
                    all_refs_ids[fig_label] = (str(figure_num) + chr(ord('`')+subfigure_num), caption,found_caption)
                    found_caption = False
                    caption = ""
                    fig_label = ""
            else:
                if(new_line.startswith("\\begin{subfigure}")):
                    found_subfigure = True
                    subfigure_num += 1
                    new_doc.append(new_line)
                    continue
                if(new_line.startswith("\\caption")):
                    for charindex in range(len(new_line)):
                        if new_line[charindex] == "}":
                            num_of_curly_brackets -= 1
                            if(num_of_curly_brackets == 0):
                                inside_curly_brackets = False
                                break
                        if inside_curly_brackets == True:
                            caption += new_line[charindex]
                        if new_line[charindex] == "{":
                            num_of_curly_brackets +=1
                            inside_curly_brackets = True
                            continue

                if(new_line.startswith("\\label")):
                    for charindex in range(len(new_line)):
                        if new_line[charindex] == "}":
                            num_of_curly_brackets -= 1
                            if(num_of_curly_brackets == 0):
                                inside_curly_brackets = False
                                break
                        if inside_curly_brackets == True:
                            fig_label += new_line[charindex]
                        if new_line[charindex] == "{":
                            num_of_curly_brackets +=1
                            inside_curly_brackets = True
                            continue

                if(new_line.startswith("\\end{figure}")):
                    found_figure = False
                    figure_ref_id_and_caption_dict[fig_label] = (figure_num,caption)
                    all_refs_ids[fig_label] = (figure_num,caption)
                    caption = ""
                    fig_label = ""

        new_doc.append(new_line)

    return new_doc

#PART 2

def bib_process(document_path):
    with open(document_path, encoding='UTF-8') as file:
        # doc = file.read()
        doc = [line for line in file]

    return doc

def getting_article_id_to_author_dict(bib_file_array):
    article_id = ""
    article_author = ""
    article_year = ""
    for line in bib_file_array:
        if (line.startswith("@")):
            article_id = ""
            start_saving = False
            in_article = True
            for char in line:
                if (char == ","):
                    start_saving = False
                    break
                if (start_saving):
                    article_id += char
                if (char == "{"):
                    start_saving = True
            continue
        if (in_article):
            num_of_curly_brackets = 0
            inside_curly_brackets = False
            if (line.lstrip().startswith("author")):
                start_saving = False
                for char in line:
                    if (char == "}"):
                        num_of_curly_brackets -= 1
                        if (num_of_curly_brackets == 0):
                            start_saving = False
                            break
                    if (start_saving):
                        article_author += char
                    if (char == "{"):
                        num_of_curly_brackets += 1
                        start_saving = True
                continue
            if (line.lstrip().startswith("year")):
                start_saving = False
                for char in line:
                    if (char == "}"):
                        start_saving = False
                        break
                    if (start_saving):
                        article_year += char
                    if (char == "{"):
                        start_saving = True
                continue
            if (line.startswith("}")):
                in_article = False

                # lets make article author more suited for placement: (make it like latex syntax makes it in the pdf
                letter_with_curly_brackets = re.findall(r'{.*?\}?\}', article_author)
                letters_to_switch = []
                for i in letter_with_curly_brackets:
                    line = re.sub("[^A-Za-z]", "", i.strip())
                    if (len(line) > 1):
                        letter = line[1]
                    else:
                        letter = line[0]
                    letters_to_switch.append(letter)

                for i in range(len(letter_with_curly_brackets)):
                    article_author = article_author.replace(letter_with_curly_brackets[i], letters_to_switch[i])

                # after cleaning we will now want to match the authors to the way authors are presented in the pdf file:
                # RULES:
                # 1. if there is more than 3  authors in an article then it will type the first author and then "et al."
                # 2. if there is less or equal to 3 authors in an article then it will type the authors last name in order and the last will be with an "and" before the last name
                # 3. if there is more than 1 author in an \cite tag then we will chain the authors based on the rules above.
                # so now we will want to make the authors match the first and second rule:
                author_string_new = ""
                x = article_author.split("and")
                if (len(x) > 3):
                    author_string_new = x[0].split(",")[0] + " et al."
                else:
                    if (len(x) == 3):
                        for i in range(len(x)):
                            if (i == 2):
                                author_string_new += x[i].split(",")[0]
                            elif (i == 1):
                                author_string_new += x[i].split(",")[0] + " and"
                            else:
                                author_string_new += x[i].split(",")[0] + ","
                    if (len(x) == 2):
                        for i in range(len(x)):
                            if (i == 0):
                                author_string_new += x[i].split(",")[0] + " and"
                            else:
                                author_string_new += x[i].split(",")[0]
                    if (len(x) == 1):
                        author_string_new += x[0].split(",")[0]

                article_id_to_author_year[article_id] = (author_string_new, article_year)
                article_id = ""
                article_author = ""
                article_year = ""




def remove_stuff_latex(latex_doc):
    new_and_improved_latex_doc = []
    for line in latex_doc:
        new_string = line
        if('\\prob' in new_string or '\\alg' in new_string):
            temp_1 = new_string.replace("\prob\\", commands_dict_with_corresponding_text['\prob'])
            temp_2 = temp_1.replace("\prob", commands_dict_with_corresponding_text['\prob'])
            temp_3 = temp_2.replace("\\alg\\",commands_dict_with_corresponding_text['\\alg'])
            temp_4 = temp_3.replace("\\alg",commands_dict_with_corresponding_text['\\alg'])
            new_string = temp_4
        if('\\cite' in new_string or '\\citeauthor' in new_string or '\\citeyear' in new_string or '\\citeyearpar' in new_string):
            #new_string is the string
            if('\\cite' in new_string):
                res = re.findall(r'\\cite\{.*?\}', new_string)
                strings_to_replace = []
                for i in res:
                    if ('\\cite{' in i):
                        string_to_print = ""
                        x = i.split("\\cite{")[1]
                        y = x[0:len(x) - 1]
                        d = y.split(",")
                        for i in range(len(d)):
                            if (d[i][0] == " "):
                                d[i] = d[i][1:len(d[i])]
                            if (i == 0 and i == len(d) - 1):
                                string_to_print += "(" + article_id_to_author_year[d[i]][0] + " " + article_id_to_author_year[d[i]][1] + ")"
                                break
                            if (i == len(d) - 1):
                                string_to_print += " " + article_id_to_author_year[d[i]][0] + " " + article_id_to_author_year[d[i]][1] + ")"
                            elif (i == 0):
                                string_to_print += "(" + article_id_to_author_year[d[i]][0] + " " + article_id_to_author_year[d[i]][1] + ";"
                            else:
                                string_to_print += " " + article_id_to_author_year[d[i]][0] + " " + article_id_to_author_year[d[i]][1] + ";"

                        strings_to_replace.append(string_to_print)

                for i in range(len(strings_to_replace)):
                    new_string = new_string.replace(res[i], strings_to_replace[i])

            if ('\\citep' in new_string):
                res = re.findall(r'\\citep\{.*?\}', new_string)
                strings_to_replace = []
                for i in res:
                    if ('\\citep{' in i):
                        string_to_print = ""
                        x = i.split("\\citep{")[1]
                        y = x[0:len(x) - 1]
                        d = y.split(",")
                        for i in range(len(d)):
                            if (d[i][0] == " "):
                                d[i] = d[i][1:len(d[i])]
                            if (i == 0 and i == len(d) - 1):
                                string_to_print += "(" + article_id_to_author_year[d[i]][0] + " " + \
                                                   article_id_to_author_year[d[i]][1] + ")"
                                break
                            if (i == len(d) - 1):
                                string_to_print += " " + article_id_to_author_year[d[i]][0] + " " + \
                                                   article_id_to_author_year[d[i]][1] + ")"
                            elif (i == 0):
                                string_to_print += "(" + article_id_to_author_year[d[i]][0] + " " + \
                                                   article_id_to_author_year[d[i]][1] + ";"
                            else:
                                string_to_print += " " + article_id_to_author_year[d[i]][0] + " " + \
                                                   article_id_to_author_year[d[i]][1] + ";"

                        strings_to_replace.append(string_to_print)

                for i in range(len(strings_to_replace)):
                    new_string = new_string.replace(res[i], strings_to_replace[i])

            if('\\citeauthor' in new_string):
                res = re.findall(r'\\citeauthor\{.*?\}', new_string)
                strings_to_replace = []
                for i in res:
                    if ('\\citeauthor{' in i):
                        string_to_print = ""
                        x = i.split("\\citeauthor{")[1]
                        y = x[0:len(x) - 1] # all authors combined separted by ','
                        d = y.split(",") # authors list
                        for i in range(len(d)):
                            if (d[i][0] == " "):
                                d[i] = d[i][1:len(d[i])]
                            if (i == 0 and i == len(d) - 1):
                                string_to_print += article_id_to_author_year[d[i]][0]
                                break
                            if (i == len(d) - 1):
                                string_to_print += article_id_to_author_year[d[i]][0]
                            elif (i == 0):
                                string_to_print += article_id_to_author_year[d[i]][0] + "; "
                            else:
                                string_to_print += article_id_to_author_year[d[i]][0] + "; "

                        strings_to_replace.append(string_to_print)

                for i in range(len(strings_to_replace)):
                    new_string = new_string.replace(res[i], strings_to_replace[i])


            if('\\citeyear' in new_string):
                res = re.findall(r'\\citeyear\{.*?\}', new_string)
                strings_to_replace = []
                for i in res:
                    if ('\\citeyear{' in i):
                        string_to_print = ""
                        x = i.split("\\citeyear{")[1]
                        y = x[0:len(x) - 1]
                        d = y.split(",")
                        for i in range(len(d)):
                            if (d[i][0] == " "):
                                d[i] = d[i][1:len(d[i])]
                            if (i == 0 and i == len(d) - 1):
                                string_to_print += article_id_to_author_year[d[i]][1]
                                break
                            if (i == len(d) - 1):
                                string_to_print += article_id_to_author_year[d[i]][1]
                            elif (i == 0):
                                string_to_print += article_id_to_author_year[d[i]][1] + "; "
                            else:
                                string_to_print += article_id_to_author_year[d[i]][1] + "; "

                        strings_to_replace.append(string_to_print)

                for i in range(len(strings_to_replace)):
                    new_string = new_string.replace(res[i], strings_to_replace[i])

            if('\\citeyearpar' in new_string):
                res = re.findall(r'\\citeyearpar\{.*?\}', new_string)
                strings_to_replace = []
                for i in res:
                    if ('\\citeyearpar{' in i):
                        string_to_print = ""
                        x = i.split("\\citeyearpar{")[1]
                        y = x[0:len(x) - 1]
                        d = y.split(",")
                        for i in range(len(d)):
                            if (d[i][0] == " "):
                                d[i] = d[i][1:len(d[i])]
                            if (i == 0 and i == len(d) - 1):
                                string_to_print += "(" + article_id_to_author_year[d[i]][1] + ")"
                                break
                            if (i == len(d) - 1):
                                string_to_print += article_id_to_author_year[d[i]][1] + ")"
                            elif (i == 0):
                                string_to_print += "(" + article_id_to_author_year[d[i]][1] + "; "
                            else:
                                string_to_print += article_id_to_author_year[d[i]][1] + "; "

                        strings_to_replace.append(string_to_print)

                for i in range(len(strings_to_replace)):
                    new_string = new_string.replace(res[i], strings_to_replace[i])
        if ('\\ref{' in new_string):
            res = re.findall(r'\\ref\{.*?\}', new_string)
            strings_to_replace = []
            for i in res:
                if ('\\ref{' in i):
                    string_to_print = ""
                    x = i.split("\\ref{")[1]
                    y = x[0:len(x) - 1]
                    strings_to_replace.append(str(all_refs_ids[y][0]))

            for i in range(len(strings_to_replace)):
                new_string = new_string.replace(res[i], strings_to_replace[i])

        if ('{\\bf' in new_string):
            res = re.findall(r'\{\\bf.*?\}', new_string)
            strings_to_replace = []
            for i in res:
                if ('{\\bf ' in i):
                    string_to_print = ""
                    x = i.split('{\\bf ')[1]
                    y = x[0:len(x) - 1]
                    strings_to_replace.append(y)

            for i in range(len(strings_to_replace)):
                new_string = new_string.replace(res[i], strings_to_replace[i])

            res2 = re.findall(r'\{\\bf.*?', new_string)
            strings_to_replace = []
            for i in res2:
                strings_to_replace.append('')

            for i in range(len(strings_to_replace)):
                new_string = new_string.replace(res2[i], strings_to_replace[i])

        if('\\noindent' in new_string):
            new_string = new_string.replace('\\noindent','')

        if('\\label{' in new_string):
            res = re.findall(r'\\label{.*?\}', new_string)
            for i in res:
                new_string = new_string.replace(i,'')
                
        # for key, value in special_char_dict.items(): NEED TO ADD AT THE END
        #     new_res_3 = re.findall(r'\\%s' % (key), new_string)
        #     for i in new_res_3:
        #         new_string = new_string.replace(i, '')

        new_and_improved_latex_doc.append(new_string)

    return new_and_improved_latex_doc

def read_file(document_path,bib_path):
    with open(document_path, encoding='UTF-8') as file:
        # doc = file.read()
        doc = [line for line in file]


    new_doc = remove_unnecessary_stuff(doc)

    bib_file_array = bib_process(bib_path)

    getting_article_id_to_author_dict(bib_file_array)

    new_new_doc = remove_stuff_latex(new_doc)

    return new_new_doc
