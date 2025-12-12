# # from flask import Flask, request, redirect, session
# # import json
# # import os

# # app = Flask(__name__)
# # app.secret_key = "your_secret_key"

# # # Load users
# # def load_users():
# #     if not os.path.exists("users.json"):
# #         return []
# #     with open("users.json", "r") as f:
# #         try:
# #             return json.load(f)
# #         except:
# #             return []

# # # Save users
# # def save_users(users):
# #     with open("users.json", "w") as f:
# #         json.dump(users, f, indent=4)


# # # ---------------------- ROUTES ---------------------- #

# # # LOGIN PAGE
# # @app.route("/login", methods=["GET"])
# # def login_page():
# #     return open("login.html").read()


# # # LOGIN FORM SUBMIT
# # @app.route("/login", methods=["POST"])
# # def login():
# #     username = request.form["username"]
# #     password = request.form["password"]

# #     users = load_users()

# #     for u in users:
# #         if u["username"] == username and u["password"] == password:
# #             session["username"] = username
# #             return redirect("/home")

# #     return "Invalid login! <a href='/login'>Try again</a>"


# # # REGISTER PAGE
# # @app.route("/register", methods=["GET"])
# # def register_page():
# #     return open("register.html").read()


# # # REGISTER SUBMIT
# # @app.route("/register", methods=["POST"])
# # def register():
# #     username = request.form["username"]
# #     password = request.form["password"]

# #     users = load_users()

# #     # Check duplicate
# #     for u in users:
# #         if u["username"] == username:
# #             return "User already exists! <a href='/register'>Try again</a>"

# #     users.append({"username": username, "password": password})
# #     save_users(users)

# #     return redirect("/login")


# # # MAIN WEBSITE HOME (AFTER LOGIN)
# # @app.route("/home")
# # def home():
# #     if "username" not in session:
# #         return redirect("/login")

# #     return open("index.html").read()


# # # PROTECTED PAGES
# # @app.route("/dashboard")
# # def dashboard():
# #     if "username" not in session:
# #         return redirect("/login")
# #     return open("dashboard.html").read()


# # @app.route("/coding")
# # def coding():
# #     if "username" not in session:
# #         return redirect("/login")
# #     return open("coding.html").read()


# # @app.route("/assistant")
# # def assistant():
# #     if "username" not in session:
# #         return redirect("/login")
# #     return open("assistant.html").read()


# # @app.route("/aiml")
# # def aiml():
# #     if "username" not in session:
# #         return redirect("/login")
# #     return open("aiml.html").read()


# # @app.route("/interview")
# # def interview():
# #     if "username" not in session:
# #         return redirect("/login")
# #     return open("interview.html").read()


# # # LOGOUT
# # @app.route("/logout")
# # def logout():
# #     session.clear()
# #     return redirect("/login")


# # # RUN
# # if __name__ == "__main__":
# #     app.run(port=7000, debug=True)

# from flask import Flask, request, redirect, url_for, session, send_from_directory, render_template

# import json
# import os

# app = Flask(__name__)
# app.secret_key = "super_secret_key"   # Needed for sessions

# # Serve HTML files directly from MAJOR folder
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def render_page(filename):
#     return send_from_directory(BASE_DIR, filename)

# # ----------- ROUTES -----------

# @app.route("/")
# def home():
#     if "username" not in session:
#         return redirect("/login")
#     return render_page("index.html")

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with open("users.json", "r") as f:
#             users = json.load(f)

#         for user in users:
#             if user["username"] == username and user["password"] == password:
#                 session["username"] = username
#                 return redirect("/")
        
#         return "Invalid username or password"

#     return render_page("login.html")

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with open("users.json", "r") as f:
#             users = json.load(f)

#         users.append({"username": username, "password": password})

#         with open("users.json", "w") as f:
#             json.dump(users, f, indent=4)

#         return redirect("/login")

#     return render_page("register.html")

# @app.route("/logout")
# def logout():
#     session.pop("username", None)
#     return redirect("/login")

# # Any page you have in MAJOR folder
# @app.route("/<page>")
# def pages(page):
#     return render_page(page)

# # ------------------------------
# # ================= QUIZ SYSTEM EXTRA ROUTES ================= #

# # Load quizzes
# def load_quizzes():
#     with open("quizzes.json", "r") as f:
#         return json.load(f)

# # Load users (existing structure)
# def load_users():
#     with open("users.json", "r") as f:
#         return json.load(f)

# # Save users (existing structure)
# def save_users(users):
#     with open("users.json", "w") as f:
#         json.dump(users, f, indent=4)

# # --- 1. GET QUIZZES ---
# @app.route("/api/quizzes")
# def get_quizzes():
#     if "username" not in session:
#         return {"error": "Not logged in"}, 401
#     return load_quizzes()


# # --- 2. SUBMIT QUIZ ---
# @app.route("/api/submit", methods=["POST"])
# def submit_quiz():
#     if "username" not in session:
#         return {"error": "Not logged in"}, 401

#     data = request.json
#     module_id = data.get("module_id")
#     answers = data.get("answers")

#     quizzes = load_quizzes()
#     questions = quizzes[str(module_id)]["questions"]

#     score = 0
#     for i, q in enumerate(questions):
#         if answers[i] == q["answer_index"]:
#             score += 1

#     # Update user score
#     users = load_users()
#     for u in users:
#         if u["username"] == session["username"]:

#             # Create scores dict ONLY if missing
#             if "scores" not in u:
#                 u["scores"] = {}  

#             u["scores"][str(module_id)] = score

#     save_users(users)

#     return {"score": score}


# # --- 3. LEADERBOARD ---
# @app.route("/api/leaderboard")
# def leaderboard():
#     users = load_users()

#     # Convert to simple list (username + total score)
#     board = []
#     for u in users:
#         total = 0
#         if "scores" in u:
#             total = sum(u["scores"].values())
#         board.append({
#             "username": u["username"],
#             "total_score": total
#         })

#     # Sort highest score first
#     board = sorted(board, key=lambda x: x["total_score"], reverse=True)

#     return {"leaderboard": board}

# @app.route("/session-user")
# def session_user():
#     if "username" not in session:
#         return {"username": None}
#     return {"username": session["username"]}
# @app.route("/dashboard")
# def dashboard():
#     if "username" not in session:
#         return redirect("/login")

#     username = session["username"]

#     # Send username to dashboard.html
#     return render_template("dashboard.html", username=username)




# if __name__ == "__main__":
#     app.run(port=7000, debug=True)


# from flask import Flask, request, redirect, session, send_from_directory, render_template
# import json
# import os

# app = Flask(__name__)
# app.secret_key = "super_secret_key"

# # Serve static HTML files from same folder
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def render_page(filename):
#     return send_from_directory(BASE_DIR, filename)

# # --------------------
# # HOME (requires login)
# # --------------------
# @app.route("/")
# def home():
#     if "username" not in session:
#         return redirect("/login")
#     return render_page("index.html")   # your homepage

# # --------------------
# # LOGIN
# # --------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with open("users.json", "r") as f:
#             users = json.load(f)

#         for user in users:
#             if user["username"] == username and user["password"] == password:
#                 session["username"] = username
#                 return redirect("/")    # go to homepage
        
#         return "Invalid username or password"

#     return render_page("login.html")

# # --------------------
# # REGISTER
# # --------------------
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with open("users.json", "r") as f:
#             users = json.load(f)

#         users.append({"username": username, "password": password})

#         with open("users.json", "w") as f:
#             json.dump(users, f, indent=4)

#         return redirect("/login")

#     return render_page("register.html")

# # --------------------
# # LOGOUT
# # --------------------
# @app.route("/logout")
# def logout():
#     session.pop("username", None)
#     return redirect("/login")

# # --------------------
# # Serve other static pages
# # --------------------
# @app.route("/<page>")
# def pages(page):
#     return render_page(page)

# # --------------------
# # START SERVER
# # --------------------
# if __name__ == "__main__":
#     app.run(port=7000, debug=True)

# from flask import Flask, request, redirect, session, send_from_directory, render_template
# import json
# import os
# import sqlite3

# app = Flask(__name__)
# app.secret_key = "super_secret_key"

# # Serve static HTML files from same folder
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def render_page(filename):
#     return send_from_directory(BASE_DIR, filename)

# # --------------------
# # HOME (requires login)
# # --------------------
# @app.route("/")
# def home():
#     if "username" not in session:
#         return redirect("/login")
#     return render_page("index.html")   # your homepage

# # --------------------
# # LOGIN
# # --------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with open("users.json", "r") as f:
#             users = json.load(f)

#         for user in users:
#             if user["username"] == username and user["password"] == password:
#                 session["username"] = username
#                 return redirect("/")    # go to homepage
        
#         return "Invalid username or password"

#     return render_page("login.html")

# # --------------------
# # REGISTER
# # --------------------
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with open("users.json", "r") as f:
#             users = json.load(f)

#         users.append({"username": username, "password": password})

#         with open("users.json", "w") as f:
#             json.dump(users, f, indent=4)

#         return redirect("/login")

#     return render_page("register.html")

# # --------------------
# # LOGOUT
# # --------------------
# @app.route("/logout")
# def logout():
#     session.pop("username", None)
#     return redirect("/login")

# # --------------------
# # Serve other static pages
# # --------------------
# @app.route("/<page>")
# def pages(page):
#     return render_page(page)

# @app.route("/api/quizzes")
# def api_get_quizzes():
#     with open("quizzes.json", "r") as f:
#         data = json.load(f)
#     return data
# @app.route("/api/submit", methods=["POST"])
# def api_submit_quiz():
#     data = request.json
#     module_id = str(data["module_id"])
#     answers = data["answers"]

#     # Load quiz data
#     with open("quizzes.json", "r") as f:
#         quizzes = json.load(f)

#     questions = quizzes[module_id]["questions"]

#     score = 0
#     for i, q in enumerate(questions):
#         if answers[i] == q["answer_index"]:
#             score += 1

#     return {"score": score, "message": "Quiz submitted"}

# def get_db():
#     return sqlite3.connect("database.db", check_same_thread=False)



# # --------------------
# # START SERVER
# # --------------------
# if __name__ == "__main__":
#     app.run(port=7000, debug=True)



from flask import Flask, request, redirect, session, send_from_directory, jsonify
import os
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "super_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------
# Helper to serve static pages
# ---------------------------
def render_page(filename):
    return send_from_directory(BASE_DIR, filename)

# ---------------------------
# Database connection
# ---------------------------
def get_db():
    return sqlite3.connect("database.db", check_same_thread=False)

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")
    return render_page("index.html")  # Your main homepage

# ---------------------------
# LOGIN
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username
            return redirect("/")
        else:
            return "Invalid username or password"

    return render_page("login.html")

# ---------------------------
# REGISTER (optional)
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "User already exists"
        conn.close()
        return redirect("/login")

    return render_page("register.html")

# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/login")

# ---------------------------
# FETCH QUIZZES
# ---------------------------
@app.route("/api/quizzes")
def api_get_quizzes():
    with open("quizzes.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

# ---------------------------
# SUBMIT QUIZZES
# ---------------------------
@app.route("/api/submit", methods=["POST"])
def api_submit_quiz():
    if "username" not in session:
        return {"error": "Not logged in"}

    data = request.json
    module_id = str(data["module_id"])
    answers = data["answers"]

    # Load quiz data
    with open("quizzes.json", "r") as f:
        quizzes = json.load(f)

    questions = quizzes.get(module_id, {}).get("questions", [])

    score = 0
    for i, q in enumerate(questions):
        if i < len(answers) and answers[i] == q["answer_index"]:
            score += 1

    # Save score to DB
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_scores (username, module_id, score) VALUES (?, ?, ?)",
        (session["username"], module_id, score)
    )
    conn.commit()
    conn.close()

    return {"score": score, "message": "Quiz submitted"}

# ---------------------------
# GET USER PROGRESS
# ---------------------------
@app.route("/api/progress")
def api_progress():
    if "username" not in session:
        return {"error": "Not logged in"}

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT module_id, score FROM quiz_scores WHERE username=?", (session["username"],))
    rows = cursor.fetchall()
    conn.close()

    progress = [{"module_id": row[0], "score": row[1]} for row in rows]
    return {"username": session["username"], "progress": progress}

# ---------------------------
# Serve other static pages
# ---------------------------
@app.route("/<page>")
def pages(page):
    return render_page(page)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/login")
    return render_page("dashboard.html")
# @app.route("/dashboard")
# def dashboard():
#     if "username" not in session:
#         return redirect("/login")

#     return render_template("dashboard.html",
#                            username=session["username"],
#                            total_score=0) 

# ------------------ QUESTIONS ------------------
questions = [
    "Explain supervised vs unsupervised learning.",
    "What is overfitting and how do you prevent it?",
    "Explain the difference between classification and regression.",
    "What are decision trees and how do they work?",
    "Explain the concept of a confusion matrix.",
    "What is feature engineering and why is it important?"
]

# ------------------ ROUTES ------------------

@app.route("/interview")
def interview_page():
    if "username" not in session:
        return "Please log in to access the interview platform", 403
    return render_template("interview.html")


@app.route("/ask", methods=["POST"])
def ask_ai():
    if "username" not in session:
        return jsonify({"answer": "User not logged in"}), 403

    user_input = request.json.get("question")
    payload = {"query": user_input}
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(VAPI_URL, json=payload, headers=headers)
        response.raise_for_status()
        ai_answer = response.json().get("answer", "No response from AI")
    except requests.exceptions.RequestException as e:
        print("VAPI AI error:", e)
        ai_answer = "Error communicating with AI. Please try again."

    # Store Q&A in session
    session.setdefault("interview_history", []).append({"question": user_input, "answer": ai_answer})

    return jsonify({"answer": ai_answer})


@app.route("/interview_history")
def interview_history():
    return jsonify({"history": session.get("interview_history", [])})


@app.route("/get_next_question", methods=["GET"])
def get_next_question():
    session.setdefault("asked_questions", [])

    remaining_questions = [q for q in questions if q not in session["asked_questions"]]

    if not remaining_questions:
        return jsonify({"question": None, "message": "No more questions left."})

    question = random.choice(remaining_questions)
    session["asked_questions"].append(question)

    return jsonify({"question": question})


# ------------------ RUN APP ------------------

if __name__ == "__main__":
    app.run(port=7000, debug=True)

