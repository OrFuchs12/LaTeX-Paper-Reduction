import os
import subprocess
import csv
import pdfplumber
from collections import defaultdict
import re
from addRows import add_clearpage_before_bibliography, find_page_number_before_bibliography, count_lines_in_page, compile_latex_to_pdf

def remove_comments(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        content = input_file.read()
        
        # Remove single-line comments that start with %
        content_without_comments = re.sub(r'%[^\n]*', '', content)
        
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content_without_comments)
            
            
#assuming the papers already seperated with bibliography on new page
#works only on one paper at a time
def analyze_pdf(pdf_file_path):
    # Analyze the compiled PDF document and extract statistical data
    pdf_data = defaultdict(int)
    
    with pdfplumber.open(pdf_file_path) as pdf:
        page_number = find_page_number_before_bibliography(pdf_file_path, "References")
        pdf_data['num_pages'] = page_number+1
        lines = count_lines_in_page(pdf_file_path, page_number)
        pdf_data['num_lines_last_page'] = lines
        
        # last_page = pdf.pages[-1]
        # last_page_text = last_page.extract_text()
        # pdf_data['num_lines_last_page']=  len(last_page_text.strip().split('\n'))
        
        for page in pdf.pages:
            pdf_data['num_pictures'] += len(page.images)
            
    
    
    return pdf_data

def analyze_latex(tex_file_path):
    # Analyze the LaTeX document and extract section, graph, and table counts
    latex_data = defaultdict(int)
    
    with open(tex_file_path, 'r', encoding='utf-8') as tex_file:
        content = tex_file.read()
        
        # Count the number of non-commented sections
        section_pattern = re.compile(r'\\section{')
        num_sections = len(section_pattern.findall(content))
        latex_data['num_sections'] = num_sections
        # latex_data['num_sections'] = content.count('\\section{')
       # Count the number of non-commented graphs
        graph_pattern = re.compile(r'\\includegraphics{')  # Adjust the pattern
        num_graphs = len(graph_pattern.findall(content))
        latex_data['num_graphs'] = num_graphs
        
        # Count the number of non-commented tables
        table_pattern = re.compile(r'\\begin{table}')  # Adjust the pattern
        num_tables = len(table_pattern.findall(content))
        latex_data['num_tables'] = num_tables
        
        # Count the number of non-commented algorithms
        algorithm_pattern = re.compile(r'\\begin{algorithm}')  # Adjust the pattern
        num_algorithms = len(algorithm_pattern.findall(content))
        latex_data['num_algorithms'] = num_algorithms
        
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
    remove_comments(tex_file_path,tex_file_path)
    analyze_result_pdf = analyze_pdf(pdf_file_path)
    analyze_result_latex = analyze_latex(tex_file_path)
    
    combined_data = defaultdict(int)
    for data_dict in [analyze_result_pdf, analyze_result_latex]:
        for key, value in data_dict.items():
            combined_data[key] += value
            
    create_summary_csv(combined_data, summary_csv_file_path)
    
if __name__ == "__main__":
    tex_file_path = "new_papers_creation/aaai_docs/main_changed.tex"
    add_clearpage_before_bibliography(tex_file_path)
    pdf_file_path = compile_latex_to_pdf(tex_file_path)
    # tex_file_path = "new_papers_creation/aaai_docs/main.tex"
    # pdf_file_path = "new_papers_creation/aaai_docs/main.pdf"
    summary_csv_file_path = "new_papers_creation/summary.csv"
    
    latex_pdf_statistics(tex_file_path, pdf_file_path, summary_csv_file_path)