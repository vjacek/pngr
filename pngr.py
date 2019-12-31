# Running
# $ python pngr.py google.com

# Commands
# q - Quit

import sys
import subprocess
import curses
from curses import wrapper
import time
from time import sleep
import signal


def pingDrawLoop(stdscr, times, target):
    
    stdscr.clear()

    # ping and save it
    pingResponse = int(round(ping(target)))
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
    
    stdscr.move(maxY-40, 50)
    stdscr.addstr('DEBUG: '+str(output))
    
    stdscr.move(maxY-41, 50)
    stdscr.addstr('CURRENT TIME: '+str(int(time.time())))

def drawGraph(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()
    graphMaxY = maxY - 3

    # Draw x axis
    for y in range(0, graphMaxY):
        stdscr.move(y, 0)
        stdscr.addstr(str(graphMaxY-y));

    # Plot data points
    xOffset = 2
    for x in range(xOffset, len(times)+xOffset):
        for y in range (graphMaxY-times[x-xOffset], graphMaxY):
            stdscr.move(y, x*2+xOffset*2)
            stdscr.addstr('[]')
               
def drawOutput(stdscr, times):
    maxY, maxX = stdscr.getmaxyx()
    average1Minute, average5Minute, average15Minute = 0, 0, 0
    if(len(times) > 0): 
        total1Minute, total5Minute, total15Minute = 0, 0, 0

        #rangeStart1Minute = max(0, len(times)-10)
        MINUTE_1, MINUTE_5, MINUTE_15 = 10, 300, 900
        rangeStart1Minute = 0 if len(times) < MINUTE_1 else len(times) - MINUTE_1
        count1Minute = min(len(times), MINUTE_1)
        

        #count1Minute, count5Minute, count15Minute = min(len(times), 10), min(len(times), 300), min(len(times), 900)
        




        # TODO: there's an error in the calculation here.... once there are 60 readings, average1Minute always decreases
        for i in range(rangeStart1Minute, len(times)-1):
            total1Minute += times[i]
        average1Minute = round(total1Minute / count1Minute, 2)


        stdscr.move(maxY-40, 50)
        stdscr.addstr('rangeStart1Minute: '+str(rangeStart1Minute))
        stdscr.move(maxY-39, 50)
        stdscr.addstr('rangeEnd1Minute:   '+str(len(times)-1))
        stdscr.move(maxY-38, 50)
        stdscr.addstr('range:             '+str(range(rangeStart1Minute, len(times)-1)))
        stdscr.move(maxY-37, 50)
        stdscr.addstr('count1Minute:      '+str(count1Minute))
        stdscr.move(maxY-36, 50)
        stdscr.addstr('total1Minute:      '+str(total1Minute))







        # for i in range(len(times) - total5MinuteCount, len(times)-1):
        #     total5Minute += times[len(times)-1-i]
        # average5Minute = round(total5Minute / len(times), 2)
        # for i in range(len(times) - total15MinuteCount, len(times)):
        #     total15Minute += times[len(times)-1-i]
        # average15Minute = round(total15Minute / len(times), 2)

    stdscr.move(maxY-1, 0)
    stdscr.addstr('Last:  '+str(times[len(times)-1])+'  Count: '+str(len(times))+'  Average: '+str(average1Minute)+', '+str(average5Minute)+', '+str(average15Minute))
    

def ping(target):
    start = time.time()
    response = subprocess.check_output("ping -c 1 "+target, shell=True)
    end = time.time()

    # in practice, python seems to add about 10ms of overhead vs linux ping
    return (end - start)*1000


def main(stdscr): 

    print('test')

    if(len(sys.argv) < 2):
        print('Error: Missing URL target')
        #help()
        #exit()
    else:
        target = sys.argv[1]
        print(">"+str(target)+"<")


        # signal.pause()

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

            pingDrawLoop(stdscr, times, target)
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
