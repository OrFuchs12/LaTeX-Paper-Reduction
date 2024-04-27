PAPER = main

export BIBINPUTS=.:../bib
#export BIBINPUTS=../bib

default:
	pdflatex --shell-escape $(PAPER).tex	
	bibtex --min-crossrefs=99 $(PAPER)
	pdflatex --shell-escape $(PAPER).tex	
	pdflatex --shell-escape $(PAPER).tex	



clean:
	rm -f *~ *.{aux,log,blg,bbl,synctex.gz,fdb_latexmk,fls,out} tmp.tex
