
from pdfMiner_new import run
from pdf_extraction import pictures,tables


def order_page(path,page_num,tables_dict,pictures_dict,frompdf):

    pdf_p0=frompdf[page_num]
    tables_p0=tables_dict[page_num]
    pictures_p0 = pictures_dict[page_num]

    left_column= {}
    right_column = {}

    for line in pdf_p0:
        if line[1][0]<300: #left_column
            left_column[(line[1][1],line[1][3])]=line[0]
        else:
            right_column[(line[1][1],line[1][3])] = line[0]

    left_column_sorted_dict = sorted(left_column.items(), key=lambda x: x[0][0])
    right_column_sorted_dict = sorted(right_column.items(), key=lambda x: x[0][0])
    current_y_start = 0
    current_y_end = 0
    last_index=0
    new_left_column_sorted_dict = {}
    for k in left_column_sorted_dict:
        if abs(k[0][0] - current_y_start) < 2 and abs(k[0][1] - current_y_end) < 2:
            helper = new_left_column_sorted_dict[last_index]
            tple=list(last_index)
            tple[1]=max(k[0][1],tple[1])
            #helper[0]=tuple(tple)
            last_index=tuple(tple)
            txt=helper+k[1]
            new_left_column_sorted_dict[last_index]=txt
            current_y_end=k[0][1]
            current_y_start=k[0][0]
            #new_left_column_sorted_dict[-1] =
        else:
            new_left_column_sorted_dict[k[0]]=k[1]
            current_y_start = k[0][0]
            current_y_end = k[0][1]
            last_index=k[0]
    left_column=new_left_column_sorted_dict

    current_y_start = 0
    current_y_end = 0
    last_index = 0
    new_right_column_sorted_dict = {}
    for k in right_column_sorted_dict:
        if abs(k[0][0] - current_y_start) < 2 and abs(k[0][1] - current_y_end) < 2:
            helper = new_right_column_sorted_dict[last_index]
            tple = list(last_index)
            tple[1] = max(k[0][1], tple[1])
            # helper[0]=tuple(tple)
            last_index = tuple(tple)
            txt = helper + k[1]
            new_right_column_sorted_dict[last_index] = txt
            current_y_end = k[0][1]
            current_y_start = k[0][0]
        else:
            new_right_column_sorted_dict[k[0]] = k[1]
            current_y_start = k[0][0]
            current_y_end = k[0][1]
            last_index = k[0]
    right_column = new_right_column_sorted_dict
    for key_picture in pictures_p0:

        if key_picture["x0"]<300:
            if (key_picture["y0"],key_picture["y1"]) in left_column: #it is possible that two figures have the exact same height
                left_column[(key_picture["y0"],key_picture["y1"])]+="_FIGUREFIGURE"
            else:
                left_column[(key_picture["y0"],key_picture["y1"])]="FIGUREFIGURE"
        else:
            if (key_picture["y0"],key_picture["y1"]) in right_column: #it is possible that two figures have the exact same height
                right_column[(key_picture["y0"],key_picture["y1"])]+="_FIGUREFIGURE"
            else:
                right_column[(key_picture["y0"],key_picture["y1"])]="FIGUREFIGURE"

    for key_table in tables_p0:
        if len(tables_p0[key_table])!=0:
            for table in tables_p0[key_table]:
                if table[0]<300:
                    left_column[(table[1],table[3])] = "TABLETABLE"
                else:
                    right_column[(table[1],table[3])] = "TABLETABLE"

    left_column_sorted_dict=sorted(left_column.items(),key=lambda x:x[0][0])
    right_column_sorted_dict=sorted(right_column.items(),key=lambda x:x[0][0])

    return left_column_sorted_dict,right_column_sorted_dict

def order(path):
    pdf_total_order={}
    frompdf = run(path)

    tables_dict = tables(path)
    pictures_dict = pictures(path)

    for i in range(2):
        pdf_total_order[i]=order_page(path,i,tables_dict,pictures_dict,frompdf)

    return pdf_total_order

if __name__ == '__main__':
    tex_path = "../../pdf-tests/two_pages_with_specific_v2.tex"
    pdf_path = "../../pdf-tests/letters.pdf"

    total_pdf=order(pdf_path)

    for i in range(2):
        print(f"===PAGE_{i}===")

        left,right=total_pdf[i]
        print("--LEFT--")
        for k in left:
            print(f"{k}")
        print("--RIGHT--")
        for k in right:
            print(f"{k}")