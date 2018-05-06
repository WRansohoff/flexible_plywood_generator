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

# Use a 'double-helix' pattern like DNA to only need to cut
# one path per column. This should be faster for a laser
# to cut out than a whole lot of perpendicular lines.
max_helix_height = 40.0
sep_h = 2.0
gap_w = 3.5
col_w = 1.5
total_gap = gap_w + col_w
#total_gap = 3.5
#num_helices = int(math.ceil(float(height-max_helix_height/2) / (max_helix_height)))
#helix_h = (float(height) / float(num_helices + 1))
num_helices = int(math.ceil(float(height-sep_h) / (max_helix_height+0.5)))
num_helices = num_helices + 1
helix_h = (float(height-sep_h) / float(num_helices+0.5))

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
cur_x = total_gap / 2
done = False

while not done:
  # Draw a double-helix alternating from the top or bottom.
  if (extra_column):
    # Starting 'half-helix'.
    svg.write(("<path d=\"M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
              %(cur_x, 0.0, (cur_x-(gap_w/2)), 0.0,
               (cur_x+(gap_w/2)), (helix_h/2))))
    # Start the path from the top, and move down.
    hel_dir = True
    for i in range(0, num_helices):
      q_pt = cur_x - (gap_w/2)
      if hel_dir:
        q_pt = cur_x + (3*gap_w/2)
      svg.write(("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
                 %(cur_x+(gap_w/2), (i*(helix_h)+(helix_h/2)),
                  (q_pt), (i*helix_h)+helix_h, cur_x+(gap_w/2),
                  (i*(helix_h)+(3*helix_h/2)))))
      hel_dir = not hel_dir
    # Move back up to the top.
    for i in range(0, num_helices):
      q_pt = cur_x - (gap_w/2)
      if hel_dir:
        q_pt = cur_x + (3*gap_w/2)
      svg.write(("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
                 %(cur_x+(gap_w/2), ((num_helices-1-i)*(helix_h)+(helix_h/2)),
                  (q_pt), ((num_helices-1-i)*helix_h)+helix_h, cur_x+(gap_w/2),
                  ((num_helices-1-i)*(helix_h)+(3*helix_h/2)))))
      hel_dir = not hel_dir
    # Finishing 'half-helix'.
    svg.write(("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
              %(cur_x+(gap_w/2), (helix_h/2), (cur_x+(3*gap_w/2)), 0.0,
               (cur_x+gap_w), 0.0)))
    svg.write("\" />\n")
  else:
    # Starting 'half-helix'.
    svg.write(("<path d=\"M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
              %(cur_x, height, (cur_x-(gap_w/2)), height,
               (cur_x+(gap_w/2)), height-(helix_h/2))))
    # Start the path from the bottom, and move up.
    hel_dir = True
    for i in range(0, num_helices):
      q_pt = cur_x - (gap_w/2)
      if hel_dir:
        q_pt = cur_x + (3*gap_w/2)
      svg.write(("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
         %((cur_x+(gap_w/2)),
          (height-(i*(helix_h)+(helix_h/2))),
          (q_pt),
          (height-((i*helix_h)+helix_h)),
          (cur_x+(gap_w/2)),
          (height-(i*(helix_h)+(3*helix_h/2))))))
      hel_dir = not hel_dir
    # Then draw back down.
    for i in range(0, num_helices):
      q_pt = cur_x - (gap_w/2)
      if hel_dir:
        q_pt = cur_x + (3*gap_w/2)
      svg.write(("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
         %((cur_x+(gap_w/2)),
          height-((num_helices-1-i)*(helix_h)+(helix_h/2)),
          (q_pt),
          height-(((num_helices-1-i)*helix_h)+helix_h),
          (cur_x+(gap_w/2)),
          height-((num_helices-1-i)*(helix_h)+(3*helix_h/2)))))
      hel_dir = not hel_dir
    # Finishing 'half-helix'.
    svg.write(("M%.2f,%.2f Q%.2f,%.2f %.2f,%.2f "
              %(cur_x+(gap_w/2), height-(helix_h/2),
               (cur_x+(3*gap_w/2)), height,
               (cur_x+gap_w), height)))
    svg.write("\" />\n")

  extra_column = not extra_column
  cur_x += total_gap
  # Check if we're done.
  if (cur_x >= (width - total_gap)):
    done = True

# Close the 'group' and SVG tags.
svg.write("  </g>\n</svg>\n")
svg.close()
