from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L12-v2")


class Model:
    def encode(self, text):
        return model.encode(text, convert_to_tensor=True).tolist()

    def similarity(self, a, b):
        return util.cos_sim(a, b).item()
