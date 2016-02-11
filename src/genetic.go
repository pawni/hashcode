package main

import (
	"math/rand"

	"github.com/thinxer/genetix"
	"github.com/pawni/hashcode"
)

var TYPES [4]rune = {'L', 'U', 'D', 'W'}

type Command struct {
	DroneNumber int
	Type rune // 'L', 'U, 'D', or 'W'
	NumRounds int // for 'W' commands: number of rounds to wait
	OrderNumber int // for 'D' commands
	WarehouseNumber int // for 'L' and 'U' commands
	NumItems int // for 'L', 'U' and 'D' commands: number of items
	ProductType int // ... and product type
}

func (c *Command) Randomize(p *Params) {
	*c = Command{}
	c.DroneNumber = rand.Intn(p.NumDrones)
	c.Type = TYPES[rand.Intn(len(TYPES))]
	switch c.Type {
	case 'W': 
		c.NumRounds = rand.Intn(p.MaxWait) + 1
	default:
		c.NumItems = rand.Intn(p.MaxNumItems)
		c.ProductType = rand.Intn(len(p.Products))
	}
	switch c.Type {
	case 'D':
		c.OrderNumber = rand.Intn(len(p.Orders))
	case 'L': fallthrough
	case 'U':
		c.WarehouseNumber = rand.Intn(len(p.Warehouses))
	}
}


type Solution struct {
	Cmds []Command
	Params *Params
	NumMutations int
}

func NewSolution(p *Params, l int, mutationRate float64, ) Solution {
	s := Solution {}
	s.Cmds = make(Solution, l)
	s.Params = p
	s.MutationRate = mutationRate
	return s
}

func (s *Solution) Randomize() {
	for _, c := range s {
		c.Randomize(s.Params)
	}
}

func (s *Solution) Score() float64 {
	// TODO
	return 0
}

func (s *Solution) Reset() {
	// isn't called anyway
}

func (s *Solution) Mutate() {
	for _, i := range rand.Perm(len(s.Cmds))[:int(s.MutationRate * float64(len(s.Cmds)))] {
		s.Cmds[i].Randomize()
	}
}

func (s *Solution) CrossOver(other *Solution) {
	// assuming len(s.Cmds) == len(other.Cmds)
	cmds1 = make([]Command, len(s.Cmds))
	cmds2 = make([]Command, len(s.Cmds))
	i1, i2 := 1 + rand.Intn(len(s.Cmds)), 1+ rand.Intn(len(s.Cmds))
	if i1 > i2 {
		i1, i2 = i2, i1
	}
	copy(cmds1[:i1], s.Cmds[:i1])
	copy(cmds2[:i1], other.Cmds[:i1])
	copy(cmds1[i1:i2], other.Cmds[i1:i2])
	copy(cmds2[i1:i2], s.Cmds[i1:i2])
	copy(cmds1[i2:], s.Cmds[i2:])
	copy(cmds2[i2:], other.Cmds[i2:])
	s.Cmds = cmds1
	other.Cmds = cmds2
}

func (s *Solution) Clone() *Solution {
	s2 = NewSolution(s.Params, len(s.Cmds), s.MutationRate))
	copy(s2.Cmds, s.Cmds)
	return &s2	
}

