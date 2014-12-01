#include <fcntl.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>

int main() {
	int fd = open("test.txt", O_RDWR | O_CREAT, 777);
	char buf[11] = "hello world";
	write(fd, buf, 11);
	close(fd);
}