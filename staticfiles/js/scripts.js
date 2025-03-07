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


  
  function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("translate-x-full");
  }

  function toggleSidebarSubMenu(event, submenuId) {
    event.preventDefault(); // Mencegah navigasi default
    const submenu = document.getElementById(submenuId);
    submenu.classList.toggle('hidden');
  }