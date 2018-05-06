import sys
import math

# Check that the right number of arguments were passed in.
if len(sys.argv) != 4:
  print("Usage: 'python3 lhinge.py [width] [height] [output filename]\n(Units in the SVG output file are mm)")
  sys.exit(1)

# Record the desired values.
width  = int(sys.argv[1])
height = int(sys.argv[2])
filename    = sys.argv[3]

# Find the "Living Hinge" dimensions.
# Each edge is 2mm; add 2mm for the last 'column', too.
# Every other column will be solid; the non-solid ones
# will have 2mm 'rows' with alternating spacing.
# Every other non-solid row will have either N or N+1 'rows'.
# So, what is 'N'? We pick it so that the largest open
# vertical space is no more than 40mm in length.
# (Also subtract 4mm for the top/bottom 'row')
# So, (H-4)/N <= 42, which means solve N = (H-4)/42 and round up.
# (The "2mm" values can be editied with these variables):
sep_h = 2.0
gap_w = 2.25
col_w = 1.75
total_gap = col_w + gap_w
num_columns_l = int(math.ceil(float(height-sep_h) / (40.0+sep_h)))
num_columns_m = int(num_columns_l + 1)
col_h_l = (float(height) / float(num_columns_l)) - sep_h
col_h_m = (float(height) / float(num_columns_m)) - sep_h

# Now, just draw the appropriate shapes in an SVG file.
# First, open the output file.
svg = open(filename, 'w')
# Write the SVG file declaration, to span the full W/H.
svg.write(("<svg width=\"%dmm\" height=\"%dmm\" "
           "viewBox=\"0 0 %d %d\" "
           "xmlns=\"http://www.w3.org/2000/svg\">\n"
           %(width, height, width, height)))
# Draw a 'group' tag to style the following shapes.
svg.write(("  <g id=\"outlines\" fill=\"none\" stroke=\"black\" "
           "stroke-width=\"0.1\" stroke-linejoing=\"miter\">\n"))
# Draw a rectangle covering the whole width.
svg.write(("    <rect x=\"0\" y=\"0\" "
           "width=\"%d\" height=\"%d\" />\n"
           %(width, height)))
# Draw each column.
extra_column = True
cur_x = col_w
done = False
while not done:
  # Draw N or N+1 rectangles
  if (extra_column):
    for i in range(0, num_columns_l):
      svg.write(("    <rect x=\"%.2f\" y=\"%.2f\" "
                 "width=\"%.2f\" height=\"%.2f\" />\n"
                 %(cur_x, (i*(col_h_l+sep_h)),
                   gap_w, col_h_l)))
  else:
    for i in range(0, num_columns_m):
      svg.write(("    <rect x=\"%.2f\" y=\"%.2f\" "
                 "width=\"%.2f\" height=\"%.2f\" />\n"
                 %(cur_x, (sep_h + i*(col_h_m+sep_h)),
                   gap_w, col_h_m)))
  extra_column = not extra_column
  cur_x += total_gap
  # Check if we're done.
  if (cur_x >= (width - max(col_w, gap_w))):
    done = True
# Close the 'group' and SVG tags.
svg.write("  </g>\n</svg>\n")
svg.close()
