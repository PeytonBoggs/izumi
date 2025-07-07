package main

import (
	"crypto/tls"
	"io"
	"log"
	"net"
)

func main() {
	cert, err := tls.LoadX509KeyPair("cert.crt", "cert.key")
	if err != nil {
		log.Fatal("Failed to load certificates:", err)
	}

	config := &tls.Config{Certificates: []tls.Certificate{cert}}
	listener, err := tls.Listen("tcp", ":4443", config)
	if err != nil {
		log.Fatal("Listener error:", err)
	}
	defer listener.Close()

	log.Println("Server listening on :4443")
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Println("Accept error:", err)
			continue
		}
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	io.Copy(conn, conn)
}
