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
  event.preventDefault();
  const submenu = document.getElementById(submenuId);
  submenu.classList.toggle('hidden');
}

document.addEventListener('click', function(event) {
  const dropdownContainers = ['dropdown-container', 'profil-dropdown-container'];
  const submenus = ['submenu-dokumen', 'submenu-profil'];
  
  submenus.forEach((submenuId, index) => {
      const container = document.getElementById(dropdownContainers[index]);
      const submenu = document.getElementById(submenuId);
      if (!container.contains(event.target)) {
          submenu.classList.add('hidden');
      }
  });
});

function toggleSidebarSubMenu(event, submenuId) {
  event.preventDefault(); // Mencegah navigasi link

  // Tutup submenu lain (optional)
  document.querySelectorAll('#sidebar ul ul').forEach(ul => {
    if (ul.id !== submenuId) {
      ul.classList.add('hidden');
    }
  });

  // Toggle submenu terkait
  const submenu = document.getElementById(submenuId);
  submenu.classList.toggle('hidden');
}

document.addEventListener('click', function(event) {
  const sidebar = document.getElementById('sidebar');

  // Cek apakah klik di luar sidebar
  if (!sidebar.contains(event.target)) {
    // Tutup semua submenu
    document.querySelectorAll('#sidebar ul ul').forEach(submenu => {
      submenu.classList.add('hidden');
    });
  }
});
