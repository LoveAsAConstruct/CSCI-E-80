import sys

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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        # Iterated through each word for each node and removes the word from the nodes domain if lengths don't match
        for node in self.domains:
            for word in self.crossword.words:
                if len(word) != node.length:
                    self.domains[node].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        overlap = self.crossword.overlaps[x,y]
        if overlap == None:
            # If we have no overlap, we need no revision
            return revision
        
        for node in self.domains[x].copy():
            fufills = False
            for node2 in self.domains[y].copy():
                if node[overlap[0]] == node2[overlap[1]]:
                    # There is a node that fuffils the current state
                    fufills = True
                    break
            if not fufills:
                # There are no nodes fitting this state, so this state is pruned
                self.domains[x].remove(node)
                revision = True
        # Return whether we have revised the node
        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is none, set arcs to all overlaps in crossword
        if arcs == None:
            arcs = set()
            for overlap in self.crossword.overlaps:
                arcs.add((overlap[0], overlap[1]))

        # Arcs variable is treated as execution queue
        while len(arcs) > 0:
            for arc in arcs.copy():
                arcs.remove(arc)
                # Check if we are revising for consistency
                if self.revise(arc[0], arc[1]):
                    if(len(self.domains[arc[0]])<= 0):
                        # If no possibilities left in domain, return false
                        return False
                    else:
                        for var in self.crossword.variables:
                            if var == arc[0]:
                                # Prevent checking against self
                                continue
                            # Add overlap if adjecent overlaps possible
                            elif self.crossword.overlaps[var, arc[0]] or self.crossword.overlaps[arc[0], var]:
                                arcs.add((var, arc[0]))
        return True
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Return false if a variable doesn't have an assignent
        for var in self.crossword.variables:
            if assignment.get(var) is None:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for key in assignment.keys():
            if key.length != len(assignment[key]):
                # Return false if word length doesn't fit
                return False
            for key2 in assignment.keys():
                if key == key2:
                    continue
                overlap = self.crossword.overlaps[key,key2]
                if overlap:
                    if assignment[key][overlap[0]] != assignment[key2][overlap[1]]:
                        # Return false if word overlap doesn't fit
                        return False
        return True
    
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Identify neighboring variables that are not yet assigned and overlap with `var`
        neighbors = {
            var2 for var2 in self.crossword.variables
            if var2 != var and var2 not in assignment and (var, var2) in self.crossword.overlaps
        }

        # Count how many arcs are ruled out by a value
        def count_ruled_out(value):
            total_ruled_out = 0
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap:
                    i, j = overlap
                    ruled_out = sum(
                        1 for neighbor_value in self.domains[neighbor]
                        if value[i] != neighbor_value[j]
                    )
                    total_ruled_out += ruled_out
            return total_ruled_out

        # Create a list of tuples for sorting, and sort based on list
        values_with_counts = [(value, count_ruled_out(value)) for value in self.domains[var]]
        sorted_values = sorted(values_with_counts, key=lambda x: x[1])

        # Return sorted values
        return [value for value, _ in sorted_values]

    
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = self.crossword.variables - assignment.keys()

        # First, sort by the number of remaining values in the domain, then by the degree (number of neighbors)
        sorted_vars = sorted(unassigned_variables, key=lambda var: (len(self.domains[var]), -len(self.get_neighbors(var))))

        # Return the variable with the minimum number of remaining values and maximum degree
        return sorted_vars[0]

    def get_neighbors(self, var):
        # Get neighbors of a variable.
        return {neighbor for neighbor in self.crossword.variables if neighbor != var and self.crossword.overlaps[var, neighbor]}




    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        """if not self.ac3(): 
            return None
        else:
            for variable in self.domains:
                assignment.update({variable: list(self.domains[variable])[0]})
        return assignment"""
        while not self.assignment_complete(assignment):
            self.select_unassigned_variable()



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
