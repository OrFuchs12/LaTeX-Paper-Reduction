#!/bin/bash

# Usage: export pictures.pdf from powerpoint
# (function) export_pdf_image.sh 2 outfile  => emits cropped pdf image from the slide 2

PICTURES_PDF="pictures-capseg.pdf"

if [ ! -f $PICTURES_PDF ]; then
	exit 1;
fi

export_pdf_image() {
	page=$1
	outfile=$2

	if [ -z "$page" ]; then
		echo 'specify page';
		exit 1;
	fi
	if [ -z "$outfile" ]; then
		echo 'specify outfile';
		exit 1;
	fi

	pdfseparate -f $page -l $page $PICTURES_PDF pictures.page${page}.tmp.pdf
	pdfcrop -margin 10 pictures.page${page}.tmp.pdf ${outfile}
	rm pictures.page${page}.tmp.pdf

	echo -e 'Done!!!\n\n'
}

if [ -z "$1" ]; then echo "No page argument supplied"; exit 1; fi
if [ -z "$2" ]; then echo "No output argument supplied"; exit 1; fi

export_pdf_image $1 $2
