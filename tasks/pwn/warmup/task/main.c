#include <stdio.h>

void __attribute__ ((constructor)) dumb_constructor() {
	__asm__("push rdi;"
		"pop rdi;");
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    int size;
    char buf[16];

    setup();

    printf("Welcome to the dungeon\n");
    printf("How long? >> ");
    scanf("%d", &size);

    if (size > 16) {
        printf("This is way too much\n");
        return 0;
    }

    printf("Tell us your story >> ");

    read(0, buf, size);
}
