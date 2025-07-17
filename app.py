from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def home():
    popup_message = ""
    panda_status = ""

    if request.method == "POST":
        task_name = request.form.get("task")
        completion_time_str = request.form.get("completion_time")
        emoji = request.form.get("emoji", "✅")

        if not task_name or not completion_time_str:
            popup_message = "Task and time are required!"
        else:
            try:
                completion_time = datetime.strptime(completion_time_str, "%Y-%m-%dT%H:%M")
                is_overdue = datetime.now() - completion_time > timedelta(hours=24)

                task = {
                    "id": len(tasks) + 1,
                    "task": task_name,
                    "time": completion_time.strftime("%Y-%m-%d %H:%M"),
                    "emoji": emoji,
                    "overdue": is_overdue,
                    "completed": False,
                }

                tasks.append(task)

                popup_message = "🐼 Great! Task added successfully." if not is_overdue else "🐼 Oh no! This task is overdue by more than 24 hours!"
                panda_status = "happy" if not is_overdue else "sad"

            except ValueError:
                popup_message = "Invalid time format. Use YYYY-MM-DD HH:MM."

    return render_template("index.html", tasks=tasks, popup_message=popup_message, panda_status=panda_status)

@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
