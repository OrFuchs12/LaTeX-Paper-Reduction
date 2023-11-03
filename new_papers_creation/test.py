import os
import subprocess
import pdflatex as pdflatex


latex_file = 'new_papers_creation\AAAI 2016\prize.tex'
latex_Dir = os.path.dirname(latex_file)
print(latex_Dir)
latex_Dir = f"{latex_Dir}"
# os.chdir(latex_Dir)
print(os.getcwd())
# Run LaTeX compiler to generate PDF.
command = ['pdflatex.exe', 'prize_changed.tex']

# Run the LaTeX compiler to generate the PDF
subprocess.run(['pdflatex.exe', 'prize_changed.tex'], cwd=latex_Dir)