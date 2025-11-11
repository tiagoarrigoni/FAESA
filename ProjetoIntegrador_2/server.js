import express from "express";
import bodyParser from "body-parser";
import sqlite3 from "sqlite3";
import path from "path";
import bcrypt from "bcrypt";
import session from "express-session";
import { fileURLToPath } from "url";

// ======= Configuração básica =======
const app = express();
const PORT = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ======= Banco SQLite3 =======
const db = new sqlite3.Database("./database.db", (err) => {
  if (err) console.error("Erro ao conectar ao banco:", err);
  else console.log("✅ Banco SQLite conectado com sucesso!");
});

// Criação das tabelas
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      email TEXT UNIQUE,
      password TEXT
    )
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS test_results (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      test_type TEXT,
      score INTEGER,
      result_text TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(id)
    )
  `);
});

// ======= Middlewares =======
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static("public"));
app.use(
  session({
    secret: "hec-secret",
    resave: false,
    saveUninitialized: false,
  })
);

// ======= Autenticação =======
app.post("/login", (req, res) => {
  const { username, password } = req.body;
  db.get("SELECT * FROM users WHERE username = ?", [username], async (err, user) => {
    if (err) return res.status(500).send("Erro no servidor");
    if (!user) return res.status(400).send("Usuário não encontrado");

    const match = await bcrypt.compare(password, user.password);
    if (!match) return res.status(400).send("Senha incorreta");

    req.session.userId = user.id;
    res.redirect("/painel.html");
  });
});

app.post("/register", async (req, res) => {
  const { username, email, password } = req.body;
  const hashed = await bcrypt.hash(password, 10);
  db.run(
    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
    [username, email, hashed],
    (err) => {
      if (err) {
        console.error(err);
        return res.status(400).send("Erro ao registrar usuário");
      }
      res.redirect("/index.html");
    }
  );
});

// ======= Middleware de login =======
function auth(req, res, next) {
  if (!req.session.userId) return res.status(401).send("Não autorizado");
  next();
}

// ======= Salvar resultado do teste =======
app.post("/save-test", auth, (req, res) => {
  const { test_type, score, result_text } = req.body;
  const userId = req.session.userId;

  db.get(
    "SELECT * FROM test_results WHERE user_id = ? AND test_type = ? ORDER BY created_at DESC LIMIT 1",
    [userId, test_type],
    (err, lastTest) => {
      if (err) return res.status(500).send("Erro ao verificar último teste");

      if (lastTest) {
        const lastDate = new Date(lastTest.created_at);
        const now = new Date();
        const diffDays = (now - lastDate) / (1000 * 60 * 60 * 24);
        if (diffDays < 30) {
          return res
            .status(403)
            .json({ message: `Você já fez o teste ${test_type} há menos de 30 dias.` });
        }
      }

      db.run(
        "INSERT INTO test_results (user_id, test_type, score, result_text) VALUES (?, ?, ?, ?)",
        [userId, test_type, score, result_text],
        (err) => {
          if (err) return res.status(500).send("Erro ao salvar resultado");
          res.json({ message: "Resultado salvo com sucesso!" });
        }
      );
    }
  );
});

// ======= Ver histórico =======
app.get("/my-tests", auth, (req, res) => {
  const userId = req.session.userId;
  db.all(
    "SELECT test_type, score, result_text, created_at FROM test_results WHERE user_id = ? ORDER BY created_at DESC",
    [userId],
    (err, results) => {
      if (err) return res.status(500).send("Erro ao buscar histórico");
      res.json(results);
    }
  );
});

// ======= Inicia o servidor =======
app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
});
