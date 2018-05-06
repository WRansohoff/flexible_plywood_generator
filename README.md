# Overview

This is a simple Python script to generate .SVG files for cutting out with a laser cutter. Using 3mm-thick plywood, these patterns produce flexible sheets which can be bent into rounded shapes before being fixed to other surfaces.

Two methods are available; rectangular cuts, or helical cuts. The rectangular cuts are the ones that were explained to me by a friend, but after talking about other possibilities it seemed worth trying a helical pattern to hopefully use less laser time. It seems to produce very flexible results, but I would like to make some improvements like adding some solid connections every few helices.

I'll try to add some images soon, but the script is easy to use; it accepts 3 arguments for the width and height in mm, and the output filename. For example, to generate a flexible sheet 50mm wide and 100mm tall in a file called "test.svg", you can use:

    python lhinge_rects.py 50 100 test_rects.svg

Or:

    python lhinge_helices.py 50 100 test_helices.svg

I'd like to add more features and options, but these patterns seem to work as a starting point.

The 'test\_rects.svg' file is an example 54x50mm tile generated with 2.25mm-thick "gap" columns and 1.75mm-thick "solid" columns. Those values can be adjusted in variables within the script, but are not currently exposed as command-line options. And the 'test\_helices.svg' file is an example 54x50mm tile generated with helices 3.5mm at their widest and spaced an extra 1.5mm apart.
