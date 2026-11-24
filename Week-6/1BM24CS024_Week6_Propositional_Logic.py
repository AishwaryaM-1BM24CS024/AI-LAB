
from itertools import product
import ast

def evaluate(node, model):
    if isinstance(node, ast.Name):
        return model[node.id]

    elif isinstance(node, ast.BoolOp):
        values = [evaluate(v, model) for v in node.values]

        if isinstance(node.op, ast.And):
            return all(values)
        if isinstance(node.op, ast.Or):
            return any(values)

    elif isinstance(node, ast.UnaryOp):
        return not evaluate(node.operand, model)

    elif isinstance(node, ast.Call):
        p = evaluate(node.args[0], model)
        q = evaluate(node.args[1], model)
        return (not p) or q

    raise ValueError("Invalid expression")


def get_symbols(expressions):
    symbols = set()

    for expr in expressions:
        tree = ast.parse(expr, mode="eval")

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id != "implies":
                symbols.add(node.id)

    return sorted(symbols)


def truth_table_entailment(kb, query):

    symbols = get_symbols(kb + [query])

    print("\nKNOWLEDGE BASE (KB)")
    for i, sentence in enumerate(kb, 1):
        print(f"{i}. {sentence}")

    print("\nQUERY:", query)

    print("\nTRUTH TABLE")

    headers = symbols + ["KB", "Query"]
    print(" | ".join(f"{h:^8}" for h in headers))
    print("-" * (len(headers) * 11))

    entails = True
    count = 0

    for values in product([True, False], repeat=len(symbols)):

        model = dict(zip(symbols, values))

        kb_values = [
            evaluate(ast.parse(e, mode="eval").body, model)
            for e in kb
        ]

        kb_true = all(kb_values)

        query_value = evaluate(
            ast.parse(query, mode="eval").body, model
        )

        row = [str(v) for v in values]
        row += [str(kb_true), str(query_value)]

        print(" | ".join(f"{v:^8}" for v in row))

        if kb_true:
            count += 1
            if not query_value:
                entails = False

    print("\nRESULT")
    print("Number of models satisfying KB:", count)

    if entails:
        print("KB entails the query.")
    else:
        print("KB does not entail the query.")


# MAIN PROGRAM

print("PROPOSITIONAL LOGIC - TRUTH TABLE ENUMERATION")

n = int(input("\nEnter number of KB sentences: "))

kb = []

for i in range(n):
    sentence = input(f"Enter KB sentence {i+1}: ")
    kb.append(sentence)

query = input("\nEnter query: ")

truth_table_entailment(kb, query)
