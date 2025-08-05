from flask import Flask, render_template, request
import pandas as pd
from flask import jsonify
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

# Excel file load karna (sirf ek baar)
df = pd.read_excel("tribal_language project 2.xlsx", engine='openpyxl')
df.columns = df.columns.str.strip()  # Extra space hata diye column names se

@app.route("/", methods=["GET", "POST"])
def index():
    output = {}
    if request.method == "POST":
        hindi_input = request.form["hindi_text"]

        # Hinglish to Hindi conversion
        converted_input = transliterate(hindi_input, sanscript.ITRANS, sanscript.DEVANAGARI)

        # Translation dhoondhna
        result = df[df['hindi'].str.strip() == converted_input.strip()]
        if not result.empty:
            output = {
                "eng": result.iloc[0]["eng"],
                "pardhi": result.iloc[0]["pardhi"],
                "kolami": result.iloc[0]["kolami"]
            }
        else:
            output = {
                "eng": "No match found",
                "pardhi": "No match found",
                "kolami": "No match found"
            }
    return render_template("index.html", output=output)

# if __name__ == "__main__":
#     app.run(debug=True)

# autocomplete
@app.route("/suggest")
def suggest():
    query = request.args.get("q", "")
    if not query:
        return []
    suggestions = df[df["hindi"].str.startswith(query, na=False)]["hindi"].unique()[:5]
    return jsonify(list(suggestions))

# end autocomplet

if __name__ == "__main__":
    app.run(debug=True)
