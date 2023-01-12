package main

import (
	"fmt"
	"bufio"
	"net"
	"strings"
	"github.com/coreos/go-systemd/activation"
)

func handle(conn net.Conn) {
    var res_content string = "Verify socket server"
    defer conn.Close()
    for {
        receives := bufio.NewReader(conn)
        receiveData, e := receives.ReadString('\n')
        if e != nil {
            fmt.Printf("read from conn failed, error:%v\n", e)
            break
        }
        fmt.Printf("Server receive: %v\n", receiveData)
        _, e = conn.Write([]byte(res_content + "\n"))
        if e != nil {
            fmt.Printf("Write from conn failed, error:%v\n", e)
            break
        }
		if strings.Contains(receiveData, "client") {
		    fmt.Println("service server end!")
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
