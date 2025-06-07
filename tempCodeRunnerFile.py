from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


# Read Excel once at startup
df = pd.read_excel("tribal_language project .xlsx", engine='openpyxl')
df.columns = df.columns.str.strip()  # Column strip for safety



@app.route("/", methods=["GET", "POST"])
@app.route("/suggest")
def suggest():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])

    suggestions = df[df['hindi'].str.startswith(query, na=False)]['hindi'].unique()[:5]
    return jsonify(list(suggestions))

def index():
    output = {}
    if request.method == "POST":
        hindi_input = request.form["hindi_text"]
        result = df[df['hindi'].str.strip() == hindi_input.strip()]
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

from flask import jsonify




if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
