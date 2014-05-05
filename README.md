TuDoUtils
=========

Helper clasess for drawing some ROOT objects in a nice way

For an example look in the examples_drawClass.py

The package is mainly split into the following different classes:

simplePlotHolder	-		For 'just' drawing some plots. Has 1D and 2D plot support
ratioPlotHolder		-		Draws a couple of objects together with a ratio at the bottom. Only supports 1D objects 
twoAxisPlotHolder	-		Allows a second Y axis on the right side. Each plot is assigned to either axis. Only supports 1D objects 
plotInPlotHolder	-		Allows the placement of a smaller subfigure inside the figure. Only supports 1D objects

All of these classes support the ROOT classes of TGraph, TGraphErrors, TH1D, TH1F, THStack and TF1. The 2D support is for TH2F and TH2D.
If you are wondering why THXI are not supported, its because you should not use integer histograms (*). Use TH2F instead.

Additionally they support two classes of this package, errorBarHist and errorBarStack. They allow the addition
of systematic uncertainties to a histogram.

There are additional examples for all these classes.



printAsLatexTable converts a python list to the body of a latex tabular.
Caution: printAsLatexTable does not work with python2, due to some magic with the print()-Function

For more information about ROOT visit http://root.cern.ch .




(*) The slightly longer answer is that ROOT not only stores the bin contents as an integer but also calculates properties like the mean 
as an integer in the THXI family. This might give wrong results. Just use THXF instead.