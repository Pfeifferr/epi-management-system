/*
Inicialização dos gráficos do dashboard utilizando Chart.js.
Os dados são injetados pelo template Django via variáveis globais.
*/

document.addEventListener("DOMContentLoaded", function () {

    if (typeof graficoStatusDados !== "undefined") {

        new Chart(document.getElementById('chartStatus'), {
            type: 'doughnut',
            data: {
                labels: ['Em Uso', 'Devolvidos', 'Outros'],
                datasets: [{
                    data: graficoStatusDados,
                    backgroundColor: ['#ffc107', '#28a745', '#dc3545'],
                    borderWidth: 0
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        new Chart(document.getElementById('chartTopEpis'), {
            type: 'bar',
            data: {
                labels: topEpisNomes,
                datasets: [{
                    label: 'Qtd',
                    data: topEpisQtds,
                    backgroundColor: '#0d6efd'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });

        new Chart(document.getElementById('chartEntregas'), {
            type: 'line',
            data: {
                labels: diasLabels,
                datasets: [{
                    label: 'Entregas',
                    data: entregasPorDia,
                    borderColor: '#17a2b8',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
            }
        });

    }
});