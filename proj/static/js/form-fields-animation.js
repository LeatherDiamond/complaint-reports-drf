document.addEventListener('DOMContentLoaded', function() {
    const formRows = document.querySelectorAll('.form-row');
    formRows.forEach((row, index) => {
        setTimeout(() => {
            row.classList.add('show');
        }, index * 100);
    });
});
