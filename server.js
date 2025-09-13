const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
  host: "localhost",
  user: "root",       // your MySQL username
  password: "password", // your MySQL password
  database: "attendance_system"
});

db.connect(err => {
  if (err) throw err;
  console.log("✅ MySQL Connected...");
});

// Create tables if not exist
db.query(`
  CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
  )
`);

db.query(`
  CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
  )
`);

// Teacher registration
app.post("/api/register/teacher", (req, res) => {
  const { name, email, password } = req.body;
  db.query("INSERT INTO teachers (name, email, password) VALUES (?, ?, ?)", 
    [name, email, password], (err) => {
      if (err) return res.json({ success: false, message: "Email already exists" });
      res.json({ success: true, message: "Teacher registered successfully" });
    });
});

// Student registration
app.post("/api/register/student", (req, res) => {
  const { name, email, password } = req.body;
  db.query("INSERT INTO students (name, email, password) VALUES (?, ?, ?)", 
    [name, email, password], (err) => {
      if (err) return res.json({ success: false, message: "Email already exists" });
      res.json({ success: true, message: "Student registered successfully" });
    });
});

// Teacher login
app.post("/api/login/teacher", (req, res) => {
  const { email, password } = req.body;
  db.query("SELECT * FROM teachers WHERE email=? AND password=?", [email, password], (err, result) => {
    if (err) throw err;
    if (result.length > 0) {
      res.json({ success: true, message: "Teacher login successful" });
    } else {
      res.json({ success: false, message: "Invalid credentials" });
    }
  });
});

// Student login
app.post("/api/login/student", (req, res) => {
  const { email, password } = req.body;
  db.query("SELECT * FROM students WHERE email=? AND password=?", [email, password], (err, result) => {
    if (err) throw err;
    if (result.length > 0) {
      res.json({ success: true, message: "Student login successful" });
    } else {
      res.json({ success: false, message: "Invalid credentials" });
    }
  });
});

app.listen(5000, () => console.log("🚀 Server running on http://localhost:5000"));
