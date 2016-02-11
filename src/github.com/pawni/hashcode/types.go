package hashcode

import (
	"os"
	"encoding/json"
)

func ReadParams(filename string) (*Params, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	dec := json.NewDecoder(file)
	p := Params{}
	err = dec.Decode(&p)
	if err != nil {
		return nil, err
	}
	p.MaxNumItems = 10
	p.MaxWait = 10
	return &p, nil
}

type Params struct {
	NumRows int `json:"numRows"`
	NumCols int `json:"numCols"`
	NumDrones int `json:"numDrones"`
	Deadline int `json:"numTurns"`
	MaxLoad	int `json:"maxPayload"`

	Products []Product `json:"productWeights"`
	
	Warehouses []Warehouse `json:"warehousesData"`

	Orders []Order `json:"orderData"`
	
	MaxNumItems int
	MaxWait int
}

type Product int // weight of product

type Warehouse struct {
	Row int `json:"x"`
	Col int `json:"y"`
	NumItems []int `json:"items"` // contains number of each type
}

type Order struct {
	Row int `json:"x"`
	Col int `json:"y"`
	Items []int  `json:"items"` // contains type of each item
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
		10000, 10, 
	}
	for i, pr := range p.Products {
		p2.Products[i] = pr
	}
	for i, wh := range p.Warehouses {
		wh.NumItems = make([]int, len(wh.NumItems))
		p2.Warehouses[i] = wh
	}
	for i, ord := range p.Orders {
		ord.Items = make([]int, len(ord.Items))
		p2.Orders[i] = ord
	}
	return p2
}
