from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/config")
def config():
    return render_template("config.html")


# Dentro do @app.route não escrever o nome da pagina e sim como no navegador ir acessar
@app.route("/analise")
def analise():
    return render_template("analise.html")


@app.route("/sobrenos")
def sobrenos():
    return render_template("sobrenos.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
