import sys
import operator
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for key in self.domains:
            length = key.length
            for word in self.domains[key].copy():
                if len(word) != length:
                    self.domains[key].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        modified = 0
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        else:
            i, j = overlap
            for xword in self.domains[x].copy():
                if not any(xword[i] == yword[j] for yword in self.domains[y].copy()):
                    modified = 1
                    self.domains[x].remove(xword)
        if modified:
            return True
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list(self.crossword.overlaps.keys())
        while arcs:
            node_pair = arcs[0]
            arcs.remove(node_pair)
            x, y = node_pair
            # Make node x consistent with node y
            modified = self.revise(x, y)
            if modified:
                # If there is no value for any x in y
                if not self.domains[x]:
                    return False
                # Nodes which were consistent with x, now would not be
                # Make them arc consistent
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # print(assignment)
        if len(assignment) == len(self.domains):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherise.
        """
        if len(set(assignment.values())) != len(assignment.values()):
            return False
        for variable in assignment.keys():
            length = variable.length
            if length != len(assignment[variable]):
                return False
            neighbours = self.crossword.neighbors(variable)
            for neighbour in neighbours:
                modified = self.revise(variable, neighbour)
                if modified:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain_dict = dict()
        neighbours = self.crossword.neighbors(var)
        xdomain = self.domains[var]
        for value in xdomain:
            count = 0
            for neighbour in neighbours:
                # If it is not assigned
                if neighbour not in assignment:
                    neighbour_domain = self.domains[neighbour]
                    if value in neighbour_domain:
                        count += 1
            domain_dict[value] = count

        domain_dict = dict(
            sorted(domain_dict.items(), key=operator.itemgetter(1)))
        return list(domain_dict.keys())

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        node_dict = {}
        for node in self.domains.keys():
            if node not in assignment:
                node_dict[node] = len(self.domains[node])
        node_dict = dict(sorted(node_dict.items(), key=operator.itemgetter(1)))

        val = list(node_dict.keys())
        var = val[0]
        if len(val)>1 and node_dict[val[0]] == node_dict[val[1]]:
            var = val[0] if len(self.crossword.neighbors(val[0])) > len(
                self.crossword.neighbors(val[1])) else val[1]
        return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        # print(assignment,var,self.order_domain_values(var,assignment))
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                connected_nodes = [(var,n) for n in self.crossword.neighbors(var)]
                inference = self.ac3(connected_nodes)
                if inference:
                    assignment[var] = value
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
