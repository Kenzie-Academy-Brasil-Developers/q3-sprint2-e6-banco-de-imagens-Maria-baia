import os
from flask import Flask, request, send_from_directory, send_file
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = eval(os.environ['MAX_CONTENT_LENGTH'])

@app.errorhandler(413)
def too_large(e):
    return {"message": "Arquivo maior que 1MB"}, 413

@app.post('/uploads')
def post_file():
    try:
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in os.environ.get('ALLOWED_EXTENSIONS'):
                return {"message": "Extensão não suportada"}, 415
            if filename in os.listdir(os.environ['FILES_DIRECTORY'] + file_ext):
                return {"message": "Nome de arquivo ja existente "}, 409
        file.save(os.path.join(os.environ['FILES_DIRECTORY'] + file_ext, filename))
        return {"message": "Upload realizado com sucesso!"}, 201
    except FileNotFoundError:
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        os.mkdir(os.environ['FILES_DIRECTORY'] + file_ext)
        if file_ext not in os.environ.get('ALLOWED_EXTENSIONS'):
                return {"message": "Extensão não suportada"}, 415
        file.save(os.path.join(os.environ['FILES_DIRECTORY'] + file_ext, filename))
        return {"message": "Upload realizado com sucesso!"}, 201


@app.get("/files")
def list_files():
    return{"files": os.listdir(os.environ['FILES_DIRECTORY'] + "files")}, 200

@app.get("/files/<ext>")
def list(ext):
    file_ext = "." + ext
    if file_ext not in os.environ['ALLOWED_EXTENSIONS']:
            return {"message": "Formato de arquivo não permitido pelo sistema"}, 404
    return{"files": os.listdir(os.environ['FILES_DIRECTORY'] + "." + ext)}, 200

@app.errorhandler(404)
def too_large(e):
    return {"message": "Nome de arquivo inválido"}, 404

@app.get("/download/<filename>")
def download(filename):
    file_ext = os.path.splitext(filename)[1]
    if filename in os.listdir(os.environ['FILES_DIRECTORY'] + file_ext):
        return send_from_directory(os.environ['FILES_DIRECTORY'] + file_ext, filename, as_attachment=True), 200

@app.get("/download-zip")
def download_zip():
    query_param = request.args.get('tipo')
    print(query_param)
    return send_file(shutil.make_archive(os.environ['FILES_DIRECTORY'] + query_param, 'zip', os.environ['FILES_DIRECTORY'] + query_param )), 200