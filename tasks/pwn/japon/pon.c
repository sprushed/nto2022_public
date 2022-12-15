#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define NOTE_LEN 16
#define INT_LEN 8
#define MAX_NOTES 2

typedef struct
{
    char note[NOTE_LEN];
    int allocated;
} note_t;

note_t* notes[MAX_NOTES];

void read_data(char* buffer, unsigned int len)
{
    fgets(buffer, len - 1, stdin);
    buffer[len - 1] = 0;
}

int read_int()
{
    char buffer[INT_LEN];
    read_data(buffer, INT_LEN);
    return atoi(buffer);
}

void add_note()
{
    for (int i = 0; i < MAX_NOTES; i++)
    {
        if (!notes[i] || !notes[i]->allocated)
        {
            note_t* note = malloc(sizeof(note_t));
            printf("あなたは私にどれだけ入れたいですか?\n");
            unsigned int len = read_int();
            if (len > NOTE_LEN)
            {
                printf("そんなに収まりきらないよ、お兄ちゃん\n");
                return;
            }
            printf("私を満たして\n");
            read_data(note->note, len);
            note->allocated = 1;
            notes[i] = note;
            return;
        }
    }
    printf("あなたは私を完全に満たした、兄弟\n");
}

note_t* get_note()
{
    printf("メモを選択\n");
    printf("> ");
    unsigned int note_id = read_int();
    if (note_id >= MAX_NOTES)
    {
        printf("申し訳ありませんが、兄弟、私はこれを行う方法がわかりません\n");
        return 0;
    }
    if (!notes[note_id] || !notes[note_id]->allocated)
    {
        printf("申し訳ありませんが、兄弟、私はこれを行う方法がわかりません\n");
        return 0;
    }
    return notes[note_id];
}

void delete_note()
{
    note_t* note = get_note();
    if (!note)
        return;
    note->allocated = 0;
    free(note);
}

void read_note()
{
    note_t* note = get_note();
    if (!note)
        return;
    printf("%s", note->note);
}

void menu()
{
    printf("1. メモを追加\n");
    printf("2. メモを削除\n");
    printf("3. メモを読む\n");
    printf("> ");
}

int main()
{
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    printf("鬼ちゃんにメモしておきます\n");
    printf("自分用に 1 つ、私用に 1 つずつ書いてください\n");
    while (1)
    {
        menu();
        int choose = read_int();
        switch (choose)
        {
        case 1:
            add_note();
            break;
        case 2:
            delete_note();
            break;
        case 3:
            read_note();
            break;
        default:
            printf("申し訳ありませんが、兄弟、私はこれを行う方法がわかりません\n");
            exit(0);
        }
    }
} 
