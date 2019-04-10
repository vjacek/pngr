#include <stdlib.h>
#include <curses.h>

int main(void) {

  // initialize curses
  initscr();
  cbreak();
  noecho();

  //clear();
  int max_row, max_col;
  getmaxyx(stdscr, max_row, max_col);

  ///////// todo: remove when done testing
  mvprintw(1, 1, "row: ");
  mvprintw(2, 2, "%i", max_row);
  mvprintw(3, 3, "col: ");
  mvprintw(4, 4, "%i", max_col);
  refresh();  

  int command = getch();
  while (command != 'q') {

 
    if (command == 'a') {
      mvprintw(max_row-1, 0, "aaaaaaaaaaa");
      refresh();
    }

    
    else if (command == 'q') {
      endwin();
      return 0;
    }
 
    command = getch();
  }
  
}
