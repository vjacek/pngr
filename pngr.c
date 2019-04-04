#include <stdlib.h>
#include <curses.h>

int main(void) {

  // initialize curses
  initscr();
  cbreak();
  noecho();

  clear();




  printf("hello world \r\n");


  getch();
  endwin();

  exit(0);
}