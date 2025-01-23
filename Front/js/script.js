// Função para buscar os dados do backend e preencher a tabela de extratos
// Função para buscar os dados do backend e preencher a tabela de extratos
function fetchDados() {
  fetch("http://127.0.0.1:5000/get_dados") // URL do backend
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Log dos dados recebidos

      const tbody = document
        .getElementById("tabela-extrato")
        .getElementsByTagName("tbody")[0];
      tbody.innerHTML = ""; // Limpa a tabela antes de adicionar os novos dados

      if (Array.isArray(data)) {
        // Verifica se a resposta é um array
        // Preenche a tabela com os dados recebidos
        data.forEach((dado) => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td>${dado.data}</td>
            <td>${dado.onde}</td>
            <td>${dado.valor.toFixed(2)}</td>
          `;
          tbody.appendChild(tr);
        });
      } else {
        console.error("A resposta não é um array:", data);
      }
    })
    .catch((error) => console.error("Erro ao buscar dados:", error));
}

// Função para enviar um arquivo .ofx para o backend
function enviaExtrato() {
  document.getElementById("envia").addEventListener("click", () => {
    const input = document.getElementById("subir-arquivo");
    const file = input.files[0];

    if (!file) {
      alert("Por favor, selecione um arquivo .ofx");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:5000/upload_ofx", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(`Erro: ${data.error}`);
        } else {
          alert(data.message);

          // Atualiza os dados na tabela após o upload do arquivo
          fetchDados();
        }
      })
      .catch((error) => {
        console.error("Erro ao enviar o arquivo:", error);
        alert("Erro ao enviar o arquivo");
      });
  });
}

// Configura os eventos assim que o conteúdo da página é carregado
document.addEventListener("DOMContentLoaded", () => {
  fetchDados(); // Busca os dados ao carregar a página
  enviaExtrato(); // Configura o evento de envio do arquivo
});
