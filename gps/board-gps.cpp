#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <termios.h>

#include <gps_board.h>

#define DEVICE "/dev/ttyAMA1"
#define BAUDRATE B9600

static struct termios s_tios;

int  board_gps_init(void)
{
    struct termios tios;
    int fd = open(DEVICE, O_RDWR|O_NOCTTY);
    if (fd < 0) {
        //fprintf(stderr, "%s: can't open device %s\n", __func__, DEVICE);
        return -EINVAL;
    }

    tcgetattr(fd, &s_tios);
    tcgetattr(fd, &tios);

    tios.c_iflag &= (~BRKINT);
    tios.c_iflag |= (IGNBRK);
    tios.c_lflag &= ~(ISIG|ICANON|ECHO);
    tios.c_cflag = BAUDRATE | CS8 | CLOCAL | CREAD;
    tcsetattr(fd, TCSANOW, &tios);

    return fd;
}

void board_gps_deinit(int handle)
{
    tcsetattr(handle, TCSANOW, &s_tios);
    close(handle);
}

int board_gps_read(int handle, char *buf, size_t buf_size)
{
    return read(handle, buf, buf_size);
}
