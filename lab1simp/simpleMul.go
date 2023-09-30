package main

import (
	"fmt"
	"math/rand"
	"time"
)

func simpMul(matrix1, matrix2 [][]int, n int) [][]int {
	mulmatrix := make([][]int, n)
	for i := 0; i < n; i++ {
		mulmatrix[i] = make([]int, n)
	}
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			for k := 0; k < n; k++ {
				mulmatrix[i][j] += matrix1[i][k] * matrix2[k][j]
			}
		}
	}
	return mulmatrix
}

func main() {
	start := time.Now()
	n := 1500
	matrix1 := make([][]int, n)
	matrix2 := make([][]int, n)
	mulmatrix := make([][]int, n)
	for i := 0; i < n; i++ {
		matrix1[i] = make([]int, n)
		matrix2[i] = make([]int, n)
		mulmatrix[i] = make([]int, n)
		for j := 0; j < n; j++ {
			matrix1[i][j] = rand.Intn(20)
			matrix2[i][j] = rand.Intn(20)
		}
	}
	rand.Seed(time.Now().UTC().UnixNano())

	mulmatrix = simpMul(matrix1, matrix2, n)
	/*for i:=0; i<n; i++{
		for j:=0; j<n; j++{
			for k:=0; k<n; k++{
				mulmatrix[i][j]+=matrix1[i][k]*matrix2[k][j]
			}
		}
	}
	for i:=0; i<n; i++{
		for j:=0; j<n; j++{
			fmt.Printf("%d ", matrix1[i][j])
		}
		fmt.Printf("\n")
	}
	fmt.Printf("\n")
	for i:=0; i<n; i++{
		for j:=0; j<n; j++{
			fmt.Printf("%d ", matrix2[i][j])
		}
		fmt.Printf("\n")
	}
	fmt.Printf("\n")*/
	/*for i:=0; i<n; i++{
		for j:=0; j<n; j++{
			fmt.Printf("%d ", mulmatrix[i][j])
		}
		fmt.Printf("\n")
	}*/
	duration := time.Since(start)
	fmt.Printf("%v\n", duration)
}
