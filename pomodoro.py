import customtkinter as ctk
import time
import winsound

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro")
        # Tamanho inicial padrão
        self.geometry("450x600")
        
        # AGORA PERMITE AJUSTAR O TAMANHO (True para largura e altura)
        self.resizable(True, True)

        self.work_mins = 25
        self.break_mins = 5
        self.time_left = self.work_mins * 60
        self.timer_running = False
        self.current_mode = "Foco" 
        self.is_pinned = False  

        self.setup_ui()

    def setup_ui(self):
        # Botão de Fixar / Sempre no Topo (Mini Player)
        self.btn_pin = ctk.CTkButton(self, text="📌 Fixar Tela", width=90, height=25, fg_color="#2b2b2b", hover_color="#3a3a3a", command=self.toggle_pin)
        self.btn_pin.pack(anchor="ne", padx=15, pady=15)

        # Título do Modo
        self.lbl_mode = ctk.CTkLabel(self, text="Hora de Focar!", font=("Arial", 28, "bold"), text_color="#3b8ed0")
        self.lbl_mode.pack(pady=(10, 10))

        # Card Central do Timer
        self.timer_frame = ctk.CTkFrame(self, width=320, height=160, corner_radius=20)
        self.timer_frame.pack_propagate(False)
        self.timer_frame.pack(pady=15)

        self.lbl_time = ctk.CTkLabel(self.timer_frame, text=f"{self.work_mins:02d}:00", font=("Arial", 64, "bold"))
        self.lbl_time.place(relx=0.5, rely=0.5, anchor="center")

        # Container de Botões Principais
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        self.btn_start = ctk.CTkButton(self.btn_frame, text="Iniciar", font=("Arial", 16, "bold"), width=130, height=40, command=self.toggle_timer)
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_reset = ctk.CTkButton(self.btn_frame, text="Reiniciar", font=("Arial", 16, "bold"), width=130, height=40, fg_color="#cf6679", hover_color="#b05464", command=self.reset_timer)
        self.btn_reset.grid(row=0, column=1, padx=10)

        # Seção de Configuração
        self.config_frame = ctk.CTkFrame(self, width=360, height=120, corner_radius=15)
        self.config_frame.pack_propagate(False)
        self.config_frame.pack(pady=20)

        self.lbl_config_work = ctk.CTkLabel(self.config_frame, text="Minutos de Foco:", font=("Arial", 12, "bold"))
        self.lbl_config_work.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        self.entry_work = ctk.CTkEntry(self.config_frame, width=100)
        self.entry_work.insert(0, str(self.work_mins))
        self.entry_work.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.lbl_config_break = ctk.CTkLabel(self.config_frame, text="Minutos de Pausa:", font=("Arial", 12, "bold"))
        self.lbl_config_break.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="w")
        self.entry_break = ctk.CTkEntry(self.config_frame, width=100)
        self.entry_break.insert(0, str(self.break_mins))
        self.entry_break.grid(row=1, column=1, padx=20, pady=(0, 20))

        self.btn_apply = ctk.CTkButton(self.config_frame, text="✔ Aplicar", width=70, height=30, fg_color="#2ecc71", hover_color="#27ae60", command=self.apply_custom_times)
        self.btn_apply.grid(row=1, column=2, padx=10, pady=(0, 20))

        # Rodapé
        self.mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.mode_frame.pack(pady=(5, 0))

        self.btn_work_mode = ctk.CTkButton(self.mode_frame, text="🍅 Modo Foco", width=110, height=30, fg_color="#2b2b2b", command=lambda: self.switch_mode("Foco"))
        self.btn_work_mode.grid(row=0, column=0, padx=5)

        self.btn_break_mode = ctk.CTkButton(self.mode_frame, text="☕ Modo Pausa", width=110, height=30, fg_color="#2b2b2b", command=lambda: self.switch_mode("Pausa"))
        self.btn_break_mode.grid(row=0, column=1, padx=5)

    def toggle_pin(self):
        """Alterna entre o modo normal e o modo compacto sempre no topo"""
        if not self.is_pinned:
            self.is_pinned = True
            self.attributes("-topmost", True)  
            
            # Escolha aqui o tamanho do Mini Player (Largura x Altura)
            self.geometry("350x300")           
            
            self.btn_pin.configure(text="📌 Desfixar", fg_color="#1f538d")
            self.config_frame.pack_forget()
            self.mode_frame.pack_forget()
        else:
            self.is_pinned = False
            self.attributes("-topmost", False)
            
            # Escolha aqui o tamanho que ele volta ao desfixar (Largura x Altura)
            self.geometry("450x600")           
            
            self.btn_pin.configure(text="📌 Fixar Tela", fg_color="#2b2b2b")
            self.config_frame.pack(pady=20)
            self.mode_frame.pack(pady=(5, 0))

    def play_alarm_sound(self):
        try:
            for _ in range(3):
                winsound.Beep(1000, 400)
                time.sleep(0.1)
        except:
            self.bell()

    def apply_custom_times(self):
        try:
            self.work_mins = int(self.entry_work.get())
            self.break_mins = int(self.entry_break.get())
            self.reset_timer()
        except ValueError:
            self.entry_work.delete(0, 'end')
            self.entry_work.insert(0, "25")
            self.entry_break.delete(0, 'end')
            self.entry_break.insert(0, "5")

    def update_timer(self):
        if self.timer_running:
            if self.time_left > 0:
                self.time_left -= 1
                mins, secs = divmod(self.time_left, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                self.lbl_time.configure(text=time_str)
                self.title(f"({time_str}) Pomodoro")
                self.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.btn_start.configure(text="Iniciar")
                self.play_alarm_sound()
                if self.current_mode == "Foco":
                    self.switch_mode("Pausa")
                else:
                    self.switch_mode("Foco")

    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.btn_start.configure(text="Pausar", fg_color="#1f538d")
            self.update_timer()
        else:
            self.timer_running = False
            self.btn_start.configure(text="Iniciar", fg_color="#3b8ed0")

    def reset_timer(self):
        self.timer_running = False
        self.btn_start.configure(text="Iniciar", fg_color="#3b8ed0")
        self.time_left = self.work_mins * 60 if self.current_mode == "Foco" else self.break_mins * 60
        mins, secs = divmod(self.time_left, 60)
        self.lbl_time.configure(text=f"{mins:02d}:{secs:02d}")
        self.title("Pomodoro")

    def switch_mode(self, mode):
        self.timer_running = False
        self.current_mode = mode
        self.btn_start.configure(text="Iniciar", fg_color="#3b8ed0")
        
        if mode == "Foco":
            self.time_left = self.work_mins * 60
            self.lbl_mode.configure(text="Hora de Focar!", text_color="#3b8ed0")
            self.lbl_time.configure(text=f"{self.work_mins:02d}:00")
        else:
            self.time_left = self.break_mins * 60
            self.lbl_mode.configure(text="Hora de Relaxar!", text_color="#2ecc71")
            self.lbl_time.configure(text=f"{self.break_mins:02d}:00")
        self.title("Pomodoro")

if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()