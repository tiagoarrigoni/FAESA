// ======= Importações =======
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
const dbPath = path.join(__dirname, "database.db");

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) console.error("Erro ao conectar ao banco:", err);
  else console.log("✅ Banco SQLite conectado com sucesso em:", dbPath);
});

// ======= Criação das tabelas =======
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

  db.run(`
  CREATE TABLE IF NOT EXISTS user_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    nome_completo TEXT,
    nascimento TEXT,
    peso REAL,
    altura REAL,
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

// ======= Middleware de autenticação =======
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

app.post("/save-info", auth, (req, res) => {
  const { nome_completo, nascimento, peso, altura } = req.body;
  const userId = req.session.userId;

  db.get("SELECT * FROM user_info WHERE user_id = ?", [userId], (err, row) => {
    if (err) {
      console.error("Erro ao buscar user_info:", err);
      return res.status(500).send("Erro ao buscar informações");
    }

    if (row) {
      // Já existe: bloqueia edição
      return res
        .status(403)
        .json({ message: "As informações pessoais já foram preenchidas e não podem ser alteradas." });
    } else {
      // Cria novo registro
      db.run(
        "INSERT INTO user_info (user_id, nome_completo, nascimento, peso, altura) VALUES (?, ?, ?, ?, ?)",
        [userId, nome_completo, nascimento, peso, altura],
        (err2) => {
          if (err2) {
            console.error("Erro ao salvar user_info:", err2);
            return res.status(500).send("Erro ao salvar informações");
          }
          res.json({ message: "Informações salvas com sucesso!" });
        }
      );
    }
  });
});




// ======= Ver histórico de testes =======
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

// ======= Verifica se o teste já foi feito =======
app.get("/get-test", auth, (req, res) => {
  const userId = req.session.userId;
  const { test_type } = req.query;

  db.get(
    "SELECT * FROM test_results WHERE user_id = ? AND test_type = ? ORDER BY created_at DESC LIMIT 1",
    [userId, test_type],
    (err, lastTest) => {
      if (err) {
        console.error("Erro ao verificar teste:", err);
        return res.status(500).json({ message: "Erro ao verificar teste" });
      }

      if (!lastTest) {
        return res.json({ exists: false });
      }

      const lastDate = new Date(lastTest.created_at);
      const now = new Date();
      const diffDays = (now - lastDate) / (1000 * 60 * 60 * 24);

      if (diffDays < 30) {
        return res.json({
          exists: true,
          score: lastTest.score,
          result_text: lastTest.result_text,
        });
      }

      res.json({ exists: false });
    }
  );
});

// ======= Retorna usuário logado =======
app.get("/session-user", auth, (req, res) => {
  db.get("SELECT username FROM users WHERE id = ?", [req.session.userId], (err, user) => {
    if (err) return res.status(500).send("Erro ao buscar usuário");
    res.json(user || { username: "Usuário" });
  });
});

// ======= Retorna informações pessoais completas =======
app.get("/user-info", auth, (req, res) => {
  const userId = req.session.userId;

  db.get("SELECT * FROM user_info WHERE user_id = ?", [userId], (err, info) => {
    if (err) {
      console.error("Erro ao buscar informações pessoais:", err);
      return res.status(500).json({ message: "Erro ao buscar informações pessoais" });
    }

    // Se não houver registro, retorna estrutura vazia (evita erro no front)
    if (!info) {
      console.warn("Nenhuma informação pessoal encontrada para o usuário:", userId);
      return res.json({
        nome_completo: null,
        nascimento: null,
        peso: null,
        altura: null
      });
    }

    // Retorna dados completos do usuário
    res.json({
      nome_completo: info.nome_completo,
      nascimento: info.nascimento,
      peso: info.peso,
      altura: info.altura
    });
  });
});




// ======= Inicializa o servidor =======
app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
});
