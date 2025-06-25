package main

import (
	"io"
	"log"
	"net"
)

func main() {
	addr := "localhost: 9999"
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
	log.Println("Server listening on:", addr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("Connection error:", err)
			continue
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	io.Copy(conn, conn)
}
