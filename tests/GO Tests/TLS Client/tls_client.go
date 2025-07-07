package main

import (
	"crypto/tls"
	"io"
	"log"
	"os"
)

func main() {
	config := &tls.Config{InsecureSkipVerify: true}
	conn, err := tls.Dial("tcp", "localhost:4443", config)
	if err != nil {
		log.Fatal("Connection error:", err)
	}
	defer conn.Close()

	go func() {
		io.Copy(os.Stdout, conn)
	}()

	_, err = io.Copy(conn, os.Stdin)
	if err != nil {
		log.Fatal("Write error: err")
	}
}
