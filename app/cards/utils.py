def print_matrix(matrix: list[list]) -> None:
    for row in matrix:
        print(row)

import pickle
def write_obj(id, obj) -> None:
    with open(f"{id}", "wb") as f:
        pickle.dump(obj, f)

def load_obj(id):
    try:
        with open(f"{id}", "rb") as f:
            obj = pickle.load(f)
        return obj
    except (EOFError, FileNotFoundError):
        return