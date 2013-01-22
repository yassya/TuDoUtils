'''
 <TuDoUtils --- A program for some nice plotting with ROOT.>
    Copyright (C) 2013  Christian Jung

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

def printAsLatex(theList):
    """
    Takes a list in will print it in a format which can be
    directly pasted into a latex tabular environment    
    """
    for element in theList:
        print(element, end=printLatexTable(element, theList))


def printLatexTable(theElement, theList):
    '''
    a small function which can be used in the python print function like this:
    
    x = ['This', 'is', 'stuff', 'to', 'print']
    for a in x:
        print(a, end=printLatexTable(a,x))
    
    this will print it in latex table format, i.e. "&" between the elements
    and an \\ at the end, in the example it would print:
    
    This    &    is    &    stuff    &    to    &    print\\
    
    '''
    if theElement is theList[-1]:
        return "\\\\\n" 
    else:
        return "\t&\t"
