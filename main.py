from fastapi import FastAPI
from pydantic import BaseModel
from model import Model
from cache import Cache
from typing import List

app = FastAPI()

model = Model()
cache = Cache()


class CompareData(BaseModel):
    originals: List[str]
    targets: List[str]


class Result(BaseModel):
    original: str
    target: str
    similarity: float


def get_vector(text):
    vector = cache.get(text)
    if not vector:
        vector = model.encode(text)
        cache.set(text, vector)
    else:
        cache.touch(text)

    return vector

@app.post("/compare")
def compare(data: CompareData):
    originals = data.originals
    targets = data.targets

    results = []
    combinations = [(original, target) for original in originals for target in targets]

    for original, target in combinations:
        original_vector = get_vector(original)
        target_vector = get_vector(target)
        similarity = model.similarity(original_vector, target_vector)
        results.append(Result(original=original, target=target, similarity=similarity))

    sorted_results = sorted(results, key=lambda x: x.similarity, reverse=True)

    return sorted_results


@app.get("/info")
def info():
    return cache.info()
