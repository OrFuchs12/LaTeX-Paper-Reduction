import os
import subprocess
import csv
import pdfplumber
from collections import defaultdict
from addRows import *

#assuming the papers already seperated with bibliography on new page
#works only on one paper at a time
def analyze_pdf(pdf_file_path):
    # Analyze the compiled PDF document and extract statistical data
    pdf_data = defaultdict(int)
    
    with pdfplumber.open(pdf_file_path) as pdf:
        pdf_data['num_pages'] = len(pdf.pages)
        
        page_number = find_page_number_before_bibliography(pdf_file_path, "References")
        
        lines = count_lines_in_page(pdf_file_path, page_number)
        # last_page = pdf.pages[-1]
        # last_page_text = last_page.extract_text()
        pdf_data['num_lines_last_page'] = lines
        
        for page in pdf.pages:
            pdf_data['num_pictures'] += len(page.images)
            
            # for char in page.chars:
            #     if char['fontname'] == 'ZapfDingbats':  # Assuming formulas use this font
            #         pdf_data['num_formulas'] += 1
            #         pdf_data['num_algorithms'] += 1
    
    return pdf_data

def analyze_latex(tex_file_path):
    # Analyze the LaTeX document and extract section, graph, and table counts
    latex_data = defaultdict(int)
    
    with open(tex_file_path, 'r') as tex_file:
        content = tex_file.read()
        latex_data['num_sections'] = content.count('\\section{')
        latex_data['num_graphs'] = content.count('\\begin{figure}')
        latex_data['num_tables'] = content.count('\\begin{table}')
        latex_data['num_algorithms'] = content.count('\\begin{algorithm}')
        latex_data['num_equations'] = content.count('\\begin{equation}')
    
    return latex_data

def create_summary_csv(data, csv_file_path):
    # Create a CSV file with the summarized statistical data
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Metric', 'Value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for metric, value in data.items():
            writer.writerow({'Metric': metric, 'Value': value})

def latex_pdf_statistics(tex_file_path, pdf_file_path, summary_csv_file_path):
   
    analyze_result_pdf = analyze_pdf(pdf_file_path)
    analyze_result_latex = analyze_latex(tex_file_path)
    
    combined_data = defaultdict(int)
    for data_dict in [analyze_result_pdf, analyze_result_latex]:
        for key, value in data_dict.items():
            combined_data[key] += value
            
    create_summary_csv(combined_data, summary_csv_file_path)
    
if __name__ == "__main__":
    tex_file_path = "new_papers_creation/aaai_docs/main.tex"
    pdf_file_path = "new_papers_creation/aaai_docs/main.pdf"
    summary_csv_file_path = "new_papers_creation/summary.csv"
    
    latex_pdf_statistics(tex_file_path, pdf_file_path, summary_csv_file_path)