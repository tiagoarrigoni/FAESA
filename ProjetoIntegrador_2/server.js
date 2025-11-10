const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");
const path = require("path");

const app = express();
const db = new sqlite3.Database("./database.db");
console.log("📂 Banco de dados usado:", path.resolve("./database.db"));


// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// 🧱 Cria tabela de usuários se não existir
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
  )
`);

app.post("/register", (req, res) => {
  // 👇 Captura os dados enviados pelo formulário
  const { username, email, password } = req.body;

  console.log("📩 Requisição POST recebida em /register");
  console.log("📦 Dados recebidos:", req.body);

  if (!username || !email || !password) {
    return res.send(`
      <script>
        alert("Preencha todos os campos!");
        window.location.href = "/register.html";
      </script>
    `);
  }

  db.run(
    `INSERT INTO users (username, email, password) VALUES (?, ?, ?)`,
    [username, email, password],
    (err) => {
      if (err) {
        console.error("❌ Erro ao cadastrar:", err.message);
        return res.send(`
          <script>
            alert("Erro ao cadastrar: Usuário já existe ou dados inválidos!");
            window.location.href = "/register.html";
          </script>
        `);
      }

      console.log(`✅ Usuário cadastrado: ${username}`);
      res.send(`
        <script>
          alert("Bem-vindo, ${username}! Cadastro realizado com sucesso!");
          window.location.href = "/index.html";
        </script>
      `);
    }
  );
});


app.post("/login", (req, res) => {
  const { username, password } = req.body;

  db.get(
    `SELECT * FROM users WHERE username = ? AND password = ?`,
    [username, password],
    (err, row) => {
      if (err) {
        console.error("Erro ao verificar login:", err.message);
        return res.status(500).send("Erro no servidor.");
      }

      if (row) {
        console.log(`✅ Login realizado: ${row.username}`);
        res.send(`
          <script>
            alert("Login bem-sucedido! Bem-vindo, ${row.username}!");
            window.location.href = "/painel.html";
          </script>
        `);
      } else {
        res.send(`
          <script>
            alert("Usuário ou senha incorretos!");
            window.location.href = "/index.html";
          </script>
        `);
      }
    }
  );
});


// 🚀 Inicia o servidor
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
