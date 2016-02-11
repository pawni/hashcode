package main

import (
	"math/rand"
	"log"
	"fmt"
	"io"
	"bufio"
	"os/exec"
	"os"

	"github.com/thinxer/genetix"
	"github.com/pawni/hashcode"
)

var TYPES [4]rune = [4]rune{'L', 'U', 'D', 'W'}
var infile string


func writeCmds(writer io.Writer, cmds []Command) {
	for _, c := range cmds {
		writer.Write([]byte(fmt.Sprintf("%d %c ", c.DroneNumber, c.Type)))
		switch c.Type {
		case 'W': writer.Write([]byte(fmt.Sprintf("%d\n", c.NumRounds)))
		case 'L': fallthrough
		case 'U': writer.Write([]byte(fmt.Sprintf("%d %d %d\n", c.WarehouseNumber, c.ProductType, c.NumItems)))
		case 'D': writer.Write([]byte(fmt.Sprintf("%d %d %d\n", c.OrderNumber, c.ProductType, c.NumItems)))
		}
	}
}

type Command struct {
	DroneNumber int
	Type rune // 'L', 'U, 'D', or 'W'
	NumRounds int // for 'W' commands: number of rounds to wait
	OrderNumber int // for 'D' commands
	WarehouseNumber int // for 'L' and 'U' commands
	NumItems int // for 'L', 'U' and 'D' commands: number of items
	ProductType int // ... and product type
}

func (c *Command) Randomize(p *hashcode.Params) {
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
	Params *hashcode.Params
	MutationRate float64
}

func NewSolution(p *hashcode.Params, l int, mutationRate float64, ) Solution {
	s := Solution {}
	s.Cmds = make([]Command, l)
	s.Params = p
	s.MutationRate = mutationRate
	return s
}

func (s *Solution) Randomize() {
	for i, c := range s.Cmds {
		c.Randomize(s.Params)
		s.Cmds[i] = c
	}
}

func (s Solution) Score() float64 {
	// TODO
	proc := exec.Command("python", "parse_out.py", infile)
	reader, _ := proc.StdoutPipe()
	writer, _ := proc.StdinPipe()
	proc.Start()
	writeCmds(writer, s.Cmds)

	score := 0.			
	numCmds := 0
	lineScanner := bufio.NewScanner(reader)
	lineScanner.Split(bufio.ScanLines)
	lineScanner.Scan()
	fmt.Sscan(lineScanner.Text(), &score)
	for lineScanner.Scan() {
		numCmds++
		s.Cmds[numCmds] = Command{}
		c := &s.Cmds[numCmds]
		aa, bb, cc, dd, ee := 0, '0', 0, 0, 0
		fmt.Sscan(lineScanner.Text(), &aa, &bb, &cc, &dd, &ee)
		c.Type = bb
		c.DroneNumber = aa
		switch bb {
		case 'W':
			c.NumRounds = cc
		case 'D':
			c.OrderNumber, c.ProductType, c.NumItems = cc,dd,ee
		case 'L': fallthrough
		case 'U':
			c.WarehouseNumber, c.ProductType, c.NumItems = cc,dd,ee
		}
	}
	// grow to initial size with random commands
	for _, c := range s.Cmds[numCmds:] {
		c.Randomize(s.Params)
	}
	return score
}

func (s Solution) Reset() {
	// isn't called anyway
}

func (s Solution) Mutate() {
	for _, i := range rand.Perm(len(s.Cmds))[:int(s.MutationRate * float64(len(s.Cmds)))] {
		s.Cmds[i].Randomize(s.Params)
	}
}

func (s Solution) CrossOver(o genetix.Entity) {
	other := o.(Solution)
	// assuming len(s.Cmds) == len(other.Cmds)
	cmds1 := make([]Command, len(s.Cmds))
	cmds2 := make([]Command, len(s.Cmds))
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

func (s Solution) Clone() genetix.Entity {
	s2 := NewSolution(s.Params, len(s.Cmds), s.MutationRate)
	copy(s2.Cmds, s.Cmds)
	return s2	
}

func main() {
	infile = os.Args[1]
	p, err := hashcode.ReadParams(infile)
	if err != nil {
		log.Fatal(err)
	}

	pop := make(genetix.EntityPopulation, 20)
	for i := range pop {
		s := NewSolution(p, 500, 0.1)
		s.Randomize()
		pop[i] = s
	}
	for i := 0; i < 100; i++ {
		s := genetix.Evolve(pop, 5, 0.1, 0.3)
		fmt.Println("Epoch number:", i, "Score:", s)
	}

	writeCmds(os.Stdout, pop[0].(*Solution).Cmds)
	
}

