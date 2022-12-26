package main

import (
    "os"
    "net"
	"fmt"
	"flag"
	"bufio"
	"strings"
)

func main() {
	fmt.Println("The client is starting...");
	var unix bool
	flag.BoolVar(&unix, "unix", false, " unix 'address' as a path for service")
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage: %s [-unix] address\n", os.Args[0])
		flag.PrintDefaults()
		os.Exit(0)
	}
	flag.Parse()
	addr := flag.Arg(0)
	if addr == "" {
		flag.Usage()
	} else {
		fmt.Println("Connect server by:" + addr)
	}
	conn, e := net.Dial("unix", addr)
    if e != nil {
    	fmt.Println("Client net.Dial error:" + e.Error())
    }
    defer conn.Close()
    read := bufio.NewReader(conn)
	var content string = "Verify socket client"
    for {
		fmt.Print("Client input content: " + content + "\n")
		conn.Write([]byte(content + "\n"))
		returnData, e := read.ReadString('\n')
		if e != nil {
			fmt.Println("Client read string error:" + e.Error())
			break
		}
		fmt.Println("Client receive:" + returnData)
		if strings.Contains(returnData, "server"){
		    fmt.Println("The client is end !")
			break
		}
    }
}
