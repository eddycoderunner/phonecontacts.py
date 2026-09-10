from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "c036c8726269e640cc155688754a7e4fb2fee731028d28c4"

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the contacts table if it doesn't exist yet."""
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name  TEXT,
            phone      TEXT NOT NULL,
            email      TEXT,
            address    TEXT,
            company    TEXT,
            group_name TEXT DEFAULT 'General',
            favorite   INTEGER DEFAULT 0,
            notes      TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    contacts = conn.execute(
        "SELECT * FROM contacts ORDER BY first_name COLLATE NOCASE"
    ).fetchall()
    conn.close()

    total = len(contacts)
    favorites = sum(1 for c in contacts if c["favorite"])
    groups = sorted({c["group_name"] or "General" for c in contacts})

    return render_template(
        "index.html",
        contacts=contacts,
        total=total,
        favorites=favorites,
        group_count=len(groups),
        groups=groups,
    )

@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        conn = get_db()
        conn.execute(
            """INSERT INTO contacts
               (first_name, last_name, phone, email, address, company, group_name, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.form["first_name"].strip(),
                request.form.get("last_name", "").strip(),
                request.form["phone"].strip(),
                request.form.get("email", "").strip(),
                request.form.get("address", "").strip(),
                request.form.get("company", "").strip(),
                request.form.get("group_name", "General").strip() or "General",
                request.form.get("notes", "").strip(),
                datetime.now().strftime("%Y-%m-%d"),
            ),
        )
        conn.commit()
        conn.close()
        flash("Contact added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_contact.html")

@app.route("/edit/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):
    conn = get_db()
    if request.method == "POST":
        conn.execute(
            """UPDATE contacts SET
               first_name=?, last_name=?, phone=?, email=?, address=?, company=?, group_name=?, notes=?
               WHERE id=?""",
            (
                request.form["first_name"].strip(),
                request.form.get("last_name", "").strip(),
                request.form["phone"].strip(),
                request.form.get("email", "").strip(),
                request.form.get("address", "").strip(),
                request.form.get("company", "").strip(),
                request.form.get("group_name", "General").strip() or "General",
                request.form.get("notes", "").strip(),
                contact_id,
            ),
        )
        conn.commit()
        conn.close()
        flash("Contact updated!", "success")
        return redirect(url_for("index"))

    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (contact_id,)).fetchone()
    conn.close()
    if contact is None:
        flash("Contact not found.", "error")
        return redirect(url_for("index"))
    return render_template("edit_contact.html", contact=contact)

@app.route("/delete/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()
    flash("Contact deleted.", "info")
    return redirect(url_for("index"))

@app.route("/favorite/<int:contact_id>", methods=["POST"])
def toggle_favorite(contact_id):
    conn = get_db()
    row = conn.execute("SELECT favorite FROM contacts WHERE id=?", (contact_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({"error": "not found"}), 404
    new_value = 0 if row["favorite"] else 1
    conn.execute("UPDATE contacts SET favorite=? WHERE id=?", (new_value, contact_id))
    conn.commit()
    conn.close()
    return jsonify({"favorite": new_value})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)