# Advent of Code 2024

For the seventh time tried to find out how far I can make it in [Advent of Code](https://adventofcode.com/2023/). Results for previous editions:
* 2018: 9 days
* 2019: 13 days
* [2020](https://github.com/Leftfish/Advent-of-Code-2020): 25 days for the first time!
* [2021](https://github.com/Leftfish/Advent-of-Code-2021): 25 days for the second time!
* [2022](https://github.com/Leftfish/Advent-of-Code-2022): 25 days for the third time!
* [2023](https://github.com/Leftfish/Advent-of-Code-2023): 25 days for the fourth time!

Not only am I (still) not a pro, nor do I have a degree in computer science, but also this is a pretty challenging time for me. As of Day 25, I managed to solve all the problems on the day of their release with two exceptions - Days 21 and Day 24 part 2. I finished Day 24 a day too late, mostly due to time constraints. Day 21 is just very difficult for me, and as far as I know, I'm not the only one who struggles with it. I do have an idea how to approach it, but time is not unlimited, so it has to wait a bit longer. On the whole, 47 stars on Day 25 is probably my best result ever in AoC.

Although I'm not done yet, I can already say that it was a pretty good year in terms of not having to rely on suggestions, tutorials and other solutions. For now, I needed that twice. [Day 16 part 2](https://adventofcode.com/2024/day/16) was the first one that required me to have a look at the solutions posted by the [AoC community on reddit](https://www.reddit.com/r/adventofcode/) - it turned out that I had the right ideas and terrible approaches to implementation. Another one was Day 20 part 2 - I think I was just tired, because I ended up solving the puzzle after applying an idea that I'd already used this year, but needed a nudge from Reddit to return to it. 

Things I **L**earned, **R**evised or **I**mproved at in 2024:

* [Day 1 Python](01/d01.py): reading comprehension (because I tried to solve a much harder puzzle for about 20 minutes...) and collections.Counter (**R**)
* [Day 2 Python](02/d02.py): zip on the same list to create pairs for the first attempt (**R**), and pop(idx) (**R**) for a far too complicated solution, because I over-worried about edge cases
* [Day 3 Python](03/d03.py): using logical operators in regex (**I**)
* [Day 4 Python](04/d04.py): operations on numpy arrays (rotate, diagonals) (**I**)
* [Day 5 Python](05/d05.py): set operations (**R**) and writing custom comparator for functools.cmp_to_key (**R**)
* [Day 6 Python](06/d06.py): storing grids in dictionaries (**R**)
* [Day 7 Python](07/d07.py): BFS (**R**) and Python operator (**R**) for a solution that's inefficient, but works; recursion (**I**) for an improved and much faster solution
* [Day 8 Python](08/d08.py): set operations (**R**)
* [Day 9 Python](09/d09.py): OH GOSH, WHAT THE HELL WAS THAT. Spent far too many hours debugging a seemingly simple solution, ended up refreshing itertools.cycle (**R**), deques (**R**) and thinking with pointers (**R**) before figuring out where the bug was
* [Day 10 Python](10/d10.py): iterative DFS (**R**)
* [Day 11 Python](11/d11.py): that you don't have to store everything that you count, just like [twice](https://github.com/Leftfish/Advent-of-Code-2021/blob/main/06/d06.py) in [2021](https://github.com/Leftfish/Advent-of-Code-2021/blob/main/14/d14.py) (**R**)
* [Day 12 Python](12/d12.py): BFS (**R**), finding islands in 2d grid (**R**) and finding sides of a 2D polygon (**L**)
* [Day 13 Python](13/d13.py): linear algebra (**I**) and Cramer's rule (**L**)
* [Day 14 Python](14/d14.py): using modulo (**R**) and saving plots made in matplotlib (**L**) (which I tried in a buggy solution what didn't make it to the final one)
* [Day 15 Python](15/d15.py): reinventing the wheel, because that's what I did when I came up with something that turned out to be just flood-fill BFS (**R**)
* [Day 16 Python](16/d16.py): Dijkstra's algorithm (**R**) with a twist requiring me to track the paths and that really made it difficult for me to implement (**L**)
* [Day 17 Python](17/d17.py): reverse-engineering (**I**), thinking in bases other than 2 and 10, namely base8 (**L**), bitwise operations (**I**) and DFS (**R**) to solve the toughest and most entertaining puzzle so far this year
* [Day 18 Python](18/d18.py): I've already implemented Dijkstra's algorithm this year, so this time I decided to refresh networkx (**R**) and binary search for part 2 (**R**)
* [Day 19 Python](19/d19.py): recursive functions (in fact - pretty much a DFS?) (**I**), LRU-cache (**R**) and frozenset (**R**)
* [Day 20 Python](20/d20.py): Dijkstra's algorithm again (**R**) and the idea to run it from start to end in a maze, then from end to start (**I**), Manhattan distance (**R**), generators (**R**)
* Day 21: TO DO
* [Day 22 Python](22/d22.py): bitwise operations (**R**) and using [xorshift](https://en.wikipedia.org/wiki/Xorshift) to generate pseudorandom numbers (**L**)
* [Day 23 Python](23/d23.py): [clique problem](https://en.wikipedia.org/wiki/Clique_problem) (**L**) and networkx (**I**)
* [Day 24 Python](24/d24.py): logic gates (**R**), adders (**I**) and ripple-carry adders (**L**), graphviz (**I**)
* [Day 25 Python](25/d25.py): list comprehensions (**R**) and itertools.product (**R**)