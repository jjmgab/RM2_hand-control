set xrange [-150:150]
set yrange [-150:150]
set zrange [-150:150]
splot "../data/base.dat" with linespoints, \
"../data/finger0.dat" with linespoints, \
"../data/finger1.dat" with linespoints, \
"../data/finger2.dat" with linespoints, \
"../data/finger3.dat" with linespoints;
pause -1
