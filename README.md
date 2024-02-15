PDF Rotate & Split Flask App 📄

This Flask application enables users to upload PDF files for rotation or splitting of pages, leveraging the PyPDF2 library for PDF manipulation and Flask for the web interface.
Setup 🛠

Ensure Flask and PyPDF2 are installed in your environment. Use pip for installation:

bash

pip install Flask PyPDF2

Features 🌟

    Upload PDF: Users can upload a PDF file for processing.
    Rotate Pages: Allows the rotation of specified pages by degrees.
    Split PDF: Enables splitting the PDF into a new document from selected page ranges.

Running the App 🚀

    Start the Flask application by running it from your terminal or command prompt.
    Open a web browser and navigate to the application URL, typically http://127.0.0.1:5000/, to access the web interface.
    Use the web interface to upload a PDF file and choose the desired operation: rotate or split.

Rotate Pages

    Specify the page numbers and the degree of rotation (90, 180, 270) for each page.
    Submit the form to process the rotation.
    Download the rotated PDF file once processed.

Split PDF

    Enter the start and end page numbers to define the range of pages to split.
    Submit the form to initiate the splitting process.
    Download the new PDF file containing the specified range of pages.

Conclusion 🎉

This application simplifies PDF manipulation tasks, such as rotating and splitting pages, through a user-friendly web interface. Enjoy managing your PDF files with ease!
