from flask import Flask, render_template, request, jsonify
import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

# Excel file load karna (sirf ek baar)
df = pd.read_excel("tribal_language project 2.xlsx", engine='openpyxl')
df.columns = df.columns.str.strip()

# Cleaned hindi column for matching
df["hindi_cleaned"] = df["hindi"].astype(str).str.strip().str.replace(" ", "").str.lower()

# Safe transliteration function
def safe_transliterate(text):
    try:
        return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    except Exception as e:
        return ""

@app.route("/", methods=["GET", "POST"])
def index():
    output = {}
    if request.method == "POST":
        hindi_input = request.form["hindi_text"]
        converted_input = safe_transliterate(hindi_input)
        converted_cleaned = converted_input.strip().replace(" ", "").lower()

        result = df[df["hindi_cleaned"] == converted_cleaned]
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

@app.route("/suggest")
def suggest():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])

    hindi_query = safe_transliterate(query)
    hindi_query_cleaned = hindi_query.strip().replace(" ", "").lower()

    # Use contains instead of startswith for better matching
    suggestions = df[df["hindi_cleaned"].str.contains(hindi_query_cleaned, na=False)]["hindi"].unique()[:5]
    return jsonify(list(suggestions))
if __name__ == "__main__":
    app.run(debug=True)
