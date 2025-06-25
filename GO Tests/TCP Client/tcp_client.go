package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:9999")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		text := scanner.Text()
		_, err := conn.Write([]byte(text + "\n"))
		if err != nil {
			log.Println("Write error:", err)
			return
		}

		response := make([]byte, len(text)+1)
		_, err2 := conn.Read(response)
		if err2 != nil {
			log.Println("Read error:", err)
			return
		}
		fmt.Print("Echo response: ", string(response))
	}
}
