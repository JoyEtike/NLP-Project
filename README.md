# NLP-Project
PERFORMANCE COMPARISON BETWEEN K-NN AND NAÏVE BAYES ALGORITHMS IN TEXT CLASSIFICATION

classifying school review text data into Positive Negative and Neutral 

Description of the code and data files

DataMinning.py to be ran first, it extracts review data from the URL specified on line 18
the extracted data is stored in RawData.csv file

Cleanup.py is next. it takes the RawData.csv file as an input for cleaning and stored the cleaned... 
...file in CleanData.csv

BOW.py (Bag of Words) uses CleanData.csv as an input for transformation and model

array.csv is the vectorised tranformed data. the text data are now represented with vectors

