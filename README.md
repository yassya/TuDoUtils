TuDoUtils
=========

Helper class for drawing ROOT objects in a nice way

For an example look in the tudoUtils_example.py 


Caution: This does *NOT* work with python 2, due to some magic with the print()-Function
If you want to use this with python 2, you can remove lines 735ff:

def printAsLatex(theList):
    
    for element in theList:
        print(element, end=printLatexTable(element, theList))


