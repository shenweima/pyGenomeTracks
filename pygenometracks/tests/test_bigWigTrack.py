# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.use('agg')
from matplotlib.testing.compare import compare_images
from tempfile import NamedTemporaryFile
import os.path
import pygenometracks.plotTracks

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/test_data/"

tracks = """
[test bigwig lines]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = gray
height = 2
type = line
title = orientation=inverted; show data range=no
orientation = inverted
show data range = no
max_value = 50

[test bigwig lines:0.2]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = red
height = 2
type = line:0.2
title = type=line:0.2

[spacer]

[test bigwig points]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = black
height = 2
min_value = -15
max_value = 100
type = points:0.5
title = type=point:0.5; min_value=0;max_value=100

[spacer]

[test bigwig nans to zeros]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = red
height = 2
nans to zeros = True
title = nans to zeros =True

[spacer]

[test bigwig mean]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = gray
height = 5
title = gray:summary method=mean; blue:summary method=max; red:summary method=min
type = line
summary method = mean
max_value = 150
min_value = -50
show data range = no
number of bins = 300

[test bigwig max]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = blue
type = line
summary method = max
show data range = no
overlay previous = share-y
number of bins = 300

[test bigwig min]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = red
type=line
summary method = min
overlay previous = share-y
number of bins = 300

[spacer]

[test bigwig negative color]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = red
negative color = blue
max_value = 15
min_value = -15
#type=line
height = 3
title = negative color = blue


[test bigwig negative color line]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = red
negative color = blue
max_value = 15
min_value = -15
type=line
height = 3
title = negative color = blue type=line
type = line

[test bigwig negative color points]
file = bigwig_chrx_2e6_5e6_with_negative.bw
color = red
negative color = black
max_value = 15
min_value = -15
type=line
height = 3
title = negative color = blue type=line
type = points

[spacer]

[x-axis]
"""

with open(ROOT + "bigwig.ini", 'w') as fh:
    fh.write(tracks)

tolerance = 13  # default matplotlib pixel difference tolerance


def test_narrow_track():
    region = "X:2700000-3100000"
    outfile = NamedTemporaryFile(suffix='.png', prefix='bigwig_test_', delete=False)
    args = "--tracks {root}/bigwig.ini --region {region} --trackLabelFraction 0.2 " \
           "--dpi 130 --outFileName  {outfile}".format(root=ROOT, outfile=outfile.name, region=region).split()
    pygenometracks.plotTracks.main(args)
    print("saving test to {}".format(outfile.name))
    res = compare_images(ROOT + '/master_bigwig.png', outfile.name, tolerance)
    assert res is None, res

    os.remove(outfile.name)
