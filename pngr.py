# Running
# $ python pngr.py google.com

# Commands
# q - Quit

import sys, os
import curses
from curses import wrapper
import time
from time import sleep


def pingDrawLoop(stdscr, times):
    
    stdscr.clear()

    # ping and save it
    pingResponse = int(round(ping()))
    times.append(pingResponse)

    # all drawing to window
    drawGraph(stdscr, times)
    drawOutput(stdscr, times)

    if any(command in ['--debug', '-d'] for command in sys.argv):
        drawDebugOutput(stdscr, times)

    # After all drawing is done, refresh screen
    stdscr.refresh()

def drawDebugOutput(stdscr, output):
    maxY, maxX = stdscr.getmaxyx()
    
    stdscr.move(maxY-40, 5)
    stdscr.addstr('DEBUG: '+str(output))
    
    stdscr.move(maxY-41, 5)
    stdscr.addstr('CURRENT TIME: '+str(int(time.time())))

def drawGraph(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()
    graphMaxY = maxY - 3
    for x in range(0, len(times)):
        stdscr.move(graphMaxY, x)
        for y in range (graphMaxY-times[x], graphMaxY):
            stdscr.move(y, x)
            stdscr.addstr("x")
   
def drawOutput(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()
    average1Minute, average5Minute, average15Minute = 0, 0, 0
    if(len(times) > 0): 
        total1Minute, total5Minute, total15Minute = 0, 0, 0
        total1MinuteCount, total5MinuteCount, total15MinuteCount = min(len(times), 60), min(len(times), 300), min(len(times), 900)
        
        for i in range(len(times) - total1MinuteCount, len(times)):
            total1Minute += times[len(times)-1-i]
        average1Minute = round(total1Minute / len(times), 2)
        for i in range(len(times) - total5MinuteCount, len(times)):
            total5Minute += times[len(times)-1-i]
        average5Minute = round(total5Minute / len(times), 2)
        for i in range(len(times) - total15MinuteCount, len(times)):
            total15Minute += times[len(times)-1-i]
        average15Minute = round(total15Minute / len(times), 2)

    stdscr.move(maxY-1, 0)
    stdscr.addstr('Last: '+str(times[len(times)-1])+' Average: '+str(average1Minute)+', '+str(average5Minute)+', '+str(average15Minute))
    

def ping():
    start = time.time()
    response = os.system("ping -c 1 "+sys.argv[1])
    end = time.time()

    # in practice, python seems to add about 10ms of overhead vs linux ping
    return (end - start)*1000


def main(stdscr): 
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
    key = ''
    while(key != ord('q')):

        pingDrawLoop(stdscr, times)
        sleep(1) # TODO: find a nicer way of accomplishing wait between pings

        # user input
        key = stdscr.getch()

    # unmount curses terminal interactions
    curses.endwin()

def help():
    print('')
    print('usage: python pngr.py <address> [OPTIONS]')
    print('')
    print('--debug -d               Show debugging info while running')
    print('--save  -s <filename>    -- TO DO -- Save time series data to the given file')
    print('--help                   Print this help message')
    print('')

if __name__ == "__main__":
    if '--help' in sys.argv:
        help()
    else:
        wrapper(main)
