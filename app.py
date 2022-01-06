import os
from flask import Flask, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.config['FILES_DIRECTORY'] = './'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.png', '.gif']

@app.errorhandler(413)
def too_large(e):
    return {"message": "Arquivo maior que 1MB"}, 413

@app.post('/uploads')
def post_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            return {"message": "Extensão não suportada"}, 415
        if filename in os.listdir(app.config['FILES_DIRECTORY'] + file_ext):
            return {"message": "Nome de arquivo ja existente "}, 409
    file.save(os.path.join(app.config['FILES_DIRECTORY'] + file_ext, filename))
    file.save(os.path.join(app.config['FILES_DIRECTORY'] + "files", filename))
    return {"message": "Upload realizado com sucesso!"}, 201

@app.get("/files")
def list_files():
    return{"files": os.listdir(app.config['FILES_DIRECTORY'] + "files")}, 200

@app.get("/files/<ext>")
def list(ext):
    file_ext = "." + ext
    if file_ext not in app.config['ALLOWED_EXTENSIONS']:
            return {"message": "Formato de arquivo não permitido pelo sistema"}, 404
    return{"files": os.listdir(app.config['FILES_DIRECTORY'] + "." + ext)}, 200

@app.errorhandler(404)
def too_large(e):
    return {"message": "Nome de arquivo inválido"}, 404

@app.get("/download/<filename>")
def download(filename):
    return send_from_directory("./files", filename, as_attachment=True), 200

@app.errorhandler(500)
def too_large(e):
    return {"message": "Arquivo não existente"}, 404

@app.get("/download-zip/<query_param>")
def download_zip(query_param):
    return send_file(shutil.make_archive('./.' + query_param, 'zip', './.' + query_param )), 200