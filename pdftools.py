from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfWriter, PdfReader
from werkzeug.utils import secure_filename
from waitress import serve
import socket
import uuid
import os
import time

app = Flask(__name__)
tempdir=app.config['UPLOAD_FOLDER'] = 'temp'

# Define the maximum lifetime of a temporary file in seconds
MAX_LIFETIME = 120  # 2 min


@app.route('/')
def index():
    return render_template('index.html')

def process_pdf(processing_function):
    if 'pdf_file' not in request.files:
        return "ไม่มีไฟล์"

    file = request.files['pdf_file']

    if file.filename == '':
        return "ไม่ได้เลือกไฟล์"

    if file:
        temp_filename = os.path.join(tempdir, str(uuid.uuid4()) + "-" + secure_filename(file.filename))
        file.save(temp_filename)

        reader = PdfReader(temp_filename)
        writer = PdfWriter()

        processing_function(reader, writer)

        output_filename = os.path.join(tempdir, 'output-' + secure_filename(file.filename))
        with open(output_filename, "wb") as fp:
            writer.write(fp)

        # Attempt to send the file to the client
        try:
            return send_file(output_filename, as_attachment=True)
        finally:
            try:
                os.remove(temp_filename)
                print(f"Temporary file '{temp_filename}' successfully removed.")
            except Exception as e:
                print(f"Error occurred while removing temporary file '{temp_filename}': {str(e)}")




@app.route('/rotate', methods=['POST'])
def rotate_pages():
    def rotate_function(reader, writer):
        page_numbers_input = request.form['page_numbers']
        degrees_input = request.form['degrees']

        # Use default values if form values are not provided
        page_numbers = list(map(int, page_numbers_input.split(',')))
        degrees = list(map(int, degrees_input.split(',')))
        
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            if i + 1 in page_numbers:
                page.rotate(degrees[page_numbers.index(i + 1)])
            writer.add_page(page)

    return process_pdf(rotate_function)


@app.route('/split', methods=['POST'])
def split_pages():
    def split_function(reader, writer):
        start_page_input = request.form['start_page']
        end_page_input = request.form['end_page']

        start_page = int(start_page_input)
        end_page = int(end_page_input)

        for page_num in range(start_page - 1, end_page):
            page = reader.pages[page_num]
            writer.add_page(page)

    return process_pdf(split_function)


def cleanup_temp_files():
    
    current_time = time.time()
    
    for file_name in os.listdir(tempdir):
        file_path = os.path.join(tempdir, file_name)
        file_age = current_time - os.path.getctime(file_path)

        if file_age > MAX_LIFETIME:
            try:
                os.remove(file_path)
                print("Removed expired file: %s", file_path)
            except Exception as e:
                print("Error removing file: %s", e)




def ensure_temp_directory_exists():

    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
        

# Run the cleanup function periodically
@app.before_request
def run_cleanup():
    cleanup_temp_files()


def start_server():

    host = socket.gethostbyname(socket.gethostname())
    port = int(os.environ.get('PORT', 83))

    ensure_temp_directory_exists()

    print(f"Starting server on http://{host}:{port}")

    serve(app, host=host, port=port)

if __name__ == '__main__':
    start_server()
