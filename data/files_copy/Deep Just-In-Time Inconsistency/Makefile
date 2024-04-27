formattedS := formatted
TEXS := $(wildcard *.tex)
TABLES := $(wildcard tables/**/*.tex)
FIGS := $(wildcard figs/*.tex) $(wildcard images/*.png) $(wildcard images/*.PNG) $(wildcard code/*)
PLOTS := $(wildcard figs/*.eps)
BIBS := $(wildcard *.bib)

LATEX = pdflatex -interaction=nonstopmode
BIBTEX = bibtex

.PHONY: all
all: $(formattedS:=.pdf)

.PHONY: display
display: $(formattedS:=.pdf)
	evince $(formattedS:=.pdf)

$(formattedS:=.pdf) : %.pdf : ${TEXS} ${TABLES} ${BIBS} ${FIGS} ${PLOTS}
	-rm -f $*.aux
	-rm -f $*.bbl
	-$(LATEX) $*
	-$(BIBTEX) $*
	-$(LATEX) $*
	-$(LATEX) $*
# Check error
	@if [ -z "$$(grep -i "error" formatted.log | grep -v "errmessage" | grep -v "infwarerr" | grep -v "\(redefined the meaning of the math\|t cause unrecoverable errors\)" | grep -v "error-analysis")"]; then \
             echo "This latex error can be safely ignored"; \
         else \
             echo "****************************************"; \
             echo "There might be other latex errors:"; \
             echo "****************************************"; \
             echo "$$(grep -i "error" formatted.log | grep -v "errmessage" | grep -v "infwarerr" | grep -v "\(redefined the meaning of the math\|t cause unrecoverable errors\)" | grep -v "error-analysis")"; \
             echo "****************************************"; \
             echo "Check formatted.log for details!"; \
             exit 1; \
         fi
#	-$(LATEX) $*
	@echo '****************************************************************'
# vvvvvv For `latex` ONLY. Comment out for `pdflatex`
#	@dvips -j0 -t letter -o $(NAME).ps $(NAME).dvi
#	@ps2pdf -dPDFSETTINGS=/prepress $(NAME).ps $(NAME).pdf
# ^^^^^^^^^^^^^^^^^^^^^^^^
	@echo '******** Did you spell-check the paper? ********'

.PHONY: clean
clean:
	ls $(formattedS:=.*) | grep -v ".\(tex\|bib\|sty\)" | xargs rm -f
	rm -f *.bak *~
#	find -name "*.eps" | xargs rm -f
