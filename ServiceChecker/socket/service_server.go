package main

import (
	"fmt"
	"bufio"
	"net"
	"strings"
	"github.com/coreos/go-systemd/activation"
)

func handle(conn net.Conn) {
    defer conn.Close()
    for {
        receives := bufio.NewReader(conn)
        var buffer [128]byte
        num, e := receives.Read(buffer[:])
        if e != nil {
            fmt.Printf("read from conn failed, error:%v\n", e)
            break
        }
        receiveData := string(buffer[:num])
        fmt.Printf("Server receive: %v\n", receiveData)
        _, e = conn.Write([]byte(receiveData))
        if e != nil {
            fmt.Printf("Write from conn failed, error:%v\n", e)
            break
        }
		if strings.Contains(receiveData, "closed") {
			break
		}
    }
}

func main() {
	fmt.Println("service server start...")
	objListener, e := activation.ListenersWithNames()
	if e != nil {
		fmt.Println("Could not get listening sockets: ", e.Error())
		return
	}
	if listen, exists := objListener["service_verify_server.socket"]; exists {
		var socketListener net.Listener
		socketListener = listen[0]
		defer socketListener.Close()
		for {
			conn, e := socketListener.Accept()
			if e != nil {
				fmt.Printf("receive failed, error:%v\n", e)
				continue
			}
			go handle(conn)
		}
	} else {
		fmt.Println("Service_verify_server.socket not exists.")
		return
	}
}
