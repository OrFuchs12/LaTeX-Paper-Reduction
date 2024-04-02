#!/bin/bash -
#===============================================================================
#
#          FILE: run.sh
#
#         USAGE: ./run.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dr. Fritz Mehner (fgm), mehner.fritz@fh-swf.de
#  ORGANIZATION: FH Südwestfalen, Iserlohn, Germany
#       CREATED: 09/09/2017 20:46
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
for lv in 0.1
do
    python DMF_TIST.py --featureK 15 --LambdaU 0.1 --LambdaV $lv --LambdaZ 0.01 --alpha 0.1 --neighborNum 4 
done
