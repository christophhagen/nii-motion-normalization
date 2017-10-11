
import plotly
import plotly.graph_objs as go
import numpy

plotList = []


def addPlot(motion, title='No name'):
    """!
    Add a three-dimensional motion to the list of plots.

    @param motion numpy array: The motion to plot, 3 columns (x,y,z)
    @param title String: The legend entry of the plot
    """
    global plotList
    trace = go.Scatter3d(
        x=motion[:,0],
        y=motion[:,1],
        z=motion[:,2],
        name=title,
        marker=dict(
            size=5
        )
    )
    plotList.append(trace)

def plot(title='Untitled'):
    """!
    Generate the html file of the plots previously added with 'addPlot'.
    Automatically removes all plots from the internal list.

    @param title: The filename (and possibly path) of the resulting file (without html ending)
    """
    global plotList
    if len(plotList) > 0:
        plotly.offline.plot({
            "data": plotList,
            "layout": go.Layout(title=title)
            }, filename=title + '.html', auto_open=False)
        plotList = []

def clearPlot():
    """!
    Remove all plots from the current list.
    """
    global plotList
    plotList = []
