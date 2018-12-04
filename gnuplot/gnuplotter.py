try:
    import PyGnuplot as gplot
except ImportError:
    print("No PyGnuplot module. Try command pip3 install PyGnuplot")



gplot.c('set xrange [-150:150]')
gplot.c('set yrange [-150:150]')
gplot.c('set zrange [-150:150]')
gplot.c('splot "../data/base.dat" with linespoints, \
"../data/finger0.dat" with linespoints, \
"../data/finger1.dat" with linespoints, \
"../data/finger2.dat" with linespoints, \
"../data/finger3.dat" with linespoints;')