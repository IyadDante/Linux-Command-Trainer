import customtkinter as ctk
import json
import random
import os
import sys
import traceback

def main():
    try:
        # -------------------------
        # Load Questions
        # -------------------------
        def load_questions():
            with open("questions.json", "r") as file:
                return json.load(file)

        all_questions = load_questions()

        # -------------------------
        # Load / Save Stats
        # -------------------------
        def load_stats():
            if not os.path.exists("stats.json"):
                return {}
            with open("stats.json", "r") as f:
                return json.load(f)

        def save_stats():
            with open("stats.json", "w") as f:
                json.dump(stats, f, indent=4)

        stats = load_stats()

        # -------------------------
        # App State
        # -------------------------
        current_question = None
        filtered_questions = []
        score = 0
        total = 0

        # -------------------------
        # Helpers
        # -------------------------
        def normalize(text):
            return " ".join(text.strip().split())

        def filter_questions():
            category = category_var.get()
            difficulty = difficulty_var.get()

            nonlocal filtered_questions
            filtered_questions = [
                q for q in all_questions
                if (category == "All" or q["category"] == category)
                and (difficulty == "All" or q["difficulty"] == difficulty)
            ]

        # -------------------------
        # Adaptive Engine
        # -------------------------
        def adaptive_choice():
            weighted_pool = []

            for q in filtered_questions:
                key = f"{q['category']}_{q['difficulty']}"
                stat = stats.get(key, {"correct": 0, "wrong": 0})

                attempts = stat["correct"] + stat["wrong"]

                if attempts == 0:
                    weight = 3
                else:
                    accuracy = stat["correct"] / attempts
                    weight = 5 if accuracy < 0.6 else 1

                weighted_pool.extend([q] * weight)

            return random.choice(weighted_pool)

        # -------------------------
        # Question Logic
        # -------------------------
        def load_new_question():
            nonlocal current_question

            if not filtered_questions:
                question_label.configure(text="No questions for selected filters.")
                return

            current_question = adaptive_choice()
            question_label.configure(text=current_question["question"])
            answer_entry.delete(0, "end")
            result_label.configure(text="")

        def check_answer():
            nonlocal score, total

            user_answer = normalize(answer_entry.get())
            correct_answers = [normalize(a) for a in current_question["answer"]]

            key = f"{current_question['category']}_{current_question['difficulty']}"

            if key not in stats:
                stats[key] = {"correct": 0, "wrong": 0}

            total += 1

            if user_answer in correct_answers:
                score += 1
                stats[key]["correct"] += 1
                result_label.configure(text="Correct ✅", text_color="green")
            else:
                stats[key]["wrong"] += 1
                result_label.configure(
                    text=f"Wrong ❌ | Correct: {correct_answers[0]}",
                    text_color="red"
                )

            save_stats()
            score_label.configure(text=f"Score: {score}/{total}")
            progress_bar.set(score / total if total > 0 else 0)

        # -------------------------
        # UI Setup
        # -------------------------
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        app = ctk.CTk()
        app.title("Linux Command Trainer")
        app.geometry("900x650")

        title = ctk.CTkLabel(
            app,
            text="🐧 Linux Command Trainer",
            font=("Segoe UI", 30, "bold")
        )
        title.pack(pady=20)

        filters_frame = ctk.CTkFrame(app)
        filters_frame.pack(pady=10)

        category_var = ctk.StringVar(value="All")
        difficulty_var = ctk.StringVar(value="All")

        categories = ["All"] + sorted(set(q["category"] for q in all_questions))
        difficulties = ["All"] + sorted(set(q["difficulty"] for q in all_questions))

        category_menu = ctk.CTkOptionMenu(filters_frame, values=categories, variable=category_var)
        category_menu.pack(side="left", padx=10)

        difficulty_menu = ctk.CTkOptionMenu(filters_frame, values=difficulties, variable=difficulty_var)
        difficulty_menu.pack(side="left", padx=10)

        apply_button = ctk.CTkButton(
            filters_frame,
            text="Apply Filters",
            command=lambda: [filter_questions(), load_new_question()]
        )
        apply_button.pack(side="left", padx=10)

        question_label = ctk.CTkLabel(
            app,
            text="",
            font=("Segoe UI", 22),
            wraplength=750
        )
        question_label.pack(pady=30)

        answer_entry = ctk.CTkEntry(
            app,
            width=650,
            height=50,
            font=("Consolas", 20)
        )
        answer_entry.pack(pady=10)

        check_button = ctk.CTkButton(app, text="Check Answer", width=220, command=check_answer)
        check_button.pack(pady=10)

        next_button = ctk.CTkButton(app, text="Next Question", width=220, command=load_new_question)
        next_button.pack(pady=5)

        result_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 18))
        result_label.pack(pady=15)

        progress_bar = ctk.CTkProgressBar(app, width=500)
        progress_bar.pack(pady=20)
        progress_bar.set(0)

        score_label = ctk.CTkLabel(app, text="Score: 0/0", font=("Segoe UI", 18))
        score_label.pack()

        filter_questions()
        load_new_question()

        app.mainloop()

    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
