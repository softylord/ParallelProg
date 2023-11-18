package main

import (
    "fmt"
    "math/rand"
    "sync"
    "time"
)

type pair struct {
    row, col int
}

const length = 1500

var start time.Time
var rez [length][length]int

func main() {
    const threadlength = 20
    pairs := make(chan pair, length)
    var matrix1 [length][length]int
    var matrix2 [length][length]int
    for i := 0; i < length; i++ {
        for j := 0; j < length; j++ {
            matrix1[i][j] = rand.Intn(20)
            matrix2[i][j] = rand.Intn(20)
        }
    }

    var wg sync.WaitGroup
    wg.Add(threadlength)
    for i := 0; i < threadlength; i++ {
        go Calc(pairs, &matrix1, &matrix2, &rez, &wg)
    }
    start = time.Now()
    for i := 0; i < length; i++ {
        for j := 0; j < length; j++ {
            pairs <- pair{row: i, col: j}
        }
    }
    close(pairs)
    wg.Wait()
    duration := time.Since(start)
    fmt.Println(duration)

    /*for i := 0; i < length; i++ {
        for j := 0; j < length; j++ {
            fmt.Print(rez[i][j])
            fmt.Print(" ")
        }
        fmt.Println(" ")
    }*/
}

func Calc(pairs chan pair, a, b, rez *[length][length]int, wg *sync.WaitGroup) {
    for {
        pair, ok := <-pairs
        if !ok {
            break
        }
        rez[pair.row][pair.col] = 0
        for i := 0; i < length; i++ {
            rez[pair.row][pair.col] += a[pair.row][i] * b[i][pair.col]
        }
    }
    wg.Done()
}