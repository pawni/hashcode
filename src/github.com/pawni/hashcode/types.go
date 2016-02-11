package github.com/pawni/hashcode

import (
	"bufio"
)

type Params struct {
	NumRows int
	NumCols int
	NumDrones int
	Deadline int
	MaxLoad	int

	NumProducts int
	Products []int // contains weights of each type
	
	NumWarehouses int

	NumOrders int
}

type Product struct {
	Weight int
}

type Warehouse struct {
	Row int
	Col int
	NumItems []int // contains number of each type
}

type Order struct {
	Row int
	Col int
	NumItems int
	Items []int // contains type of each item

