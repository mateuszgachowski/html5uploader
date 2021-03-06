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
	# files sent as FILES list
	if request.files.getlist('\'upload\''):
	    file = request.files.getlist('\'upload\'')[0]
	    if file:
		#remove ' and ' from filename
		filename = file.filename.replace('\'', '')
		file.save(os.path.join(save_path, filename))
	    else:
		return jsonify({'success': False, 'error': 'Extension not suported'})
		
	# support send image in headers
	if request.args.get('up') and not request.files:
	    if request.args.get('base64') and request.args['base64'] == 'true':
		content = base64.b64decode(request.data) # b64
	    else:
		content = request.data

	    # fix bug in some browsers - headers must be uppercase
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
	
# files serving method
@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(save_path, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)