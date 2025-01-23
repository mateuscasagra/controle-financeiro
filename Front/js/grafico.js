function graphc() {
  const ctx = document.getElementById("grafico").getContext("2d");

  // Dados de entrada e saída para o mês de janeiro
  const data = {
    labels: [
      "01 Jan",
      "05 Jan",
      "10 Jan",
      "15 Jan",
      "20 Jan",
      "25 Jan",
      "30 Jan",
    ], // Dias do mês
    datasets: [
      {
        label: "Entradas",
        data: [1000], // Valores de entrada
        backgroundColor: "rgba(54, 162, 235, 0.5)", // Cor de fundo
        borderColor: "rgba(54, 162, 235, 1)", // Cor da borda
        borderWidth: 1,
        tension: 0.4, // Suavização da linha
      },
      {
        label: "Saídas",
        data: [1500], // Valores de saída
        backgroundColor: "rgba(255, 99, 132, 0.5)", // Cor de fundo
        borderColor: "rgba(255, 99, 132, 1)", // Cor da borda
        borderWidth: 1,
        tension: 0.4, // Suavização da linha
      },

      {
        label: "Saldo",
        data: [2009],
        backgroundColor: "grey", // Cor de fundo
        borderColor: "grey", // Cor da borda
        borderWidth: 1,
        tension: 0.4, // Suavização da linha
      },
    ],
  };

  // Configurações do gráfico
  const config = {
    type: "bar", // Tipo do gráfico (linha)
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top", // Posição da legenda
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Dias do Mês", // Texto do eixo X
          },
        },
        y: {
          title: {
            display: true,
            text: "Valores (R$)", // Texto do eixo Y
          },
          beginAtZero: true,
        },
      },
    },
  };

  // Criação do gráfico
  new Chart(ctx, config);
}

graphc();

// <td>${dado.tipo}</td>
