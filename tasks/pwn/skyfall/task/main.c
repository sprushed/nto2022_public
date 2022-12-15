#include <stdio.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
	char buf[256] = {0};
	setup();
	puts("I WILL TALK WITH YOU FOREVER");
	for (;;) {
		puts("TELL ME RIGHT F NOW WHAT IS YOUR NAME?");
		read(0, buf, 256);
		if (!strncmp(buf, "exit", 4)) {
			break;
		}
		printf(buf);
	}
}
