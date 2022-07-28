#!/bin/bash

# Cleanup old runs.
rm -f apireturns.txt apireturns2.txt
rm -f practicemodels/confusionmatrix.png
rm -f practicemodels/confusionmatrix2.png
rm -f models/confusionmatrix.png
rm -f ingestedfiles.txt

cp config-practice.json config.json

for script in ingestion training scoring deployment diagnostics reporting apicalls
    do
        python $script.py
    done

#
# Save certain files
#
mv apireturns.txt apireturns2.txt
cp practicemodels/confusionmatrix.png practicemodels/confusionmatrix2.png

cp config-prod.json config.json
python fullprocess.py
