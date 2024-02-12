from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfWriter, PdfReader
from werkzeug.utils import secure_filename

app = Flask(__name__)

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
        filename = secure_filename(file.filename)
        file.save(filename)

        reader = PdfReader(filename)
        writer = PdfWriter()

        # Process the PDF using the provided processing_function
        processing_function(reader, writer)

        output_filename = 'output-' + filename
        with open(output_filename, "wb") as fp:
            writer.write(fp)

        return send_file(output_filename, as_attachment=True)

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

if __name__ == '__main__':
    app.run(debug=True)
