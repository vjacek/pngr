# Running
# $ python pngr.py google.com

# Commands
# q - Quit
# p - Pause or Unpause

import sys
import subprocess
import curses
from curses import wrapper
import time
from time import sleep


def pingDrawLoop(stdscr, times, target):

    stdscr.clear()

    # ping and save it
    pingResponse = int(round(ping(target)))
    times.append(pingResponse)

    # all drawing to window
    drawGraph(stdscr, times)
    drawOutput(stdscr, times)

    if any(command in ["--debug", "-d"] for command in sys.argv):
        drawDebugOutput(stdscr, times)

    # After all drawing is done, refresh screen
    stdscr.refresh()


def drawDebugOutput(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()

    stdscr.move(maxY - 10, 10)
    stdscr.addstr("CURRENT TIME: " + str(int(time.time())))

    stdscr.move(maxY - 9, 10)
    stdscr.addstr("DEBUG:        " + str(times))


def drawGraph(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()
    graphMaxY = maxY - 1
    graphMaxX = maxX - 1

    # Draw y axis
    for y in range(0, graphMaxY):
        stdscr.move(y, 0)
        stdscr.addstr(str(graphMaxY - y))

    # Plot data points
    xOffset = 1
    for x in range(xOffset, len(times) + xOffset):
        rangeStart = 0
        if times[x - xOffset] < graphMaxY:
            rangeStart = graphMaxY - times[x - xOffset]
        for y in range(rangeStart, graphMaxY):
            stdscr.move(y, x * 2 + xOffset * 2)
            stdscr.addstr("[]")


# Calculate the average value of a range of most recent data given by length
def getRangeAverage(times, length):
    rangeTotal = 0
    rangeStart = 0 if len(times) <= length else len(times) - length - 1
    rangeCount = min(len(times), length)
    for i in range(rangeStart, len(times) - 1):
        rangeTotal += times[i]
    rangeAverage = round(rangeTotal / rangeCount, 2)
    return rangeAverage


# Draw the bottom output to the screen
def drawOutput(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()
    average1Minute, average5Minute, average15Minute = 0, 0, 0

    if len(times) > 0:
        MINUTE_1, MINUTE_5, MINUTE_15 = 60, 300, 900
        average1Minute = getRangeAverage(times, MINUTE_1)
        average5Minute = getRangeAverage(times, MINUTE_5)
        average15Minute = getRangeAverage(times, MINUTE_15)

    stdscr.move(maxY - 1, 0)
    stdscr.addstr(
        "Count:"
        + str(len(times))
        + "  Last:"
        + str(times[len(times) - 1])
        + "  Min:"
        + str(min(times))
        + "  Max:"
        + str(max(times))
        + "  Average:"
        + str(average1Minute)
        + " "
        + str(average5Minute)
        + " "
        + str(average15Minute)
    )


def ping(target):
    start = time.time()
    response = subprocess.check_output("ping -c 1 " + target, shell=True)
    end = time.time()

    # in practice, python seems to add about 10ms of overhead vs linux ping
    return (end - start) * 1000


def main(stdscr):

    target = sys.argv[1]
    print(">" + str(target) + "<")

    # set up screen
    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(True)

    # set up colors
    curses.curs_set(0)
    curses.start_color()
    curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    stdscr.bkgd(curses.color_pair(1))

    # all recorded ping times
    times = []

    # input loop
    key = ""
    pause = False
    while key != ord("q"):

        # allow pausing
        if key == ord("p"):
            pause = not pause
        if not pause:
            pingDrawLoop(stdscr, times, target)

        sleep(1)  # TODO: find a nicer way of accomplishing wait between pings

        # user input
        key = stdscr.getch()

    # unmount curses terminal interactions
    curses.endwin()


def help():
    print("")
    print("usage: python pngr.py <address> [OPTIONS]")
    print("")
    print("--debug -d               Show debugging info while running")
    print(
        "--save  -s <filename>    -- TO DO -- Save time series data to the given file"
    )
    print("--help                   Print this help message")
    print("")


if __name__ == "__main__":
    if "--help" in sys.argv:
        help()
    else:
        if len(sys.argv) < 2:
            print("Error: Missing URL target")
            help()
            exit()
        else:
            wrapper(main)
