import time

import PyGnuplot as gplot


def plot(data):
    assert type(data) == str, "data must be a directory as string"
    if data[-1] != '/':
        data.append('/')
    gplot.c('set xrange [-40:150]')
    gplot.c('set yrange [-40:150]')
    gplot.c('set zrange [-40:150]')
    gplot.c('splot "' + data + 'base.dat" with linespoints, \
    "' + data + 'finger0.dat" with linespoints, \
    "' + data + 'finger1.dat" with linespoints, \
    "' + data + 'finger2.dat" with linespoints, \
    "' + data + 'finger3.dat" with linespoints;')


def replot():
    gplot.c('replot')


if __name__ == '__main__':
    plot('../data/')
    while True:
        time.sleep(1)
        gplot.c('replot')
