# ⚒️ QueryForge

> **A modern SQL Query Builder and Database Explorer built with Python, SQLite, and CustomTkinter.**

QueryForge is a desktop application that simplifies SQL query creation through an intuitive graphical interface. It enables users to explore database schemas, visually build SQL queries, preview generated SQL, execute queries, and export results to Excel without manually writing SQL.

---

## ✨ Features

- 🔗 Connect to SQLite databases
- 🗂 Browse database tables and columns
- 📝 Generate SQL queries visually
- 🔍 Add dynamic filters with multiple operators
- 👀 Live SQL preview
- ▶️ Execute SQL queries safely
- 📊 Display results in an interactive data grid
- 📤 Export query results to Excel (.xlsx)
- 🌙 Modern dark-themed interface using CustomTkinter

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Application Development |
| SQLite | Database Engine |
| CustomTkinter | Desktop GUI |
| OpenPyXL | Excel Export |
| tksheet | Interactive Data Grid |

---

## 📁 Project Structure

```text
QueryForge/
│
├── database/
│   ├── db_connection.py
│   ├── query_executor.py
│   └── schema_loader.py
│
├── exports/
│   └── excel_export.py
│
├── models/
│   ├── column.py
│   ├── filter.py
│   └── table.py
│
├── query/
│   ├── query_builder.py
│   └── sql_generator.py
│
├── ui/
│   ├── filter_panel.py
│   ├── main_window.py
│   ├── results_panel.py
│   ├── sql_preview_panel.py
│   ├── table_panel.py
│   └── toolbar.py
│
├── Sample_DB.db
├── main.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/QueryForge.git
cd QueryForge
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python main.py
```

---

## 📖 How to Use

1. Launch QueryForge.
2. Click **Connect DB** and select a SQLite database.
3. Choose a table from the Database Explorer.
4. Select the columns you want to retrieve.
5. Add one or more filters.
6. Review the generated SQL in the SQL Preview panel.
7. Click **Run Query** to execute.
8. Export the results to Excel if needed.

---

## 📸 Screenshots

### Database Explorer

> *Add screenshot here*

### SQL Query Builder

> *Add screenshot here*

### Query Results

> *Add screenshot here*

---

## 🎯 Planned Features

- JOIN Builder
- GROUP BY support
- HAVING clause support
- ORDER BY & LIMIT controls
- Saved query projects
- Query history
- Multiple database support
  - MySQL
  - PostgreSQL
  - SQL Server
- CSV Export
- PDF Export

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Cyril Jhay Capitulo**

- 🎓 Bachelor of Science in Electronics Engineering
- 📊 Master of Data Analytics (New Zealand Skills and Education Group)

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!
