from sgnlp.models.sentic_gcn import(
    SenticGCNConfig,
    SenticGCNModel,
    SenticGCNEmbeddingConfig,
    SenticGCNEmbeddingModel,
    SenticGCNTokenizer,
    SenticGCNPreprocessor,
    SenticGCNPostprocessor,
    download_tokenizer_files,
)
from flask import Flask, render_template, request

# Loading up the files, pretrained models, etc.
download_tokenizer_files(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_tokenizer/",
    "senticgcn_tokenizer")

tokenizer = SenticGCNTokenizer.from_pretrained("senticgcn_tokenizer")

config = "C:/Users/rites/OneDrive/Documents/Python/AISingapore/models/config.json"

model = SenticGCNModel.from_pretrained(
    "C:/Users/rites/OneDrive/Documents/Python/AISingapore/models/pytorch_model.bin",
    config=config
)

embed_config = SenticGCNEmbeddingConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/config.json"
)

embed_model = SenticGCNEmbeddingModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticgcn_embedding_model/pytorch_model.bin",
    config=embed_config
)


preprocessor = SenticGCNPreprocessor(
    tokenizer=tokenizer, embedding_model=embed_model,
    senticnet="https://storage.googleapis.com/sgnlp/models/sentic_gcn/senticnet.pickle",
    device="cpu")

postprocessor = SenticGCNPostprocessor()

def prediction(usr_input, aspects):

    inputs = [
        {
        "aspects" : aspects,
        "sentence" : usr_input,
        }
        ]

    processed_inputs, processed_indices = preprocessor(inputs)
    raw_outputs = model(processed_indices)

    post_outputs = postprocessor(processed_inputs=processed_inputs, model_outputs=raw_outputs)

    for output in post_outputs:
        out  = ""
        print(" ".join(output["sentence"]), end="  ")
        for z, aspect in enumerate(output["aspects"]):
            aspects = " ".join([output["sentence"][x] for x in aspect])
            result = ["Negative", "Neutral", "Positive"][output["labels"][z] + 1]
            print(result, end = " - ")
            if result == "Positive":
                out = "You did a great job today!"
            elif result == "Neutral":
                out = "Keep up the work!"
            else:
                out = "It's okay to feel that way, Let me get you help!"
        return out

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", out="")
    
@app.route("/", methods=["POST", "GET"])
def post():
    if request.method == "POST":
        usr_in = request.form["usr_in"].lower()
        print(usr_in)
        possible_aspects = []
        for a in ["i", "im", "feeling", "id", "ive"]:
            if any(x == a for x in usr_in.split()):
                possible_aspects.append(a)
        
        out = prediction(usr_in, possible_aspects)
        return render_template("home.html", out=out)
        
"""
processed_inputs, processed_indices = preprocessor(inputs)
raw_outputs = model(processed_indices)

post_outputs = postprocessor(processed_inputs=processed_inputs, model_outputs=raw_outputs)

for output in post_outputs:
    print(" ".join(output["sentence"]), end="  ")
    for z, aspect in enumerate(output["aspects"]):
        aspects = " ".join([output["sentence"][x] for x in aspect])
        result = ["Negative", "Neutral", "Positive"][output["labels"][z] + 1]
        print(result, end = " - ")
        if result == "Positive":
            print("You did a great job today!")
        elif result == "Neutral":
            print("Keep up the work!")
        else:
            print("It's okay to feel that way, Let me get you help!")
"""

if __name__ == "__main__":
    app.run(debug=True)