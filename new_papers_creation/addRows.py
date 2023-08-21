import pdfplumber
import subprocess
import os

def compile_latex_to_pdf(tex_file_path):
    try:
        # Get the directory path and base name of the input LaTeX file
        dir_path = os.path.dirname(tex_file_path)
        base_name = os.path.splitext(os.path.basename(tex_file_path))[0]

        # Create the output PDF file path
        pdf_file_path = os.path.join(dir_path, base_name + ".pdf")
        
        # Run pdflatex to compile the LaTeX file and generate the PDF
        subprocess.run(["pdflatex", "-output-directory=" + dir_path, tex_file_path])
        
        print("LaTeX to PDF conversion successful. PDF saved at:", pdf_file_path)
    except subprocess.CalledProcessError as e:
        print("Error during LaTeX to PDF conversion:", e)

# Replace this with the actual path to your .tex file
tex_file_path = "/Users/amitvitkovsky/Desktop/projects/LaTeX-Paper-Reduction/new_papers_creation/AAAI13-QDEC/QDEC-POMDP.8.tex"

compile_latex_to_pdf(tex_file_path)

