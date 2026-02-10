import numpy as np
import matplotlib.pyplot as plt

class PlotHelper:
    # plotting options:
    x_log = False
    y_log = True
    x_max = None # 500
    y_min = None # 1e-5
    figsize = (10,5) #(6,4)
    legend = 'upper right'
    grid = False
    quant = [(0.25, .1)] #(quantile, color_alpha)

    def __init__(self):
        pass

    def begin(self, title, xlabel, ylabel):
        # plt.clf()
        self.fig, self.ax = plt.subplots(1, 1, figsize=self.figsize)
        if title is not None:
            self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if self.y_log:
            self.ax.set_yscale('log')
        if self.x_log:
            self.ax.set_xscale('log')
        if self.x_max is not None:
            plt.xlim(0, self.x_max)
        self.p_idx = 0

    def add(self, label, xvalues, mid, lo_ups=None, traces=None, linestyle=None):
        # xrange = np.array(range(traces.shape[1]))
        color = self._color()
        if self.x_log:
            xvalues += 1
        if traces is not None:
            self.ax.plot(xvalues, traces.T, color=color, linewidth=0.2)
        self.ax.plot(xvalues, mid, color=color, label=label, linestyle=linestyle, linewidth=1)
        if lo_ups is not None:
            for lo_up in lo_ups:
                self.ax.fill_between(xvalues, lo_up[0], lo_up[1], alpha=lo_up[2], color=color)

        self.p_idx += 1

    def end(self, filename, show=True):
        ylim = self.ax.get_ylim()
        if self.y_min is not None and ylim[0]<self.y_min:
            self.ax.set_ylim(bottom=self.y_min)
        if self.grid:
            plt.grid()
        if self.legend is not None:
            self.ax.legend(loc=self.legend, fontsize=7)
        self.fig.savefig(filename, format='pdf', bbox_inches='tight')
        if show:
            plt.show()
    
    def _color(self):
        return f'C{self.p_idx}'

    def _mean(self, traces):
        return np.mean(traces, axis=0)

    def _std(self, traces):
        return np.std(traces, axis=0)

    def _median(self, traces):
        return np.quantile(traces, 0.5, axis=0)

    def _lo_ups(self, traces):
        lo_ups = []
        for q in self.quant:
            lo_ups.append((np.quantile(traces, q[0], axis=0),
                            np.quantile(traces, 1-q[0], axis=0),
                            q[1]))
        return lo_ups


