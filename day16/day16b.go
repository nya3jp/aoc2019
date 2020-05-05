package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func phase(in []int) (out []int) {
	n := len(in)

	sums := make([]int, n + 1)
	for i, v := range in {
		sums[i+1] = sums[i] + v
	}

	capa := func(i int) int {
		if i > n {
			return n
		}
		return i
	}

	sum := func(i, j int) int {
		return sums[capa(j)] - sums[capa(i)]
	}

	digit := func(i int) int {
		if i < 0 {
			return (-i) % 10
		}
		return i % 10
	}

	out = make([]int, n)
	for i := 0; i < n; i++ {
		var o int
		sz := i + 1
		for ofs := i; ofs < n; ofs += 4*sz {
			o += sum(ofs, ofs+sz)
			o -= sum(ofs+sz*2, ofs+sz*3)
		}
		out[i] = digit(o)
	}
	return out
}

func parse(s string) []int {
	var v []int
	for _, c := range s {
		v = append(v, int(c - '0'))
	}
	return v
}

func main() {
	line, err := bufio.NewReader(os.Stdin).ReadString('\n')
	if err != nil {
		panic(err)
	}
	line = strings.TrimSpace(line)

	line = strings.Repeat(line, 10000)

	offset, _ := strconv.Atoi(line[:7])

	ar := parse(line)
	for i := 0; i < 100; i++ {
		fmt.Fprintf(os.Stderr, "Phase %d...\n", i + 1)
		ar = phase(ar)
	}

	for _, v := range ar {
		fmt.Printf("%d", v)
	}
	fmt.Println()

	for _, v := range ar[offset:offset+8] {
		fmt.Printf("%d", v)
	}
	fmt.Println()
}
