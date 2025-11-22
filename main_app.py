import tkinter as tk
import os
from tkinter import messagebox
#ifandraisany interface le interface main amin'ny le moteur
from diagnostic_engine import diagnose, generate_explanation

#Liste symptome raha mbo te hampilitsy hafa
SYMPTOMS = [
    "fumée noire",
    "consommation élevée",
    "moteur chauffe",
    "fuite liquide",
    "démarrage difficile",
    "batterie faible",
    "fumée blanche",
    "perte de puissance",
    "bruit métallique côté moteur",
]


class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        bg_main = "#3e2723"   # marron foncé
        bg_card = "#4e342e"  # marron un peu plus clair
        accent = "#ffb300"   # bouton jaune/orangé

        self.root.configure(bg=bg_main)
        self.root.title("Connexion mécanicien")
        self.root.geometry("480x260")

        container = tk.Frame(root, bg=bg_main)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        title = tk.Label(
            container,
            text="Connexion mécanicien",
            bg=bg_main,
            fg="white",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(pady=(0, 15))

        card = tk.Frame(container, bg=bg_card)
        card.pack(fill="x")

        label_email = tk.Label(
            card,
            text="Adresse e-mail :",
            bg=bg_card,
            fg="white",
            font=("Segoe UI", 10),
        )
        label_email.pack(anchor="w", padx=15, pady=(15, 2))

        self.entry_email = tk.Entry(card, font=("Segoe UI", 10))
        self.entry_email.pack(fill="x", padx=15, pady=(0, 10))

        label_pwd = tk.Label(
            card,
            text="Mot de passe :",
            bg=bg_card,
            fg="white",
            font=("Segoe UI", 10),
        )
        label_pwd.pack(anchor="w", padx=15, pady=(5, 2))

        self.entry_pwd = tk.Entry(card, show="*", font=("Segoe UI", 10))
        self.entry_pwd.pack(fill="x", padx=15, pady=(0, 15))

        self.error_label = tk.Label(
            container,
            text="",
            bg=bg_main,
            fg="#ffccbc",
            font=("Segoe UI", 9),
        )
        self.error_label.pack(pady=(8, 0))

        btn = tk.Button(
            container,
            text="Se connecter",
            command=self.try_login,
            bg=accent,
            fg="black",
            activebackground="#ffa000",
            activeforeground="black",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=5,
        )
        btn.pack(pady=(10, 0))

    def try_login(self):
        email = self.entry_email.get().strip().lower()
        password = self.entry_pwd.get().strip()

        # vérification minimale: champs non vides
        if not email or not password:
            self.error_label.config(
                text="Merci de saisir une adresse e-mail et un mot de passe."
            )
            return

        # option: vérifier un format e-mail grossier
        if "@" not in email or "." not in email:
            self.error_label.config(
                text="Format d'adresse e-mail incorrect. Exemple : mecano@garage.mg"
            )
            return

        # confirmation métier: réservé aux mécaniciens mais basé sur l'honnêteté
        answer = messagebox.askyesno(
            "Confirmation",
            "Êtes-vous vraiment mécanicien(ne) automobile ?\n\nCliquez sur 'Oui' pour continuer.",
        )

        if answer:
            self.error_label.config(text="")
            self.on_success(email)
        else:
            self.error_label.config(
                text="Accès réservé en priorité aux mécaniciens automobile."
            )


class DiagnosticApp:
    # ato moa lefa resaky manova police na couleur interface iny
    def __init__(self, root, user_email, on_logout):
        self.root = root
        self.user_email = user_email
        self.on_logout = on_logout
        self.root.title("Assistant intelligent de diagnostic automobile")

        self.bg_color = "#f7f7f7"
        self.accent_color = "#0b7285"
        self.frame_bg = "#ffffff"
        self.text_color = "#222222"
        self.root.configure(bg=self.bg_color)

        self.title_font = ("Segoe UI", 12, "bold")
        self.label_font = ("Segoe UI", 10)
        self.button_font = ("Segoe UI", 10, "bold") 
        self.text_font = ("Consolas", 9)

        self.checkbox_vars = {}
    # ...existing code...
        self.create_widgets()
#Ato famorona  cadre , case reny, texte libre reny
    def create_widgets(self):
        # bandeau utilisateur + déconnexion
        top_bar = tk.Frame(
            self.root,
            bg=self.bg_color,
        )
        top_bar.pack(fill="x", padx=10, pady=(10, 0))

        label_user = tk.Label(
            top_bar,
            text=f"Connecté : {self.user_email}",
            bg=self.bg_color,
            fg=self.text_color,
            font=self.label_font,
        )
        label_user.pack(side="left")

        btn_logout = tk.Button(
            top_bar,
            text="Déconnexion",
            command=self.handle_logout,
            bg="#c62828",
            fg="white",
            activebackground="#8e0000",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=2,
        )
        btn_logout.pack(side="right")

        # bandeau de titre coloré
        header = tk.Frame(self.root, bg=self.accent_color)
        header.pack(fill="x", padx=0, pady=(5, 10))

        title_lbl = tk.Label(
            header,
            text="Assistant intelligent de diagnostic automobile",
            bg=self.accent_color,
            fg="white",
            font=("Segoe UI", 13, "bold"),
        )
        title_lbl.pack(anchor="w", padx=12, pady=(6, 0))

        subtitle_lbl = tk.Label(
            header,
            text="Analyse des symptômes du véhicule et estimation de la gravité / du coût",
            bg=self.accent_color,
            fg="#e0f7fa",
            font=("Segoe UI", 9),
        )
        subtitle_lbl.pack(anchor="w", padx=12, pady=(0, 6))

        # zone principale en deux colonnes
        content = tk.Frame(self.root, bg=self.bg_color)
        content.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left_pane = tk.Frame(content, bg=self.bg_color)
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 5))

        right_pane = tk.Frame(content, bg=self.bg_color)
        right_pane.pack(side="right", fill="both", expand=True, padx=(5, 0))

        frame_symptoms = tk.LabelFrame(
            left_pane,
            text="Symptômes (cases à cocher)",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.title_font,
        )
        frame_symptoms.pack(fill="x", pady=(0, 8))

        for symptom in SYMPTOMS:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                frame_symptoms,
                text=symptom.capitalize(),
                variable=var,
                bg=self.frame_bg,
                fg=self.text_color,
                font=self.label_font,
                activebackground=self.frame_bg,
            )
            cb.pack(anchor="w", pady=2)
            self.checkbox_vars[symptom] = var

        frame_text = tk.LabelFrame(
            left_pane,
            text="Description libre des symptômes",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.title_font,
        )
        frame_text.pack(fill="both", expand=True)

        self.text_input = tk.Text(
            frame_text,
            height=4,
            font=self.text_font,
        )
        self.text_input.pack(fill="both", expand=True, padx=5, pady=5)

        bottom_left = tk.Frame(left_pane, bg=self.bg_color)
        bottom_left.pack(fill="x", pady=(10, 0))

        btn = tk.Button(
            bottom_left,
            text="Diagnostiquer",
            command=self.run_diagnostic,
            bg=self.accent_color,
            fg="white",
            activebackground="#09506b",
            activeforeground="white",
            font=self.button_font,
            padx=24,
            pady=6,
        )
        btn.pack(pady=0)

        frame_result = tk.LabelFrame(
            right_pane,
            text="Résultat du diagnostic",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.title_font,
        )
        frame_result.pack(fill="both", expand=True)

        self.label_diag = tk.Label(
            frame_result,
            text="Diagnostic : ",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.label_font,
        )
        self.label_diag.pack(anchor="w")

        self.label_gravite = tk.Label(
            frame_result,
            text="Gravité : ",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.label_font,
        )
        self.label_gravite.pack(anchor="w")

        self.label_cout = tk.Label(
            frame_result,
            text="Coût estimatif : ",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.label_font,
        )
        self.label_cout.pack(anchor="w")

        label_exp = tk.Label(
            frame_result,
            text="Explication IA :",
            bg=self.frame_bg,
            fg=self.text_color,
            font=self.label_font,
        )
        label_exp.pack(anchor="w", pady=(10, 0))

        self.text_explication = tk.Text(frame_result, height=8, font=self.text_font)
        self.text_explication.pack(fill="both", expand=True, padx=5, pady=5)

    def handle_logout(self):
        if callable(self.on_logout):
            self.on_logout()

    def run_diagnostic(self):
        selected_symptoms = [
            name
            for name, var in self.checkbox_vars.items()
            if var.get()
        ]
        free_text = self.text_input.get("1.0", tk.END)

        result = diagnose(selected_symptoms, free_text)
        explanation = generate_explanation(
            result,
            selected_symptoms,
            free_text,
        )

        diagnostic = result["diagnostic"]
        gravite = result["gravite"]
        cout_min = result["cout_min"]
        cout_max = result["cout_max"]

        self.label_diag.config(text="Diagnostic : " + diagnostic)
        self.label_gravite.config(text="Gravité : " + gravite)

        if cout_min > 0 or cout_max > 0:
            cout_text = f"Coût estimatif : entre {cout_min} Ar et {cout_max} Ar"
        else:
            cout_text = "Coût estimatif : non défini"

        self.label_cout.config(text=cout_text)

        self.text_explication.delete("1.0", tk.END)
        self.text_explication.insert(tk.END, explanation)


def main():
    root = tk.Tk()
    # Icône de fenêtre (Windows): utiliser des chemins absolus et garder une référence
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 1) Priorité ICO racine (meilleure compat Windows titre + petite icône)
    try:
        ico_root = os.path.join(base_dir, "icon.ico")
        if os.path.exists(ico_root):
            root.iconbitmap(ico_root)
            # on ne return pas: on peut aussi définir une grande icône PNG si dispo
    except Exception:
        pass

    # 2) PNG racine pour grande icône (title bar sur certains systèmes)
    try:
        icon_path = os.path.join(base_dir, "icon.png")
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
        root._icon_img = icon  # garder une référence
    except Exception:
        # 3) Fallback ICO dans assets
        try:
            ico_path = os.path.join(base_dir, "assets", "diagnostic.ico")
            root.iconbitmap(ico_path)
        except Exception:
            # 4) Fallback PNG dans assets
            try:
                png2_path = os.path.join(base_dir, "assets", "diagnostic.png")
                icon2 = tk.PhotoImage(file=png2_path)
                root.iconphoto(True, icon2)
                root._icon_img = icon2
            except Exception:
                pass
    def show_login():
        # nettoie la fenêtre et affiche l'écran de connexion
        for widget in root.winfo_children():
            widget.destroy()

        # callback après succès du login
        def start_app(user_email: str):
            # supprimer les widgets du login et lancer l'app principale
            for widget in root.winfo_children():
                widget.destroy()
            app = DiagnosticApp(root, user_email=user_email, on_logout=show_login)
            root.minsize(600, 500)

        LoginWindow(root, start_app)

    # affiche d'abord l'écran de connexion
    show_login()
    root.mainloop()


if __name__ == "__main__":
    main()
