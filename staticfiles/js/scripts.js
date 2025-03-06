document.addEventListener("DOMContentLoaded", function () {
    let searchInput = document.querySelector("#navbar-search-form #search-input");
    let resultsContainer = document.querySelector("#navbar-search-form #search-results");

    if (!searchInput || !resultsContainer) {
        console.error("Elemen pencarian tidak ditemukan!");
        return;
    }

    searchInput.addEventListener("input", function() {
        let query = this.value.trim();

        if (query.length > 2) {
            fetch(`/cari/?q=${query}`, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = "";
                if (data.results.length > 0) {
                    data.results.forEach(item => {
                        let div = document.createElement("div");
                        div.classList.add("p-2", "border-b", "cursor-pointer", "hover:bg-gray-200");

                        div.innerHTML = `
                            <p class="font-semibold">${item.nama_peraturan}</p>
                            <p class="text-sm text-gray-500">${item.teks_pdf}...</p>
                            <div class="flex gap-2 mt-1">
                                <a href="${item.view_url}" target="_blank" class="text-blue-500 view-link">
                                    <i class="fas fa-eye"></i> View
                                </a>
                                <a href="${item.download_url}" class="text-green-500 download-link" download>
                                    <i class="fas fa-download"></i> Download
                                </a>
                            </div>
                        `;

                        // Mencegah redirect saat mengklik View atau Download
                        div.querySelector(".view-link").addEventListener("click", function(event) {
                            event.stopPropagation(); // Hentikan event bubbling
                        });

                        div.querySelector(".download-link").addEventListener("click", function(event) {
                            event.stopPropagation(); // Hentikan event bubbling
                        });

                        // Klik div untuk redirect ke halaman detail
                        div.addEventListener("click", function() {
                            window.location.href = item.view_url;
                        });

                        resultsContainer.appendChild(div);
                    });
                    resultsContainer.classList.remove("hidden");
                } else {
                    resultsContainer.classList.add("hidden");
                }
            })
            .catch(error => console.error("Error fetching search results:", error));
        } else {
            resultsContainer.classList.add("hidden");
        }
    });

    // Mencegah enter agar tidak mengirim form dan mengganti halaman
    searchInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
        }
    });
});


document.querySelectorAll('.read-more').forEach(button => {
    button.addEventListener('click', () => {
        const truncatedText = button.previousElementSibling; // Ambil teks yang dipersingkat
        const content = button.nextElementSibling; // Ambil teks lengkap

        truncatedText.classList.add('hidden'); // Sembunyikan teks yang dipersingkat
        content.classList.remove('hidden'); // Tampilkan teks lengkap
        button.classList.add('hidden'); // Sembunyikan tombol "Read more"
    });
});

document.addEventListener('click', (event) => {
    if (!event.target.classList.contains('read-more') && !event.target.closest('.read-more-content')) {
        document.querySelectorAll('.read-more-content').forEach(content => {
            if (!content.classList.contains('hidden')) {
                content.classList.add('hidden');
                const truncatedText = content.previousElementSibling.previousElementSibling;
                truncatedText.classList.remove('hidden'); // Tampilkan kembali teks yang dipersingkat
                content.previousElementSibling.classList.remove('hidden'); // Tampilkan kembali tombol "Read more"
            }
        });
    }
});



function toggleNavbarSubMenu(event, submenuId) {
    event.preventDefault(); // Mencegah navigasi default
    const submenu = document.getElementById(submenuId);
    submenu.classList.toggle('hidden');
  }

  document.addEventListener('click', function(event) {
    const dropdownContainer = document.getElementById('dropdown-container');
    const submenu = document.getElementById('submenu-dokumen');
    if (!dropdownContainer.contains(event.target)) {
      submenu.classList.add('hidden');
    }
  });
  
  document.getElementById('clear-search').addEventListener('click', function() {
    document.getElementById('search-input').value = '';
    document.getElementById('search-results').classList.add('hidden');
  });

  
  function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("translate-x-full");
  }

  function toggleSidebarSubMenu(event, submenuId) {
    event.preventDefault(); // Mencegah navigasi default
    const submenu = document.getElementById(submenuId);
    submenu.classList.toggle('hidden');
  }