#include <stdio.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void __libc_init_() {
	execve("/bin/bash", 0, 0);
}

int main() {
	char buf[32] = {0};
	setup();

	puts("I don't know just type smth...");
	read(0, buf, 0x100);
}
