document.getElementById('thriftForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Form submitted!');
});

document.getElementById('color').addEventListener('input', function() {
    const color = this.value;
    document.getElementById('colorDisplay').style.backgroundColor = color;
});

function previewForm() {
    alert('Preview the form details!');
}
