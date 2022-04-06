README.txt 	% How use our model to create a class time-tabling solution
% Modelling projet Group 2
% Chingyee Chow
% Luuk Hofmeijer
% Sem van den Bos
% Giuliano Cavallo Garavilla
% Jeanne Lemoine

% Libraries imported: 
pandas, numpy, random, defaultdict from collections, 
(Iterable, List, Set, Iterator) from typing

% Input and Output behaviour :
The Input has to be an Excel file consisting of two sheets :

1 -	All the students with their ID (1st column), credits required (2nd column) 
	and course list preferences (from the 3rd to the 10th column)

2 - All the courses with thier ID (1st column), minimum students limit (2nd column), 
	maximum students limit (3rd column), timeslot (4th column) and credits associated (5th column)

This input file is expected in the folder named 'data'. To run the algorithm, run the main.py.
When asked for the filename, the name of the excel file without the extension is expected, e.g.
type example for the file example.xls. The output will appear in the same data folder, as 
filename_output.xls.
This output file consists of two sheets:
1 -	Columns with all the course names and the assigned student ids below it.
2 -	Rows with the student ids and the assigned courses next to it.