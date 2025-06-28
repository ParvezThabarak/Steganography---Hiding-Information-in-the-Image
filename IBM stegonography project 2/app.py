import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
import cv2
from stegano_utils import (
    encrypt_message, decrypt_message, embed_data_into_image, extract_data_from_image, allowed_file, load_image, save_image, max_data_capacity, prepend_length, extract_length
)

UPLOAD_FOLDER = 'static/uploads'
ENCRYPTED_FOLDER = 'static/encrypted'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENCRYPTED_FOLDER'] = ENCRYPTED_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files['image']
    message = request.form.get('message')
    key = request.form.get('key')

    if file.filename == '' or not message or not key:
        flash("Missing inputs")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex[:8]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + '_' + filename)
        file.save(filepath)

        image = load_image(filepath)
        encrypted = encrypt_message(message, key)
        data_to_embed = prepend_length(encrypted)
        if len(data_to_embed) * 8 > image.size:
            flash("Message too large for this image. Try a larger image or shorter message.")
            return redirect(url_for('index'))
        try:
            encoded_image = embed_data_into_image(image, data_to_embed)
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('index'))
        output_filename = unique_id + '_encrypted.png'
        output_path = os.path.join(app.config['ENCRYPTED_FOLDER'], output_filename)
        save_image(output_path, encoded_image)
        return render_template('result.html', image_url='static/encrypted/' + output_filename)
    else:
        flash("Invalid file")
        return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'image' not in request.files:
        flash("No file part")
        return redirect(url_for('index'))
    file = request.files['image']
    key = request.form.get('key')

    if file.filename == '' or not key:
        flash("Missing inputs")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_id = uuid.uuid4().hex[:8]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_id + '_' + filename)
        file.save(filepath)
        image = load_image(filepath)
        # Extract enough bytes for a large message (e.g., 4096 bytes)
        try:
            raw_data = extract_data_from_image(image, data_len=4096)
            msg_len, encrypted_data = extract_length(raw_data)
            encrypted_data = encrypted_data[:msg_len]
            decrypted = decrypt_message(encrypted_data, key)
        except Exception as e:
            flash(f"Error during decryption: {str(e)}")
            return redirect(url_for('index'))
        return render_template('decrypted.html', message=decrypted)
    flash("Invalid file")
    return redirect(url_for('index'))

@app.route('/static/encrypted/<filename>')
def encrypted_file(filename):
    return send_from_directory(app.config['ENCRYPTED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) 