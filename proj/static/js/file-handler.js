document.addEventListener('DOMContentLoaded', function () {
    const attachmentsInput = document.getElementById('attachments');
    const fileList = document.getElementById('file-list');
    const files = new DataTransfer();

    attachmentsInput.addEventListener('change', function () {
        for (let i = 0; i < attachmentsInput.files.length; i++) {
            const file = attachmentsInput.files[i];

            // Check if file already added
            let alreadyExists = false;
            for (let j = 0; j < files.items.length; j++) {
                if (files.items[j].getAsFile().name === file.name) {
                    alreadyExists = true;
                    break;
                }
            }
            if (alreadyExists) {
                continue;
            }

            files.items.add(file);
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');
            fileItem.innerHTML = `<span>${file.name}</span><button type="button"> X </button>`;
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
            });
        }
        attachmentsInput.files = files.files;
    });
});