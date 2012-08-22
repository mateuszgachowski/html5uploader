# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, url_for, jsonify, send_from_directory
import base64
import os

app = Flask(__name__)
save_path = 'uploads'

#main method rendering html
@app.route('/')
def index():
    return render_template('index.html')

#html5uploader method, do all the magic
@app.route('/upload', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
	filename = None
	if request.files and request.files.getlist('\'upload\''):
	    file = request.files.getlist('\'upload\'')[0]
	    
	    # check here file extenstion
	    if file:
		#remove ' and ' from filename
		filename = file.filename.replace('\'', '')
		file.save(os.path.join(save_path, filename))
	    else:
		return jsonify({'success': False, 'error': 'Extension not suported'})
	    
	if request.args.get('up') and not request.files:
	    if 'base64' in request.args and request.args['base64'] == 'true':
		content = base64.b64decode(request.data) # b64
	    else:
		content = request.data

	    headers = {k.upper(): v for k, v in request.headers}
		
	    filename = headers.get('UP-FILENAME')
	    path = os.path.join(save_path, filename)
	    
	    if filename:
		f = open(path, 'w')
		f.write(content)
		f.close()
	    else:
		return jsonify({'success': False, 'error': 'Image file not supported'})
	return jsonify({'success': True, 'path': url_for('uploads', filename=filename), 'filename': filename})
	
@app.route('/uploads/<filename>')
def uploads(filename):
    if filename:
	return send_from_directory(save_path, filename)
    else:
	return None

if __name__ == "__main__":
    app.run(debug=True, port=5000)