package modals

import (
	"fmt"
	"math/rand/v2"
)

type Deck struct {
	Cards []Card
}

func (d Deck) DrawCard() Card {
	return d.Cards[0]
}

func (d Deck) AddCard(card Card) {
	d.Cards = append(d.Cards, card)
}

func (d Deck) RemoveCard(card Card) {
	for i, c := range d.Cards {
		if c == card {
			d.Cards = append(d.Cards[:i], d.Cards[i+1:]...)
			break
		}
	}
}

func (d Deck) Shuffle() {
	rand.Shuffle(len(d.Cards), func(i, j int) {
		d.Cards[i], d.Cards[j] = d.Cards[j], d.Cards[i]
	})
}

/*
 * Go supports arrays and slices.
 * Arrays are fixed length, slices are dynamic length.
 * Slices are more flexible and easier to use.
 * Slices are a reference to an array.
 * Slices are a view into an array.
 * Slices are a reference to an array.s
 */
func (d Deck) Print() {
	for i, card := range d.Cards {
		fmt.Println(i, card)
	}
}
