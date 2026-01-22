package main

import (
	"cards/modals"
)

var deck modals.Deck

/*
* The main function is the entry point of the program.
* It is the first function that is called when the program starts.
 */
func main() {
	initializeDeck()
	deck.Shuffle()
	deck.Print()
}

func initializeDeck() {
	deck = modals.Deck{
		Cards: []modals.Card{
			{Value: "Ace", Suit: "Spades"},
			{Value: "Two", Suit: "Spades"},
			{Value: "Three", Suit: "Spades"},
			{Value: "Four", Suit: "Spades"},
			{Value: "Five", Suit: "Spades"},
		},
	}
}
