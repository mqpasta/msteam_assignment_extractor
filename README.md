# MS Team Assignment Extractor
Extract students submitted assignments from MS Team download files

You have to download student submissions on your computer in order to use this utility. Refer the following URL to learn how to do it. 
https://techcommunity.microsoft.com/t5/microsoft-teams/download-all-files-from-my-all-teams-in-microsoft-teams/m-p/172876

# Usage

## -i input path
point the directory where all folders of student-submitted work present

## -o output path
point the directory where you want to copy all extracted files

## -a assignment tile
title of the assignment (don't forget to provie qutations in case of spaces i.e. "Assignment 1")

# Example
asg_extractor.py  -i e:\test\AllFiles -a "Assignment 1" -o files
