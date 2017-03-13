from .engine import PlottingEngine, PlottingFigure, PlottingLayout
import plotly
from plotly.graph_objs import Scatter, Layout, Data

plotly.offline.init_notebook_mode(connected=True)

plotly.offline.iplot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1], mode = 'lines')],
    "layout": Layout(title="hello world")
})

class PlotlyFigure(PlottingFigure):
    def __init__(self, title=None, layout=PlottingLayout()):
        self.title = title
        self.xy_datasets = []

    def addXYDataset(self, x_arr, y_arr, name=None):
        """ Adds an X/Y dataset to the plot.

        :param x_arr: A numpy array describing the X datapoints. Should have the same size as y_arr.
        :param y_arr: A numpy array describing the Y datapoints. Should have the same size as x_arr.
        """
        dataset = {'x': x_arr, 'y': y_arr}
        if name is not None:
            dataset['name'] = name
        self.xy_datasets.append(dataset)

    def makeLayout(self):
        kwargs = {}
        if self.title is not None:
            kwargs['title'] = self.title
        return Layout(**kwargs)

    def plot(self):
        """ Plot the figure. Call this last."""
        traces = []
        for dataset in self.xy_datasets:
            kwargs = {}
            if 'name' in dataset:
                kwargs['name'] = dataset['name']
            traces.append(Scatter(
                x = dataset['x'],
                y = dataset['y'],
                mode = 'lines',
                **kwargs
            ))

        data = Data(traces)
        plotly.offline.iplot({
            'data': data,
            'layout': self.makeLayout()
        })

class PlotlyPlottingEngine(PlottingEngine):
    def newFigure(self, title=None, layout=PlottingLayout()):
        """ Returns a figure object."""
        return PlotlyFigure(title=title, layout=layout)

    def figureFromTimecourse(self, m, title=None):
        """ Generate a new figure from a timecourse simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.newFigure()
        if m.colnames[0] != 'time':
            raise RuntimeError('Cannot plot timecourse - first column is not time')

        for k in range(1,m.shape[1]):
            fig.addXYDataset(m[:,0], m[:,k], name=m.colnames[k])

        return fig

    def plotTimecourse(self, m, title=None):
        """ Plots a timecourse from a simulation.

        :param m: An array returned by RoadRunner.simulate.
        """
        fig = self.figureFromTimecourse(m, title=title)
        fig.plot()