import tkinter as tk
import random

class MathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pràctica de Matemàtiques")
        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Quina operació vols practicar?", font=("Arial", 14)).pack(pady=10)
        for op in ["Suma", "Resta", "Multiplicació", "Divisió"]:
            tk.Button(self.root, text=op, width=15, command=lambda o=op: self.new_problem(o)).pack(pady=5)
        tk.Button(self.root, text="Sèrie de 20", width=15, command=self.choose_series).pack(pady=5)
        tk.Button(self.root, text="Sortir", command=self.root.quit).pack(pady=10)

    def add_numpad(self, entry_widget, send_command):
        frame = tk.Frame(self.root)
        frame.pack(side="right", padx=10)
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1)
        ]
        for (text, row, col) in buttons:
            tk.Button(frame, text=text, width=8, height=4,
                  command=lambda t=text: entry_widget.insert(tk.END, t)).grid(row=row, column=col, padx=2, pady=2)
        tk.Button(frame, text="⌫", width=8, height=4,
              command=lambda: entry_widget.delete(len(entry_widget.get())-1, tk.END)).grid(row=4, column=0, padx=2, pady=2)
        tk.Button(frame, text="Envia", width=8, height=4,
              command=send_command).grid(row=4, column=2, padx=2, pady=2)

    def new_problem(self, operacio):
        self.clear_screen()
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        if operacio == "Suma":
            self.resultat = a + b
            signe = "+"
        elif operacio == "Resta":
            if a < b: a, b = b, a
            self.resultat = a - b
            signe = "-"
        elif operacio == "Multiplicació":
            self.resultat = a * b
            signe = "×"
        elif operacio == "Divisió":
            self.resultat = random.randint(1, 9)
            b = random.randint(1, 9)
            a = self.resultat * b
            signe = "÷"
        self.current_problem = f"{a} {signe} {b}"

        tk.Label(self.root, text=f"Resol: {self.current_problem}", font=("Arial", 14)).pack(pady=10)
        self.answer_entry = tk.Entry(self.root, font=("Arial", 12), width=10, justify="center")
        self.answer_entry.pack(pady=5)
        self.add_numpad(self.answer_entry, self.check_answer)
        self.answer_entry.focus_set()
        self.answer_entry.bind("<Return>", lambda event: self.check_answer())
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.feedback_label.pack(pady=5)
        tk.Button(self.root, text="Envia", command=self.check_answer).pack(pady=5)
        tk.Button(self.root, text="Tornar al menú", command=self.main_menu).pack(pady=10)

    def check_answer(self):
        try:
            resposta = int(self.answer_entry.get())
            if resposta == self.resultat:
                self.feedback_label.config(text="✅ Correcti!", fg="green")
            else:
                self.feedback_label.config(text=f"❌ Incorrecte. Era {self.resultat}", fg="red")
        except ValueError:
            self.feedback_label.config(text="⚠️ Resposta no vàlida", fg="orange")

    def choose_series(self):
        self.clear_screen()
        tk.Label(self.root, text="Quina operació vols per la sèrie de 20?", font=("Arial", 14)).pack(pady=10)
        for op in ["Suma", "Resta", "Multiplicació", "Divisió"]:
            tk.Button(self.root, text=op, width=15, command=lambda o=op: self.start_series(o)).pack(pady=5)
        tk.Button(self.root, text="Tornar", command=self.main_menu).pack(pady=10)

    def start_series(self, operacio):
        self.serie_operacio = operacio
        self.serie_total = 20
        self.serie_actual = 0
        self.serie_correctes = 0
        self.serie_incorrectes = 0
        self.serie_errors = []
        self.next_series_problem()

    def next_series_problem(self):
        if self.serie_actual >= self.serie_total:
            self.show_series_result()
            return
        self.serie_actual += 1
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        if self.serie_operacio == "Suma":
            resultat = a + b
            signe = "+"
        elif self.serie_operacio == "Resta":
            if a < b: a, b = b, a
            resultat = a - b
            signe = "-"
        elif self.serie_operacio == "Multiplicació":
            resultat = a * b
            signe = "×"
        elif self.serie_operacio == "Divisió":
            resultat = random.randint(1, 9)
            b = random.randint(1, 9)
            a = resultat * b
            signe = "÷"
        problema = f"{a} {signe} {b}"
        self.serie_current_result = resultat
        self.serie_current_problem = problema

        self.clear_screen()
        tk.Label(self.root, text=f"Operació {self.serie_actual} de {self.serie_total}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Resol: {problema}", font=("Arial", 14)).pack(pady=10)
        self.serie_answer_entry = tk.Entry(self.root, font=("Arial", 12), width=10, justify="center")
        self.serie_answer_entry.pack(pady=5)
        self.add_numpad(self.serie_answer_entry, self.check_series_answer)
        self.serie_answer_entry.focus_set()
        self.serie_answer_entry.bind("<Return>", lambda event: self.check_series_answer())
        self.serie_feedback_label = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.serie_feedback_label.pack(pady=5)
        tk.Button(self.root, text="Envia", command=self.check_series_answer).pack(pady=5)
        tk.Button(self.root, text="Sortir de la sèrie", command=self.main_menu).pack(pady=10)

    def check_series_answer(self):
        try:
            resposta = int(self.serie_answer_entry.get())
            if resposta == self.serie_current_result:
                self.serie_correctes += 1
                self.serie_feedback_label.config(text="✅ Correcti!", fg="green")
            else:
                self.serie_incorrectes += 1
                self.serie_errors.append((self.serie_current_problem, self.serie_current_result, resposta))
                self.serie_feedback_label.config(text=f"❌ Incorrecte. Era {self.serie_current_result}", fg="red")
        except ValueError:
            self.serie_incorrectes += 1
            self.serie_errors.append((self.serie_current_problem, self.serie_current_result, "No vàlida"))
            self.serie_feedback_label.config(text="⚠️ Resposta no vàlida", fg="orange")

        self.root.after(1000, self.next_series_problem)

    def show_series_result(self):
        self.clear_screen()
        tk.Label(self.root, text="Resultat de la sèrie de 20", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Encerts: {self.serie_correctes}").pack()
        tk.Label(self.root, text=f"Errors: {self.serie_incorrectes}").pack()
        if self.serie_errors:
            tk.Label(self.root, text="Errors:", font=("Arial", 12)).pack(pady=5)
            for prob, sol, user in self.serie_errors:
                tk.Label(self.root, text=f"{prob} = {sol} (Tu: {user})").pack()
            tk.Button(self.root, text="Repetir només errors", command=self.repeat_errors).pack(pady=10)
        tk.Button(self.root, text="Tornar al menú", command=self.main_menu).pack(pady=10)

    def repeat_errors(self):
        if not self.serie_errors:
            self.main_menu()
            return
        self.serie_repeat_list = list(self.serie_errors)
        self.serie_repeat_index = 0
        self.serie_repeat_correctes = 0
        self.serie_repeat_incorrectes = 0
        self.serie_repeat_errors = []
        self.next_repeat_error()

    def next_repeat_error(self):
        if self.serie_repeat_index >= len(self.serie_repeat_list):
            self.show_repeat_result()
            return
        prob, sol, _ = self.serie_repeat_list[self.serie_repeat_index]
        self.serie_repeat_index += 1
        self.serie_repeat_current_problem = prob
        self.serie_repeat_current_result = sol

        self.clear_screen()
        tk.Label(self.root, text=f"Repetició d'errors ({self.serie_repeat_index} de {len(self.serie_repeat_list)})", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=f"Resol: {prob}", font=("Arial", 14)).pack(pady=10)
        self.serie_repeat_answer_entry = tk.Entry(self.root, font=("Arial", 12), width=10, justify="center")
        self.serie_repeat_answer_entry.pack(pady=5)
        self.add_numpad(self.serie_repeat_answer_entry, self.check_repeat_error)
        self.serie_repeat_answer_entry.focus_set()
        self.serie_repeat_answer_entry.bind("<Return>", lambda event: self.check_repeat_error())
        self.serie_repeat_feedback_label = tk.Label(self.root, text="", font=("Arial", 12), fg="blue")
        self.serie_repeat_feedback_label.pack(pady=5)
        tk.Button(self.root, text="Envia", command=self.check_repeat_error).pack(pady=5)
        tk.Button(self.root, text="Sortir", command=self.main_menu).pack(pady=10)

    def check_repeat_error(self):
        try:
            resposta = int(self.serie_repeat_answer_entry.get())
            if resposta == self.serie_repeat_current_result:
                self.serie_repeat_correctes += 1
                self.serie_repeat_feedback_label.config(text="✅ Correcte!", fg="green")
            else:
                self.serie_repeat_incorrectes += 1
                self.serie_repeat_errors.append((self.serie_repeat_current_problem, self.serie_repeat_current_result, resposta))
                self.serie_repeat_feedback_label.config(text=f"❌ Incorrecte. Era {self.serie_repeat_current_result}", fg="red")
        except ValueError:
            self.serie_repeat_incorrectes += 1
            self.serie_repeat_errors.append((self.serie_repeat_current_problem, self.serie_repeat_current_result, "No vàlida"))
            self.serie_repeat_feedback_label.config(text="⚠️ Resposta no vàlida", fg="orange")

        self.root.after(1000, self.next_repeat_error)

    def show_repeat_result(self):
        self.clear_screen()
        tk.Label(self.root, text="Resultat de la repetició", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text=f"Encerts: {self.serie_repeat_correctes}").pack()
        tk.Label(self.root, text=f"Errors: {self.serie_repeat_incorrectes}").pack()
        if self.serie_repeat_errors:
            tk.Label(self.root, text="Errors:", font=("Arial", 12)).pack(pady=5)
            for prob, sol, user in self.serie_repeat_errors:
                tk.Label(self.root, text=f"{prob} = {sol} (Tu: {user})").pack()
        tk.Button(self.root, text="Tornar al menú", command=self.main_menu).pack(pady=10)

# Iniciar l'app
root = tk.Tk()
app = MathApp(root)
root.mainloop()