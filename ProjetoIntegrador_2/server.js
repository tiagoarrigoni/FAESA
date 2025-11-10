const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");
const path = require("path");

const app = express();
const db = new sqlite3.Database("./database.db");

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// Cria tabela de usuários
db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
)`);

// Rota de cadastro
app.post("/register", (req, res) => {
  const { username, email, password } = req.body;

  db.run(
    `INSERT INTO users (username, email, password) VALUES (?, ?, ?)`,
    [username, email, password],
    (err) => {
      if (err) {
        res.send(`
          <script>
            alert("Erro ao cadastrar: Usuário já existe ou dados inválidos!");
            window.location.href = "/register.html";
          </script>
        `);
      } else {
        res.send(`
          <script>
            alert("Bem-vindo, ${username}! Cadastro realizado com sucesso!");
            window.location.href = "/";
          </script>
        `);
      }
    }
  );
});

// Rota de login
app.post("/login", (req, res) => {
  const { username, password } = req.body;

  db.get(
    `SELECT * FROM users WHERE username = ? AND password = ?`,
    [username, password],
    (err, row) => {
      if (row) {
        res.send(`
          <h2 style="font-family:Arial; text-align:center; margin-top:50px;">
            Bem-vindo, ${row.username}! <br><br>
            <a href="/">Voltar</a>
          </h2>
        `);
      } else {
        res.send(`
          <script>
            alert("Usuário ou senha incorretos!");
            window.location.href = "/";
          </script>
        `);
      }
    }
  );
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
