# This does not work currently.
# It is kept for a future implementation.
# TODO:
# - Add proto field for "iq" mode
# - Call radio->StartIQMode() from api
# - Add proto message for iq samples
# - Listen on api in python

# set the matplotlib style
matplotlib.style.use('ggplot')

# set the plot mode to interactive
plt.ion()

# add a new figure
fig = plt.figure(figsize=(12, 12))
ax, ap = fig.subplots(2)

# keep the reference to the plot line to dynamically update it
line1 = None

waterfall = []

img = None
cnt = 0


def processData(buf):
    global line1
    global img
    global cnt

    # insert the sample into the waterfall array
    waterfall.append(buf)

    # limit the waterfall elements
    if len(waterfall) > 100:
        waterfall.pop(0)


while True:
    time.sleep(0.01)

    if len(waterfall) == 0:
        continue

    if img == None:
        img = ap.imshow(waterfall, origin='lower', cmap='jet',
                        interpolation='none', aspect='auto')
        ap.set_xlabel('Frequency [Hz]')
        ap.set_ylabel('Time [s]')

    img.set_data(waterfall)

    bf = waterfall[len(waterfall) - 1]

    # check if the chart already exists
    # if it does not exist, create the chart
    # and set the limit
    if line1 == None:
        line1 = ax.plot(bf)[0]
        ax.set_ylim([0, 500])

    # if the chart already exists, just
    # update the data
    if line1 != None:
        line1.set_ydata(bf)

    fig.canvas.draw()
