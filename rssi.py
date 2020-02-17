import matplotlib.pyplot as plt
import matplotlib


class RSSI:
    serial = None
    fig = None
    plt = None
    line = None
    count = 4096
    rssibuf = [0] * count
    x = list(range(0, count))

    def __init__(self, api):
        self.api = api

    def start(self):
        self.show()
        self.api.receive('rssi', self.receive)

    def receive(self, msg):
        rssi = msg.rssi.rssi

        self.rssibuf.append(rssi)
        if len(self.rssibuf) > self.count:
            self.rssibuf.pop(0)

    def show(self):
        # set the matplotlib style
        matplotlib.style.use('ggplot')

        # set the plot mode to interactive
        plt.ion()

        # add a new figure
        self.fig = plt.figure(figsize=(12, 12))
        self.plt = self.fig.add_subplot(1, 1, 1)
        self.line = self.plt.plot(self.x, self.rssibuf)[0]
        self.plt.set_ylim(-120, -24)

    def plot(self):
        self.line.set_ydata(self.rssibuf)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
