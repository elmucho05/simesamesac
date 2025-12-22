from flask import Flask, render_template, request
from wtforms import Form, IntegerField, SubmitField, validators
from prenotazione import *
# from colors_gcp import Colors
# versione completa
app = Flask(__name__, static_url_path="/static", static_folder="static")
booking = Prenotazione()
riep = RiepilogoGiorno()

class Colorform(Form):
    # eredita' e polimorfismo, in questo caso si chiama composizione
    # multiform mi da' delle classi che mi definiscono dei form
    # uso le classi di quei fild per dire "nel mio form ho 3 field interi e un tasto submit"
    red = IntegerField("Red", [validators.NumberRange(min=0, max=255)])
    green = IntegerField("Green", [validators.NumberRange(min=0, max=255)])
    blue = IntegerField("Blue", [validators.NumberRange(min=0, max=255)])
    submit = SubmitField("Submit")


@app.route("/room42/<date>", methods=["GET"])
def get_dettaglio(date):
    if request.method == "GET":
        dettaglio_giornata = riep.get_dettagli_giornata(date)
        if dettaglio_giornata is None:
            dettaglio_giornata = {"riunioni" : []}
        return render_template("dettaglio.html", date=date, dettaglio_giornata=dettaglio_giornata), 200
    return render_template("404.html", path=request.path), 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", path=request.path), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
