// Get reference to the drop area and the list element where file names will be displayed
const dropAreas = document.querySelectorAll('.drop-area');

dropAreas.forEach(dropArea => {
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
        const files = e.dataTransfer.files;
        handleFiles(files, dropArea); // Pass the dropped files and drop area to the handleFiles function
      }
    }, false);
  });
});

// Function to handle dropped files
function handleFiles(files, dropArea) {
  const input = dropArea.querySelector('input[type="file"]');
  input.files = files; // Set dropped files to the input element
}

// Add event listener for when files are selected through the file input element
document.querySelectorAll('input[type="file"]').forEach(input => {
  input.addEventListener('change', function() {
    const dropArea = this.closest('.drop-area');
    handleFiles(this.files, dropArea); // Pass the selected files and drop area to the handleFiles function
  });
});
