#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char 🌚;
typedef int 🌝;
typedef void 😶;

#define 🖨 fprintf
#define 🎲 rand
#define 📕 srand
#define 👌 strlen

🌚* 🔀(🌝 📏) {
    🌚* 🌟 = malloc(📏);
    for (🌝 🆖 = 0; 🆖 < 📏; 🆖++) {
        🌟[🆖] = rand() % 256;
    }

    return 🌟;
}

😶 🤓(🌚* 🏁, 🌝 🏁📏, 🌚* 🔑, 🌝 🔑📏) {
    for (🌝 🆖 = 0; 🆖 < 🏁📏; 🆖++) {
        🏁[🆖] ^= 🔑[🆖 % 🔑📏];
    }
}

😶 👉(🌚* 🅰️, 🌝 🅰️📏) {
    🌚 🅱️ = 🅰️[🅰️📏 - 1];
    for (🌝 🆖 = 🅰️📏 - 1; 🆖 > 0; 🆖--) {
        🅰️[🆖] = 🅰️[🆖 - 1];
    }
    🅰️[0] = 🅱️;
}



😶 🔒(🌚* 🏁, 🌝 📏, 🌚* 🔑, 🌝 🔑📏) {
    for (🌝 🆔 = 0; 🆔 < 📏; 🆔++) {
        🤓(🏁, 📏, 🔑, 🔑📏);
        👉(🔑, 🔑📏);
    }
}


🌝 main(🌝 🆖, 🌚 *🌟[]) {
    setbuf(stderr, NULL);
    if (🆖 != 2) {
        🖨(stderr, "Provide flag as the first argument!\n");
        return 1;
    }

    🌚* 🏁 = 🌟[1];
    🌝 📏 = 👌(🏁);

    📕(0x1337);
    🌚* 🔑 = 🔀(10);

    🔒(🏁, 📏, 🔑, 10);

    for (🌝 🆔 = 0; 🆔 < 📏; 🆔++) {
        🖨(stdout, "%02x", 🏁[🆔]);
    }
    🖨(stdout, "\n");
    return 0;
}

