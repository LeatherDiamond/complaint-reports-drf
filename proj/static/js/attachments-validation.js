document.addEventListener('DOMContentLoaded', function () {
    const attachmentsInput = document.getElementById('attachments');
    const fileList = document.getElementById('file-list');
    const files = new DataTransfer();
    const errorContainer = document.querySelector('.attachment-error-container');
    const maxFiles = 10;
    const maxSize = 24 * 1024 * 1024;
    const allowedExtensions = ['png', 'jpg', 'pdf'];

    function displayError(message) {
        if (errorContainer) {
            errorContainer.innerHTML = `<p class="attachment-error">${message}</p>`;
            errorContainer.classList.add('error-pulse');
            setTimeout(function() {
                errorContainer.classList.remove('error-pulse');
            }, 1000); 
        }
    }

    function clearError() {
        if (errorContainer) {
            errorContainer.innerHTML = '';
        }
    }

    function truncateFileName(fileName, maxLength = 20) {
        if (fileName.length > maxLength) {
            const extension = fileName.split('.').pop();
            return `${fileName.substring(0, maxLength - extension.length - 3)}...${extension}`;
        }
        return fileName;
    }

    function validateFiles() {
        clearError();
        let totalSize = 0;
        const fileNames = new Set();

        for (let i = 0; i < files.items.length; i++) {
            const file = files.items[i].getAsFile();
            const extension = file.name.split('.').pop().toLowerCase();

            // Check allowed extensions
            if (!allowedExtensions.includes(extension)) {
                const truncatedFileName = truncateFileName(file.name);
                displayError(messages.invalid_extension.replace('{file_name}', truncatedFileName).replace('{extensions}', allowedExtensions.join(', ')));
                return false;
            }

            // Check for duplicate files
            if (fileNames.has(file.name)) {
                const truncatedFileName = truncateFileName(file.name);
                displayError(messages.file_already_added.replace('{file_name}', truncatedFileName));
                return false;
            }

            fileNames.add(file.name);
            totalSize += file.size;
        }

        if (files.items.length > maxFiles) {
            displayError(messages.max_files_exceeded);
            return false;
        }

        if (totalSize > maxSize) {
            displayError(messages.max_size_exceeded);
            return false;
        }

        return true;
    }

    attachmentsInput.addEventListener('change', function () {
        for (let i = 0; i < attachmentsInput.files.length; i++) {
            const file = attachmentsInput.files[i];

            // Check if file already added
            let alreadyExists = false;
            for (let j = 0; j < files.items.length; j++) {if (files.items[j].getAsFile().name === file.name) {
                    alreadyExists = true;
                    break;
                }
            }
            if (alreadyExists) {
                continue;
            }

            files.items.add(file);
            const truncatedFileName = truncateFileName(file.name);
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');
            fileItem.innerHTML = `<span>${truncatedFileName}</span><button type="button"> X </button>`;
            fileList.appendChild(fileItem);

            fileItem.querySelector('button').addEventListener('click', function () {
                for (let j = 0; j < files.items.length; j++) {
                    if (files.items[j].getAsFile() === file) {
                        files.items.remove(j);
                        break;
                    }
                }
                fileItem.remove();
                attachmentsInput.files = files.files;
                validateFiles();
            });
        }
        attachmentsInput.files = files.files;
        validateFiles();
    });

    const form = attachmentsInput.closest('form');
    if (form) {
        form.addEventListener('submit', function (event) {if (!validateFiles()) {
            event.preventDefault();
        }
    });
}
});