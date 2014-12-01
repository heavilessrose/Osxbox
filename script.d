/*
 Main D script for dtrace.

 Copyright 2014, Jose Toro.
 Licensed under MIT.
*/

/* Process create */

proc:::exec-success
{
  printf("%d\nPROCESS\nCREATE\n%s\n%d\n", ppid, execname, pid);
}

/* File open */

syscall::open:entry
{
    self->file = arg0;
}

syscall::open:return
{
    printf("%d\nFILE\nOPEN\n%s\n", pid, copyinstr(self->file));
    self->file = 0;
}