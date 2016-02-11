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

	Products []Product // contains weights of each type
	
	Warehouses []Warehouse

	Orders []Order
	
	MaxNumItems int
	MaxWait int
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
	Items []int // contains type of each item
}

// Returns a deep copy of p
func (p *Params) Copy() (p2 Params) {
	p2 = Params{
		p.NumRows,
		p.NumCols,
		p.NumDrones,
		p.Deadline,
		p.MaxLoad,
		make([]Product, len(p.Products)),
		make([]Warehouse, len(p.Warehouses)),
		make([]Order, len(p.Orders)),
	}
	for pr, i := range p.Products {
		p2.Products[i] = pr
	}
	for wh, i := range p.Warehouses {
		wh.NumItems = make([]int, len(wh.NumItems))
		p2.Warehouses[i] = wh
	}
	for ord, i := range p.Orders {
		ord.Items = make([]int, len(wh.Items))
		p2.Orders[k] = ord
	}
	return p2
}
