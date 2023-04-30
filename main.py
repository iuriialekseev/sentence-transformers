from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L12-v2')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

app = Flask(__name__)


@app.route('/compare', methods=['POST'])
def compare_sentences():
    data = request.get_json()

    # Embed the sentence into a vector
    sentence = data['sentence']
    example = data['example']

    sentence_vector = model.encode(sentence, convert_to_tensor=True)
    example_vector = model.encode(example, convert_to_tensor=True)

    score = util.cos_sim(sentence_vector, example_vector).item()

    return jsonify(round(score, 3))

@app.route('/embed', methods=['POST'])
def embed_sentence():
    data = request.get_json()

    # Embed the sentence into a vector
    sentence = data['sentence']
    model = data['model']

    sentence_vector = model.encode(sentence, convert_to_tensor=True)

    return jsonify(sentence_vector)

if __name__ == '__main__':
    app.run(debug=True)
