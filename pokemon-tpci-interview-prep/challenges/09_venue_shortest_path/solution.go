//go:build solution

// Shortest path across the venue floor — reference solution (BFS).
//
// Why BFS? Every step costs 1. BFS explores in rings (everything 1 step away, then 2,
// ...), so the first time it reaches E, that path is a shortest one.
// Time and space are O(rows*cols): each cell is queued at most once.
package venue

// point is a small comparable struct, so it can be a map key directly.
type point struct{ r, c int }

func ShortestPath(grid []string) int {
	// ---- Find S and E ----
	var start, end point
	foundS, foundE := false, false
	for r, row := range grid {
		// Ranging over a string yields (byteIndex, rune). The grid is ASCII, so the byte
		// index equals the column.
		for c, ch := range row {
			switch ch {
			case 'S': // single quotes: a rune literal, not a string
				start, foundS = point{r, c}, true
			case 'E':
				end, foundE = point{r, c}, true
			}
		}
	}
	if !foundS || !foundE {
		return -1
	}

	// dist doubles as the visited set: a cell is in dist once it has been queued.
	dist := map[point]int{start: 0}

	// A slice used as a FIFO queue: append to the back, take from the front with
	// queue[1:]. Simple, and fine for interview-sized grids.
	queue := []point{start}
	dirs := []point{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} // down, up, right, left

	for len(queue) > 0 {
		cur := queue[0]
		queue = queue[1:] // dequeue the oldest cell; that's what makes it breadth-first

		if cur == end { // structs with comparable fields can be compared with ==
			return dist[cur]
		}

		for _, d := range dirs {
			n := point{cur.r + d.r, cur.c + d.c}
			// Skip if out of bounds or a wall. Go's || short-circuits, so the bounds
			// checks protect the grid[n.r][n.c] index from going out of range.
			if n.r < 0 || n.r >= len(grid) || n.c < 0 || n.c >= len(grid[n.r]) || grid[n.r][n.c] == '#' {
				continue
			}
			if _, seen := dist[n]; seen {
				continue // already queued
			}
			// Mark it visited when ENQUEUING, so no cell is ever queued twice.
			dist[n] = dist[cur] + 1
			queue = append(queue, n)
		}
	}
	return -1 // the queue emptied without reaching E: unreachable
}
