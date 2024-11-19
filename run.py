
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding

# Constant values for testing purposes
NUM_TILES = 4
GRID_LENGTH = 3

"""
These should be treated as constant values. The loops populate them based on the values
of NUM_TILES and GRID_LENGTH
"""
TILES = []
for i in range(NUM_TILES):
    TILES.append(f't{i}')

print(TILES)

LOCATIONS = []

for row in range(GRID_LENGTH):
    for col in range(GRID_LENGTH):
        LOCATIONS.append(f"l_{row},{col}")

print(LOCATIONS)


@proposition(E)
class Location:
    def __init__(self, tile, location):
        # error checking. make sure the tiles are valid
        assert tile in TILES
        assert location in LOCATIONS

        # init values
        self.tile = tile
        self.location = location

    def _prop_name(self):
        return f"tile({self.tile}) @ loc{self.location}"


@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created.

    print("hello world")
    for t in TILES:
        possible_locations = []

        # For each tile, determines every possible location for it (25x25 tiles for each)
        for loc in LOCATIONS:
            possible_locations.append(Location(t, loc))

        # Ensures that only one of these holds
        constraint.add_exactly_one(E, possible_locations)

    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
