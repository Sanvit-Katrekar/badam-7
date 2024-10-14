from app import redis_db
import pickle

def print_matrix(matrix: list[list]) -> None:
    for row in matrix:
        print(row)

def write_obj(id: str, obj) -> None:
    '''
    with open(f"{id}", "wb") as f:
        pickle.dump(obj, f)
    '''
    redis_db.set(id, pickle.dumps(obj))

def load_obj(id):
    '''
    try:
        with open(f"{id}", "rb") as f:
            obj = pickle.load(f)
        return obj
    except (EOFError, FileNotFoundError):
        return
    '''
    redis_resp = redis_db.get(id)
    if redis_resp is None:
        return redis_resp
    return pickle.loads(redis_resp)