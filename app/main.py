from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Função para verificar extensões permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400

    file = request.files['file']
    
    # Se o arquivo não tiver nome
    if file.filename == '':
        return 'Nenhum arquivo selecionado', 400

    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Renderizar template com a imagem enviada
        return render_template('dashboard.html', uploaded_image=filename)

    return 'Tipo de arquivo não permitido', 400

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
