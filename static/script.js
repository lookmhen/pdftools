// Get reference to the drop area and the list element where file names will be displayed
const dropArea = document.getElementById('rotate-app');
const fileList = document.getElementById('split-app');

// Add event listeners for drag and drop events
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, e => {
    e.preventDefault(); // Prevent default behavior of the browser for these events
    e.stopPropagation(); // Stop the event from propagating further

    // Toggle 'drag-over' class based on the event type
    if (eventName === 'dragenter' || eventName === 'dragover') {
      dropArea.classList.add('drag-over');
    } else {
      dropArea.classList.remove('drag-over');
    }

    // If the event is 'drop', handle the dropped files
    if (eventName === 'drop') {
      handleFiles(e.dataTransfer.files); // Pass the dropped files to the handleFiles function
    }
  }, false);
});

// Add event listener for when files are selected through the file input element
document.getElementById('fileElem').addEventListener('change', function() {
  handleFiles(this.files); // Pass the selected files to the handleFiles function
});