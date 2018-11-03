#ifndef GETKEY_KBHIT_H
#define GETKEY_KBHIT_H

extern void init_keyboard(void);
extern void close_keyboard(void);
extern int kbhit(void);
extern int readch(void);

#endif //GETKEY_KBHIT_H
