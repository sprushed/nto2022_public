#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void(*ptr)() = 0;

int main() {
    size_t size;
    char buf[16];

    setup();
    char* cur = mmap(0, 0x1000, 7, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    puts("Waiting for your code:");
    size = read(0, cur, 0x20);
    for (int i = 0; i < size; i++) {
        if ((cur[i] == '\x0f') || (cur[i] == '\x05') || (cur[i] == '\x80') || (cur[i] == '\xcd')) {
            puts("Invalid input");
            return 0;
        }
    }
    ptr = (void (*)())cur;
    mprotect(ptr, 0x1000, 5);
    __asm__("xor rdi, rdi;"
            "xor rax, rax;"
            "xor rbx, rbx;"
            "xor rbp, rbp;"
            "xor rcx, rcx;"
            "xor rdx, rdx;"
            "xor rsi, rsi;"
            "xor r8, r8;"
            "xor r9, r9;"
            "xor r10, r10;"
            "xor r11, r11;"
            "xor r12, r12;"
            "xor r13, r13;"
            "xor r14, r14;"
            "xor r15, r15;"
            "call qword ptr %0" : :"m"(ptr)
    );
}