document.addEventListener("DOMContentLoaded", function () {
    let fileInput = document.querySelector("#id_file_pdf");

    if (!fileInput) return;

    // Buat wrapper drag & drop
    let dropArea = document.createElement("div");
    dropArea.classList.add("drop-area");
    dropArea.innerHTML = `
        <p>Seret & Lepas file di sini atau <span class="browse-btn">Pilih File</span></p>
    `;

    // Sisipkan sebelum file input
    fileInput.style.display = "none"; // Sembunyikan input default
    fileInput.parentNode.insertBefore(dropArea, fileInput);

    // Klik area untuk membuka file picker
    dropArea.addEventListener("click", function () {
        fileInput.click();
    });

    // Efek Drag Over
    dropArea.addEventListener("dragover", function (event) {
        event.preventDefault();
        dropArea.classList.add("dragover");
    });

    dropArea.addEventListener("dragleave", function () {
        dropArea.classList.remove("dragover");
    });

    // Saat file di-drop
    dropArea.addEventListener("drop", function (event) {
        event.preventDefault();
        dropArea.classList.remove("dragover");

        let files = event.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            dropArea.innerHTML = `<p><strong>${files[0].name}</strong> siap diunggah</p>`;
        }
    });

    // Saat file dipilih lewat tombol
    fileInput.addEventListener("change", function () {
        if (fileInput.files.length > 0) {
            dropArea.innerHTML = `<p><strong>${fileInput.files[0].name}</strong> siap diunggah</p>`;
        }
    });
});
