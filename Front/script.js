function fetchDados() {
  function fetchDados() {
    fetch("http://127.0.0.1:5000/get_dados") // URL do backend
      .then((response) => response.json())
      .then((data) => {
        const tbody = document
          .getElementById("tabela-extrato")
          .getElementsByTagName("tbody")[0];
        tbody.innerHTML = ""; // Limpa a tabela antes de adicionar os novos dados

        // Preenche a tabela com os dados recebidos
        data.forEach((dado) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
              <td>${dado.data}</td>
              <td>${dado.onde}</td>
              <td>${dado.valor}</td>
            `;
          tbody.appendChild(tr);
        });
      })
      .catch((error) => console.error("Erro ao buscar dados:", error));
  }

  // Chama a função para preencher a tabela assim que o conteúdo for carregado
  fetchDados();
}
