#!/usr/bin/env bash
set -e

ARG_1=$1
ARG_2=$2

#mkdir output_flatex
#pdflatex -output-directory=output_flatex -output-format=pdf ${LATEX_FILE}

#mkdir output_rubber
#cd output_rubber
#rubber --pdf ../${LATEX_FILE}
#cd -

if [ "$ARG_1" = "add" ]
then
  ./add_source_to_latex.sh Thesis_paper_to_latex.txt main_template.tex main.tex
fi

if [ "$ARG_2" = "images" ]
then
  convert -density 600 -background none examplePta.eps      examplePta.png
  #convert -density 600 -background none ptaMaintain17.svg   ptaMaintain17.png
  #convert -density 600 -background none ptaAchieve17.svg    ptaAchieve17.png
fi

if [ -f Paper.pdf ]; then
    rm Paper.pdf
fi
if [ -f Paper.out ]; then
    rm Paper.out
fi


wait ${!}
xelatex main.tex
wait ${!}
#bibtex main
wait ${!}
bibtex main
wait ${!}
evince main.pdf &>/dev/null
