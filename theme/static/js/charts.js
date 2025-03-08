
document.addEventListener("DOMContentLoaded", function() {
    function getJsonData(elementId) {
        var element = document.getElementById(elementId);
        return element ? JSON.parse(element.textContent) : [];
    }

    var labels = getJsonData("chartLabels");
    var dataValues = getJsonData("chartData");

    if (labels.length === 0 || dataValues.length === 0) {
        console.warn("Data chart kosong, grafik tidak ditampilkan.");
        return;
    }

    var canvas = document.getElementById("chartRingkasan");
    if (!canvas) return;
    
    var ctx = canvas.getContext("2d");

    var chartRingkasan = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Jumlah Dokumen',
                data: dataValues,
                backgroundColor: ['#4CAF50', '#2196F3', '#FF9800', '#E91E63', '#9C27B0', '#3F51B5', '#00BCD4'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    function resizeChart() {
        setTimeout(() => {
            chartRingkasan.resize();
        }, 300);
    }
    window.addEventListener("resize", resizeChart);
});



// Live Search Functionality
document.getElementById('searchInput').addEventListener('keyup', function() {
    var searchValue = this.value.toLowerCase();
    var rows = document.querySelectorAll('#peraturanTable tr');
    rows.forEach(function(row) {
        var namaPeraturan = row.cells[1].textContent.toLowerCase();
        if (namaPeraturan.includes(searchValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

function toggleReadMore(id, fullText) {
    var textElement = document.getElementById("teksPdf" + id);
    var words = fullText.split(" ");
    var maxWords = 100; // Batasi jumlah kata setelah Read More

    if (textElement.dataset.expanded === "true") {
        textElement.innerHTML = textElement.dataset.shortText;
        textElement.dataset.expanded = "false";
    } else {
        textElement.dataset.shortText = textElement.innerHTML;
        textElement.innerHTML = words.slice(0, maxWords).join(" ") + (words.length > maxWords ? "..." : "");
        textElement.dataset.expanded = "true";
    }
}