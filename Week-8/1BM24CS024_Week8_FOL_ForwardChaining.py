
def parse_atom(atom):
    name, args = atom.strip().split("(", 1)
    args = args.rstrip(")")
    return name.strip(), [x.strip() for x in args.split(",")]


def unify(pattern, fact, substitution):
    if pattern[0] != fact[0] or len(pattern[1]) != len(fact[1]):
        return None

    sub = substitution.copy()

    for p, f in zip(pattern[1], fact[1]):
        if p[0].islower():
            if p in sub and sub[p] != f:
                return None
            sub[p] = f
        elif p != f:
            return None

    return sub


def find_matches(conditions, facts, substitution=None):
    if substitution is None:
        substitution = {}

    if not conditions:
        yield substitution
        return

    condition = conditions[0]

    for fact in facts:
        result = unify(condition, fact, substitution)

        if result is not None:
            yield from find_matches(
                conditions[1:], facts, result
            )


def apply_substitution(atom, substitution):
    name, args = atom
    args = [substitution.get(a, a) for a in args]
    return name + "(" + ",".join(args) + ")"


def forward_chaining(facts, rules, query):

    known = set(facts)
    iteration = 1

    print("\n========== INITIAL KNOWLEDGE BASE ==========")

    for fact in facts:
        print(fact)

    print("\n========== FORWARD CHAINING ==========")

    while True:
        new_facts = []

        print(f"\n---------- ITERATION {iteration} ----------")

        for i, (conditions, conclusion) in enumerate(rules, 1):

            for sub in find_matches(
                conditions,
                [parse_atom(f) for f in known]
            ):

                result = apply_substitution(conclusion, sub)

                if result not in known and result not in new_facts:

                    print(f"\nRule {i} applied")
                    print("Substitution:", sub)

                    print("Matched facts:")
                    for condition in conditions:
                        print(" ", apply_substitution(condition, sub))

                    print("Conclusion:", result)

                    new_facts.append(result)

        if not new_facts:
            print("\nNo new facts can be inferred.")
            break

        print("\nNew facts added to KB:")

        for fact in new_facts:
            print(" +", fact)
            known.add(fact)

        iteration += 1

    print("\n========== FINAL KNOWLEDGE BASE ==========")

    for fact in sorted(known):
        print(fact)

    print("\n========== QUERY RESULT ==========")
    print("Query:", query)

    if query in known:
        print("SUCCESS: Query proved using Forward Chaining.")
    else:
        print("FAILURE: Query cannot be proved.")


# MAIN PROGRAM

print("FIRST ORDER LOGIC - FORWARD CHAINING")

n = int(input("\nEnter number of initial facts: "))

facts = []

for i in range(n):
    facts.append(input(f"Enter fact {i+1}: "))

r = int(input("\nEnter number of rules: "))

rules = []

for i in range(r):

    print(f"\nRule {i+1}")

    rule = input("Enter rule (A(x) & B(x) -> C(x)): ")

    left, right = rule.split("->")

    conditions = [
        parse_atom(x) for x in left.split("&")
    ]

    conclusion = parse_atom(right.strip())

    rules.append((conditions, conclusion))

query = input("\nEnter query: ")

forward_chaining(facts, rules, query)
