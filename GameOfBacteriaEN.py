class Cell:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.age = 0
        self.survival_steps = 0
        self.emoji_font = ("DejaVu Sans Mono", 23)

import random
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import pygame

class SplashScreen:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path

    def show(self, display_duration=3000):
        self.splash = tk.Toplevel(self.root)
        self.splash.overrideredirect(True)
        self.splash.attributes('-topmost', True)

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 600) // 2

        self.splash.geometry(f'625x625+{x}+{y}')

        image = Image.open(self.image_path)
        image = image.resize((625, 625))
        self.photo = ImageTk.PhotoImage(image)
        self.label = tk.Label(self.splash, image=self.photo)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)

        self.root.after(display_duration, self.fade_out)

    def fade_out(self, alpha=1.0, step=0.02, interval=50):
        if alpha > 0:
            self.splash.attributes('-alpha', alpha)
            self.root.after(interval, lambda: self.fade_out(alpha - step, step, interval))
        else:
            self.close()

    def close(self):
        self.splash.destroy()
        
class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#c299c2")
        img_folder = "img"
        image_files = [file for file in os.listdir(img_folder) if file.startswith("splash") and file.endswith((".jpeg", ".jpg", ".png"))]

        if not image_files:
            print("No valid image files found in the 'img' subfolder.")
        else:
            random_image_file = random.choice(image_files)
            random_image_path = os.path.join(img_folder, random_image_file)
            splash = SplashScreen(root, random_image_path)
            splash.show()
        self.emoji_images = {
            "happy": PhotoImage(file="img/antibiotic.png"),
            "angry": PhotoImage(file="img/bacteria.png"),
            "devil": PhotoImage(file="img/resistent.png"),
            "resistance": PhotoImage(file="img/fool.png")
        }
        self.ultratime = 0
        self.sfigamode = ""
        self.motivationcount = 0
        self.black_cells_added = False
        self.is_running = True
        self.infection_started = False
        self.step_counter = 0
        self.blue_cell_added = False
        self.resistence = False
        self.blinking = False
        self.tempo = 4
        self.score = 1000
        self.grid_size = 13
        self.bccount = 1
        self.cell_size = 40
        self.initial_green_cells = 9
        self.initial_black_cells = 0
        self.sfiga = random.randint(1, 10)
        self.ultradose = 0
        self.ultradosemse = ""
        pygame.mixer.init()
        pygame.init()
        background_image = Image.open("img/background.jpeg")
        self.background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        root.configure(bg="")
        self.ambient_sound = pygame.mixer.Sound("sounds/ambient.mp3")
        self.ambient_sound.set_volume(0.65)
        self.ambient_channel = self.ambient_sound.play(loops=-1)
        
        if not self.resistence:
            self.track_sound = pygame.mixer.Sound("sounds/track.wav")
            self.track_sound.set_volume(0.4)
            self.track_channel = self.track_sound.play(loops=-1)
            self.control = True

        self.bacteria_names = [
            "Staphylococcus aureus", "Escherichia coli", "Salmonella", "Streptococcus pneumoniae", "Mycobacterium tuberculosis", "Clostridium difficile", "Helicobacter pylori", "Neisseria gonorrhoeae", "Bacillus anthracis", "Yersinia pestis", "Listeria monocytogenes", "Vibrio cholerae", "Pseudomonas aeruginosa", "Campylobacter jejuni", "Chlamydia trachomatis", "Treponema pallidum", "Legionella pneumophila", "Borrelia burgdorferi", "Mycoplasma pneumoniae", "Bordetella pertussis", "Haemophilus influenzae", "Enterococcus faecalis", "Klebsiella pneumoniae", "Acinetobacter baumannii", "Shigella", "Enterobacter cloacae", "Proteus mirabilis", "Mycobacterium leprae", "Francisella tularensis", "Brucella", "Mycobacterium avium", "Clostridium perfringens", "Clostridium botulinum", "Actinomyces israelii", "Corynebacterium diphtheriae", "Erysipelothrix rhusiopathiae", "Lactobacillus", "Listeria", "Shigella flexneri", "Shigella sonnei", "Proteus vulgaris", "Proteus penneri", "Morganella morganii", "Edwardsiella tarda", "Klebsiella oxytoca", "Klebsiella granulomatis", "Klebsiella rhinoscleromatis", "Serratia marcescens", "Yersinia enterocolitica", "Yersinia pseudotuberculosis"
        ]
        self.root.title("Bacteria versus Antibiotics - ©2023 Davide")
        frame = tk.Frame(root, borderwidth=5, relief="ridge", bg="black", padx=2, pady=2)
        frame.pack()

        self.count_label = tk.Label(frame, text="Press 'Start' to go.", font=("Helvetica", 20, "bold"), fg="white", bg="black")
        self.count_label.pack()
        self.green_cells = []
        self.black_cells = []
        self.blue_cells = []
        self.frame = tk.Frame(root, borderwidth=1, relief="solid")
        self.frame.pack(padx=5, pady=5)
        self.symptoms_label = tk.Label(
            self.frame,
            text="Bacteria found their way in...",
            font=("Helvetica", 16),
            fg="black"
        )        


        self.symptoms_label.pack(padx=2, pady=2)
        self.canvas = tk.Canvas(
            root, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size,
        )
        self.canvas.pack(pady=10)
        self.coughing_sound = pygame.mixer.Sound("sounds/coughing.mp3")
        self.laugh_sound = pygame.mixer.Sound("sounds/laugh.mp3")

        self.draw_grid()
        
        self.play_button = tk.Button(
            root, text=" Start ", command=self.start_simulation, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.play_button.pack(side=tk.LEFT, ipady=5)
        self.pause_button = tk.Button(
            root, text=" Resume ", command=self.toggle_pause, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.pause_button.config(text=" Pause ")

        self.pause_button.pack(side=tk.LEFT, ipady=5)
        self.paused = False
        self.reset_button = tk.Button(
            root, text=" Reset ", command=self.reset_simulation, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.reset_button.pack(side=tk.LEFT, ipady=5)
        self.add_black_cells_button = tk.Button(
            root, text=" Antibiotic ", command=self.add_black_cells, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.add_black_cells_button.pack(side=tk.LEFT, ipady=5)
        self.resistance_button = tk.Button(
            root, text=" resistance ", command=self.add_blue_cell, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.resistance_button.pack(side=tk.LEFT, ipady=5)
        
        self.help_button = tk.Button(
            root, text=" Help ", command=self.show_help_window, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.help_button.pack(side=tk.RIGHT, ipady=5)
        
        self.audio_button = tk.Button(
            root, text=" Music ", command=self.stop_sound_channels, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6")
        self.audio_button.config(fg="black")
        self.audio_button.pack(side=tk.RIGHT, ipady=5)

        self.root.bind("<Return>", self.on_enter_press)
        self.root.bind("<Escape>", self.on_esc_press)
        self.root.bind("<space>", self.on_space_press)
        self.initialize_cells()
        self.draw_cells()
        self.bells_sound = pygame.mixer.Sound("sounds/bells.mp3")
        self.gulp_sound = pygame.mixer.Sound("sounds/gulp.mp3")
        self.berries_sound = pygame.mixer.Sound("sounds/berries.mp3")
        self.cough_sound = pygame.mixer.Sound("sounds/cough.mp3")
        self.beep_sound = pygame.mixer.Sound("sounds/beep.mp3")
        self.death_sound = pygame.mixer.Sound("sounds/death.mp3")
        self.thanks_sound = pygame.mixer.Sound("sounds/thankyou.mp3")
        self.ok_sound = pygame.mixer.Sound("sounds/ok.mp3")
        self.poof_sound = pygame.mixer.Sound("sounds/poof.mp3")
        self.deadbac_sound = pygame.mixer.Sound("sounds/deadbac.mp3")
        self.breath_sound = pygame.mixer.Sound("sounds/breath.mp3")
        self.boss_sound = pygame.mixer.Sound("sounds/boss.mp3")
        self.idiot_sound = pygame.mixer.Sound("sounds/idiot.mp3")
        self.crowd_sound = pygame.mixer.Sound("sounds/crowd.mp3")

        self.avvio = False
        self.avviso = False
        self.avviso2 = False
        self.antanimessage = ""
        self.resmes = ""
        self.breath = False
        self.breath1 = False
        self.breath2 = False
        self.breath3 = False

        self.sintomi = False
        self.center_window(self.root)
        self.simulate_step()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_simulation()
        else:
            self.resume_simulation()

    def pause_simulation(self):
        self.is_running = False
        self.pause_button.config(text=" Resume ")

    def resume_simulation(self):
        self.is_running = True
        self.simulate_step()
        self.pause_button.config(text=" Pause ")

    def stop_sound_channels(self):
        self.ambient_channel.stop()
        self.track_channel.stop()

    def on_space_press(self, event):
        self.add_blue_cell()

    def on_esc_press(self, event):
        self.reset_simulation()

    def on_enter_press(self, event):
        self.add_black_cells()

    def update_symptoms_label(self):
            total_colored_cells = len(self.green_cells) + len(self.blue_cells)
            total_black_cells = len(self.black_cells)
            colored_cell_percentage = total_colored_cells / (
                self.grid_size * self.grid_size
            )
            if self.is_running:
                if self.tempo > 0 and self.tempo < 20:
                    if not self.avvio:
                        self.update_count_label()
                        self.avvio = True
                        self.symptoms_label.config(text="Bacteria are building a colony... wait for infection.", fg="brown")

            if total_colored_cells < 20:
                if self.blinking:
                    self.blinking = False
                    self.update_count_label()
                    self.symptoms_label.config(text="Sympthoms under control!", fg="green")
                    self.score += 15

            bacteria_symptoms = [
                "has fever", 
                "has strong pain", 
                "is fatigued", 
                "can't eat!", 
                "is spreading nasty fluids...",
                "has sympthoms", 
                "has sympthoms",
                "has sympthoms",
                "has sympthoms", 
                "has sympthoms",
                "has sympthoms", 
                "has sympthoms", 
                "has sympthoms", 
                "has sympthoms",
                "has sympthoms", 
                "has sympthoms", 
                "has sympthoms", 
                "has sympthoms", 
                "has sympthoms", 
                "has sympthoms", 
            ]

            if total_colored_cells > 20 and total_black_cells <= 20:
                self.score -= 20
                
                if self.sintomi:
                    random_symptom = random.choice(bacteria_symptoms)
                    self.update_count_label()
                    symptoms_text = f"Patient {random_symptom}"
                    self.symptoms_label.config(text=symptoms_text, fg="red")
                    self.sintomi = False
                else:
                    self.sintomi = True
                    self.update_count_label()

            if total_black_cells >= 15 < 20:
                if not self.blinking:
                    self.blinking = True
                    self.blink_symptoms_label()
                    self.update_count_label()
                    self.symptoms_label.config(
                        text="Dose is high! Be careful!", fg="red"
                    )
                    if self.resistence:
                        self.score -= 100
                    else:
                        self.score -= 80
                    
            if total_black_cells >= 20:
                if not self.blinking:
                    self.blinking = True
                    self.blink_symptoms_label()
                    self.update_count_label()
                self.symptoms_label.config(
                    text="That's too much! We are overdosing!", fg="red"
                )
                self.ultradose += 1
                if self.breath1:
                    self.breath_sound.play()
                    self.breath1 = False
                else:
                    self.breath1 = True
                    
                if self.resistence:
                    self.score -= 280
                else:
                    self.score -= 200

            if self.score < -1500:
                self.show_patient_death_notification2()

            if self.tempo > 600:
                self.show_patient_death_notification3()
                
            if self.tempo > 40:    
                if total_black_cells < 1:
                    self.score -= 100

            if self.tempo > 300 and self.tempo < 380:
                if not self.blue_cell_added:
                    if not self.avviso:
                        self.avviso = True
                        if not self.blinking:
                            self.blinking = True
                            self.blink_symptoms_label()
                        self.symptoms_label.config(
                            text="Terapy is getting too long!", fg="red"
                        )
                        self.cough_sound.play()

            if self.blue_cell_added:
                if not self.avviso2:
                    self.avviso2 = True
                    if not self.blinking:
                        self.blinking = True
                        self.blink_symptoms_label()
                    self.symptoms_label.config(
                        text="Oops... resistance building up!", fg="red"
                    )
                    self.cough_sound.play()

            phrases = [
                "Sepsis risk is high!",
                "Infection is spreading alarmingly!"
            ]

            random_phrase = random.choice(phrases)

            if colored_cell_percentage > 0.4 < 0.45:
                if not self.blinking:
                    self.blinking = True
                    self.blink_symptoms_label()
                self.symptoms_label.config(text=random_phrase, fg="red")
                self.beep_sound.play()
                self.score -= 80
                self.breath2 = True
                if self.breath2:
                    self.berries_sound.play()
                    self.breath2 = False 
                else:
                    self.breath2 = True            
            else:            
                if self.tempo > 80 and colored_cell_percentage < 0.55:
                    if total_black_cells < 3:
                        self.breath3 = True
                        if not self.blinking:
                            self.blinking = True
                            self.blink_symptoms_label()
                        self.symptoms_label.config(
                            text="Administer an antibiotic dose, patient is sick!", fg="red"
                        )
                        if self.breath3:
                            self.breath_sound.play()
                            self.breath3 = False
                        else:
                            self.breath3 = True
                            
            if colored_cell_percentage > 0.45:
                if not self.blinking:
                    self.blinking = True
                    self.blink_symptoms_label()
                self.symptoms_label.config(text="Patient is critical!", fg="red")
                self.cough_sound.play()
                self.score -= 100
                if self.breath:
                    self.berries_sound.play()
                    self.breath = False
                else:
                    self.breath = True
                                                
    def blink_symptoms_label(self):
        if self.blinking:
            self.symptoms_label.config(fg="red")
            self.root.after(500, self.stop_blink_symptoms_label)

    def stop_blink_symptoms_label(self):
        if self.blinking:
            self.symptoms_label.config(fg="blue")
            self.root.after(500, self.blink_symptoms_label)

    def update_count_label(self):
        total_colored_cells = len(self.green_cells) + len(self.blue_cells)
        days = int(self.tempo / 24)
        self.count_label.config(
            text=f"    Points: {self.score}   •   Infection: {total_colored_cells}%   •   Day: {days}    ")
 
    def initialize_cells(self):
        self.play_button.configure(fg="red")
        for _ in range(self.initial_green_cells):
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.green_cells.append(Cell(row, col, "#024002"))
            
        for _ in range(self.initial_black_cells):
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.black_cells.append(Cell(row, col, "black"))

    def draw_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, outline="", fill="#8c6f8c"
                )
        border_width = 1
        self.canvas.create_rectangle(
            border_width, border_width, self.grid_size * self.cell_size - border_width, self.grid_size * self.cell_size - border_width, outline="black", width=border_width,
        )



    def show_motivation(self):
        self.is_running = False
        self.info_window = tk.Toplevel(self.root, background="#c299c2")
        self.info_window.title("")
        self.info_window.overrideredirect(True)
        message = (
            f"Patient has extra motivation!\n\n"
            f"You get +2000 points!\n\n"
            "Go forward diligently, and don't disappoint him!"
        )
        info_label = tk.Label(
            self.info_window, text=message, padx=10, pady=10, font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
        )
        info_label.pack()

        certo_button = tk.Button(
            self.info_window, text="My honour!", command=self.close_motivation_window_and_continue,
            padx=10, pady=10, font=("DejaVu Sans Mono", 13, "bold")
        )
        certo_button.pack()
        
        self.center_window(self.info_window)

    def close_motivation_window_and_continue(self):
        self.info_window.destroy()
        self.is_running = True
        self.simulate_step()
                
    def show_infection_notification(self):
        if len(self.green_cells) >= self.grid_size * self.grid_size * 0.17:
            if not self.infection_started:
                self.infection_started = True
                self.is_running = False
                self.info_window = tk.Toplevel(self.root, background="#c299c2")
                self.info_window.title("")
                self.info_window.overrideredirect(True)
                random_bacteria = random.choice(self.bacteria_names)
                bacteria_name_for_url = random_bacteria.replace(" ", "_")
                wikipedia_url = f"https://en.wikipedia.org/wiki/{bacteria_name_for_url}"
                if not self.resistence:
                    message = (
                        f"Patient shows first signs of infection from\n\n"
                        f"{random_bacteria}\n\n{self.sfigamode}\n\n"
                        "We need antibiotics\nyou know what i mean?"
                    )
                else:
                    message=(
                        f"You got lab results:\n\n"
                        f"{random_bacteria}\n and resistent to antibiotics!\n\n{self.sfigamode}\n\n"
                        "We need to start a strong therapy\nfor this guy!\nYou know what to do, right?"
                    )                    
                info_label = tk.Label(
                    self.info_window, text=message, padx=10, pady=10, font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
                )
                info_label.pack()

                non_so_button = tk.Button(
                    self.info_window, text="Know anything!", command=lambda: self.show_antibiotics_info(self.info_window), padx=10, pady=10, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
                )
                non_so_button.pack()
                certo_button = tk.Button(
                    self.info_window, text="Of course, let's go!", command=lambda: self.close_info_window_and_continue(
                        self.info_window
                    ), padx=10, pady=10, font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
                )
                certo_button.pack()
                bacteria_label = tk.Label(
                    self.info_window, text=f"\n(Read {random_bacteria} on Wikipedia!)\n\n", font=("DejaVu Sans Mono", 13, "bold"), cursor="hand2", 
                    fg="blue", background="#c299c2"
                )
                import webbrowser
                bacteria_label.bind("<Button-1>", lambda event, url=wikipedia_url: webbrowser.open_new_tab(url))
                bacteria_label.pack()
                self.center_window(self.info_window)
                self.cough_sound.play()

    def close_info_window_and_continue(self, window):
        self.ok_sound.play()
        window.destroy()
        self.resume_simulation()

    def show_antibiotics_info(self, prev_window):
        prev_window.destroy()  # Close the previous window.
        antibiotics_info_window = tk.Toplevel(self.root, background="#c299c2") 
        antibiotics_info_window.title("Information about Antibiotics")
        info_message = (
            "Antibiotics are medicines used to\ncombat bacterial infections.\n\n"
            "They should only be administered when necessary\nand following doctor's instructions.\n\n"
            "Improper use can lead to bacterial resistance,\n"
            "making bacteria less sensitive to antibiotics.\n\n"
            "To eradicate resistant bacteria, more antibiotics\n"
            "or stronger antibiotics are needed, which can cause side effects.\n\n"
            "Excessive doses of antibiotics can be harmful,\n"
            "especially if you have other conditions (e.g., renal).\n\n"
            "Right antibiotic, at the right dose, and\nat the right time can help fight infection,\n"
            "but it's important to use them responsibly to avoid problems.\n\n"
            "Choose wisely!"
        )

        info_label = tk.Label(
            antibiotics_info_window,
            text=info_message,
            padx=20,
            pady=20,
            font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2")
        
        info_label.pack()
        ok_button = tk.Button(
            antibiotics_info_window,
            text="Ready to fight!",
            command=lambda: self.close_antibiotics_info(antibiotics_info_window),
            font=("DejaVu Sans Mono", 13, "bold"),
        )
        ok_button.pack()
        self.center_window(antibiotics_info_window)

    def close_antibiotics_info(self, window):
        window.destroy()
        self.ok_sound.play()
        self.resume_simulation()

    def add_black_cells(self):
        
        if not (self.black_cells or self.blue_cells) and len(self.green_cells) < 35:
            return
        else:
            self.bccount +=1

        self.random_black = random.randint(1, 100)
        self.random_black_number = random.randint(1, 15)
        
        if self.random_black <= 30:
            num_black_cells_to_add = self.random_black_number
        else:                
            days = self.tempo / 24
            if days <= 2:
                num_black_cells_to_add = 4
            if days > 2 <= 10:
                num_black_cells_to_add = 8
            if days > 10:
                num_black_cells_to_add = 2

                    
        if self.sfiga >= 1 < 2: # tanta sfiga
            self.score -= 30
        else:
            self.score -= 20
            
        num_direct_colored_spawns = int(num_black_cells_to_add * 0.15)

        for _ in range(num_direct_colored_spawns):
            colored_cell = random.choice(self.green_cells + self.blue_cells)
            self.black_cells.append(Cell(colored_cell.row, colored_cell.col, "#4d4c4c"))

        for _ in range(num_black_cells_to_add - num_direct_colored_spawns):
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            
            # Simulate the therapy error with a 2% chance
            if random.random() < 0.02:
                if self.tempo > 200 :
                    self.black_cells.append(Cell(row, col, "#fc035a"))
                    self.black_cells.append(Cell(row, col, "#fc035a"))
                    self.black_cells.append(Cell(row, col, "#fc035a"))
                    self.black_cells.append(Cell(row, col, "#fc035a"))
                    self.black_cells.append(Cell(row, col, "#fc035a"))                    
                    self.symptoms_label.config(text="You gave the wrong antibiotic!", fg="red")
                    self.blinking = True
                    self.blink_symptoms_label()
                    self.idiot_sound.play()
                    self.score -= -50
            else:
                self.black_cells.append(Cell(row, col, "#4d4c4c"))


                
        self.black_cells_added = True
        self.draw_cells()
        self.gulp_sound.play()

    def add_blue_cell(self):
        from tkinter import messagebox
        if not self.blue_cell_added:
            new_row = random.randint(0, self.grid_size - 1)
            new_col = random.randint(0, self.grid_size - 1)
            self.blue_cells.append(Cell(new_row, new_col, "#662d59"))
            self.laugh_sound.play()
            self.score -= 5
            self.blue_cell_added = True
            self.draw_cells()
            self.resistance_button.config(fg="red")
            self.resistence = True
            self.update_count_label

    def duplicate_blue_cells(self):
        new_blue_cells = []
        for blue_cell in self.blue_cells:
            possible_moves = self.get_valid_moves(blue_cell.row, blue_cell.col)
            if possible_moves:
                new_row, new_col = random.choice(possible_moves)
                new_blue_cells.append(Cell(new_row, new_col, "#662d59"))
                break
        self.blue_cells += new_blue_cells
        self.score -= 2
        self.update_count_label

    def simulate_step(self):
        pygame.mixer.init()
        pygame.init()
        if self.resistence:
            if self.control:
                self.stop_sound_channels()
                self.track_sound = pygame.mixer.Sound("sounds/trackres.wav")
                self.track_sound.set_volume(0.4)
                self.track_channel = self.track_sound.play(loops=-1)
                self.control = False
            
        self.update_count_label()
        if self.paused:
            return
        if not self.infection_started:
            self.show_infection_notification()
        self.remove_smilies_from_white_cells()
        self.remove_frozen_yellow_cells()
        self.move_cells()
        self.check_collisions()
        black_cell_percentage = len(self.black_cells) / (
            self.grid_size * self.grid_size
        )
        if black_cell_percentage >= 0.18:
            self.score -= 5000
            self.update_count_label
            self.is_running = False
            self.show_patient_death_notification()
            return
        self.step_counter += 1
        self.score += 15
        if self.step_counter == 2:
            self.step_counter = 0
            days = self.tempo / 24
            if days > 1 < 8:
                self.duplicate_green_cell()
                self.duplicate_green_cell()
                self.duplicate_green_cell()
                self.duplicate_green_cell()
                self.duplicate_green_cell()

            if days > 10 and self.black_cells_added < 5:
                self.duplicate_green_cell()

                
            total_colored_cells = len(self.green_cells) + len(self.blue_cells)


            self.update_count_label

            if self.sfiga >= 1 < 2: # tanta sfiga
                self.sfigamode = "Hard case:\npatient immune system\nis compromised! Be careful!"
                self.duplicate_green_cell()
                self.duplicate_green_cell()
                self.duplicate_green_cell()                
                self.duplicate_green_cell()
                self.duplicate_green_cell()
                self.duplicate_blue_cells()
                self.duplicate_blue_cells()

                if self.black_cells_added < 7:
                    self.duplicate_green_cell()
                    self.duplicate_green_cell()
                    self.duplicate_green_cell()
                    
                if total_colored_cells >= 35:
                    self.duplicate_green_cell()
                    self.duplicate_green_cell()
                    self.duplicate_green_cell()
                
            if self.sfiga > 2 < 3: # botta di culo
                self.duplicate_green_cell()
                self.duplicate_blue_cells()

                self.sfigamode = "Easy case:\npatient has a super immune system!\nEasy peasy!"

            if self.sfiga >= 3: # comportamento normale
                self.sfigamode = "Routine case:\npatient has normal immune system\nbut you should stay careful!"
                self.duplicate_green_cell()
                self.duplicate_green_cell()

                if total_colored_cells >= 35:
                    self.duplicate_green_cell()

            if self.motivationcount < 2:
                if self.resistence:
                    random_chance = random.randint(1, 100)
                    if random_chance <= 5:
                        self.show_motivation()
                        self.score += 2000
                        self.motivationcount += 1     
                else:        
                    if self.motivationcount <= 2:
                        random_chance = random.randint(1, 100)
                        if random_chance < 2:
                            self.show_motivation()
                            self.score += 2000
                            self.motivationcount += 1 
    

            self.update_count_label
                
        if random.random() < 1 and self.black_cells:
            cell_to_die = random.choice(self.black_cells)
            if any(
                abs(cell_to_die.row - blue_cell.row) <= 1
                and abs(cell_to_die.col - blue_cell.col) <= 1
                for blue_cell in self.blue_cells
            ):
                self.blue_cells.pop(0)
            self.black_cells.remove(cell_to_die)
        if not self.black_cells and self.black_cells_added:
            self.black_cells_added = False
            self.add_blue_cell()
        for blue_cell in self.blue_cells:
            neighbors = self.get_neighbors(blue_cell.row, blue_cell.col)
            black_neighbors = sum(
                1 for row, col in neighbors if self.is_black(row, col)
            )
            if black_neighbors >= 2:
                self.blue_cells.remove(blue_cell)
                for row, col in neighbors:
                    if self.is_black(row, col):
                        for black_cell in self.black_cells:
                            if black_cell.row == row and black_cell.col == col:
                                self.poof_sound.play()
                                black_cell.color = "yellow"
                                black_cell.is_flashing = True
                                self.score += 100
                                break
        self.draw_cells()
        self.update_symptoms_label()
        if self.tempo > 4:
            self.check_patient_health()
        self.tempo += 4
        self.score = int(self.score - (self.tempo / 3))
        if self.is_running and (len(self.green_cells) + len(self.blue_cells) > 0):
            self.check_patient_sepsis()
        if self.tempo > 400:
            if not self.resistence:
                self.add_blue_cell()
                self.resistence = True
        if self.is_running:
            self.root.after(1000, self.simulate_step)
        self.play_button.configure(fg="Green")

    def remove_frozen_yellow_cells(self):
        new_black_cells = []
        for cell in self.black_cells:
            if cell.color == "yellow" and cell.is_flashing:
                cell.is_flashing = False
                cell.color = "#4d4c4c"
                self.draw_cells()
            new_black_cells.append(cell)
        self.black_cells = new_black_cells

    def get_neighbors(self, row, col):
        neighbors = []
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (
                    0 <= r < self.grid_size
                    and 0 <= c < self.grid_size
                    and (r != row or c != col)
                ):
                    neighbors.append((r, c))
        return neighbors

    def is_black(self, row, col):
        return any(cell.row == row and cell.col == col for cell in self.black_cells)

    def draw_cells(self):
        self.canvas.delete("cells")
        for cell in self.green_cells + self.black_cells + self.blue_cells:
            color = cell.color
            x1 = cell.col * self.cell_size
            y1 = cell.row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.probability = 5
            random_number = random.randint(1, 100)
            if random_number <= self.probability and self.tempo == 4:
                if not self.is_running:
                    self.symptoms_label.config(
                        text="You have admitted a patient with resistance!\nStart treatment immediately while waiting for lab results!", fg="red"
                    )
                    self.coughing_sound.play()
                    self.add_blue_cell()
            emoji = "resistance"
            
            if color == "#024002":
                emoji = "angry"
            elif color == "#4d4c4c":
                emoji = "happy"
            elif color == "#662d59" and self.blue_cell_added:
                emoji = "devil"
            
            self.canvas.create_oval(
                x1, y1, x2, y2, fill=color, outline="black", tags="cells"
            )
            
            if color == "#4d4c4c":
                self.canvas.create_oval(
                    x1 + self.cell_size // 4, y1 + self.cell_size // 4, x2 - self.cell_size // 4, y2 - self.cell_size // 4, fill="white", outline="white", tags="cells"
                )
                
            emoji_image = self.emoji_images[emoji]
            self.canvas.create_image(
                x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=emoji_image, tags="cells"
            )

    def remove_smilies_from_white_cells(self):
        for cell in self.black_cells:
            if cell.color == "black" and cell.age > 0:
                cell.age = 0
                self.draw_cells()
                
    def show_patient_death_notification2(self):
        self.stop_sound_channels()
        self.is_running = False
        death_window = tk.Toplevel(self.root, background="#c299c2")
        death_window.title("")
        death_window.overrideredirect(True)
        message = f"You've messed up the treatment, {self.bccount} doses!\n\nYour boss has run out of patience; you'll have to find another job...\n\nNow your patient is in better hands, and maybe they'll survive...\n\nYou've earned {self.score} points.\n\nEmbarrassing..."
        death_label = tk.Label(
            death_window,
            text=message,
            padx=20,
            pady=20,
            font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
        )
        self.boss_sound.play()
        death_label.pack()
        ok_button = tk.Button(
            death_window,
            text="Ooops...",
            command=lambda: self.reset_simulation(),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        ok_button.pack()
        self.center_window(death_window)

    def show_patient_death_notification3(self):
        self.symptoms_label.config(
        text="Patient has died due to complications!"

, fg="red", background="#c299c2"
        )
        self.stop_sound_channels()
        self.bells_sound.play()
        self.death_sound.play()
        death_window = tk.Toplevel(self.root, background="#c299c2")
        death_window.title("")
        death_window.overrideredirect(True)
        days = int(self.tempo / 24)
        message = f"After {self.tempo} hours of treatment, patient didn't make it!\n\nTreatment lasted for about {days} days, and severe complications arose\nafter administering {self.bccount} doses!\n\nYou receive a penalty of 5000 points!\nBe aware, boss is keeping an eye on you...\n\nFinal score: {self.score}"
        death_label = tk.Label(
            death_window,
            text=message,
            padx=20,
            pady=20,
            font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
        )
        death_label.pack()
        ok_button = tk.Button(
            death_window,
            text="Ooops...",
            command=lambda: self.reset_simulation(),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        ok_button.pack()
        self.center_window(death_window)
               
    def show_patient_death_notification(self):
        self.symptoms_label.config(
        text="Patient died of overdose!", fg="red"
        )
        self.stop_sound_channels()
        self.bells_sound.play()
        self.death_sound.play()
        death_window = tk.Toplevel(self.root, background="#c299c2")
        death_window.title("")
        death_window.overrideredirect(True)
        days = int(self.tempo / 24)
        message = f"You killed the patient with {self.bccount} lethal doses in just {self.tempo} hours!\n\nIt took you about {days} days to do it!\n\nWait for the antibiotic to take effect before administering more!\n\nYou receive a penalty of 5000 points!\nBe aware, boss is keeping an eye on you...\n\nFinal score: {self.score}"
        death_label = tk.Label(
            death_window,
            text=message,
            padx=20,
            pady=20,
            font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
        )
        death_label.pack()
        ok_button = tk.Button(
            death_window,
            text="Ooops...",
            command=lambda: self.reset_simulation(),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        ok_button.pack()
        self.center_window(death_window)

    def close_death_window(self, window):
        window.destroy()

    def show_patient_health_notification(self):
        self.stop_sound_channels()
        self.crowd_sound.play()
        self.symptoms_label.config(
        text="Patient is back to health! Congratulations!", fg="red"
        )
        self.score += 4000
        self.update_count_label()
        if self.resistence:
            self.resmes = "Congratulations, you defeated resistance! (+5000 punti)\n"
            self.score += 5000 
        health_window = tk.Toplevel(self.root, background="#c299c2")
        health_window.title("")
        health_window.overrideredirect(True)
        days = self.tempo / 24
        if days < 5:
            self.antanimessage = f"{self.resmes}Easy, isn't it? Can you do it again? (+1000 bonus tempo)"
            self.score += 1000 
        if days > 5 < 8:
            self.antanimessage = f"{self.resmes}Illness gave you a hard time,\nbut you handled it great! (+500 time bonus)"
            self.score += 500 
        if days > 8 < 12:
            self.antanimessage = f"{self.resmes}You were about to make a mess,\nbut you saved the patient! (+250 time bonus)"
            self.score += 250
        if days > 12:
            self.antanimessage = f"{self.resmes}You saved him by accident, but just consider the result... (+125 time bonus)"
            self.score += 125
        self.ultratime = self.ultradose * 4

        if not self.resistence:
            if self.ultradose > 100:
                self.ultradosemse = f"You administered {self.ultratime} hours of lethal doses to patient,\ntake it easy next time! (-100 points)."
                self.score -= 100
            else:
                self.ultradosemse = f"Your boss seems satisfied with the therapy you chose,\nbut still suspects a lot about you..."

        else:
            if self.ultradose > 200:
                self.ultradosemse = f"You administered {self.ultratime} hours of lethal doses to the person, take it easy! (-100 points)"
                self.score -= 100
            else:
                self.ultradosemse = f"Your boss seems satisfied with the therapy you have chosen,\nbut still suspects a lot about you..."
    
        self.update_count_label()
        days = int(self.tempo / 24)
        message = f"The patient has recovered!\nInfection was eradicated after {self.tempo} hours (approximately {days} days) and {self.bccount} doses!\n\n{self.antanimessage}\n\n{self.ultradosemse}\n\nYou have received a promotion and a bonus of 4000 points!\n\nUpdated score: {self.score}"
        health_label = tk.Label(
            health_window,
            text=message,
            padx=20,
            pady=20,
            font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
        )
        health_label.pack()
        ok_button = tk.Button(
            health_window,
            text="Great!",
            command=lambda: self.reset_simulation(),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        self.thanks_sound.play()
        ok_button.pack()
        self.center_window(health_window)

    def close_health_window(self, window):
        window.destroy()

    def show_patient_sepsis_notification(self):
        self.symptoms_label.config(
        text="Patient died of infection!", fg="red"
        )
        self.stop_sound_channels()
        self.score -= 5000
        self.bells_sound.play()
        self.death_sound.play()
        self.update_count_label()
        sepsis_window = tk.Toplevel(self.root, background="#c299c2")
        sepsis_window.title("")
        sepsis_window.overrideredirect(True)
        days = int(self.tempo / 24)
        message = f"Patient died of infection in just {self.tempo} hours (approximately {days} days)!\n\nYou didn't administer antibiotics (only {self.bccount} doses), where was your head?\n\nDon't interrupt the therapy and always try to administer enough!\n\nYou receive a penalty of 4000 points!\n\nFinal score: {self.score}"
        sepsis_label = tk.Label(
            sepsis_window,
            text=message,
            padx=20,
            pady=20,
            font=("DejaVu Sans Mono", 13, "bold"), background="#c299c2"
        )
        sepsis_label.pack()
        ok_button = tk.Button(
            sepsis_window,
            text="Who's next?",
            command=lambda: self.reset_simulation(),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        ok_button.pack()
        self.center_window(sepsis_window)

    def close_sepsis_window(self, window):
        window.destroy()

    def start_simulation(self):
        if not self.is_running:
            self.is_running = True
            self.simulate_step()

    def reset_simulation(self):
        self.stop_sound_channels()
        self.root.destroy()
        root = tk.Tk()
        root.geometry("800x680") 

        app = GridApp(root)
        root.mainloop()

    def duplicate_green_cell(self):
        self.score -= 2

        if self.green_cells:
            cell_to_duplicate = random.choice(self.green_cells)
            possible_moves = self.get_valid_moves(
                cell_to_duplicate.row, cell_to_duplicate.col
            )
            unoccupied_moves = [
                move
                for move in possible_moves
                if move not in [(cell.row, cell.col) for cell in self.green_cells]
            ]
            if unoccupied_moves:
                new_row, new_col = random.choice(unoccupied_moves)
                self.green_cells.append(Cell(new_row, new_col, "#024002"))
        self.update_count_label

    def move_cells(self):
        for cell in self.green_cells + self.black_cells + self.blue_cells:
            possible_moves = self.get_valid_moves(cell.row, cell.col)
            if possible_moves:
                new_position = random.choice(possible_moves)
                cell.row, cell.col = new_position
                cell.age += 1
                if cell.color == "#662d59":
                    cell.survival_steps += 1

    def check_collisions(self):
        new_green_cells = []
        new_blue_cells = []
        for green_cell in self.green_cells:
            is_colliding = any(
                abs(green_cell.row - black_cell.row) <= 1
                and abs(green_cell.col - black_cell.col) <= 1
                for black_cell in self.black_cells
            )
            if not is_colliding:
                new_green_cells.append(green_cell)
            if is_colliding:
                self.score += 25
                self.deadbac_sound.play()
        for blue_cell in self.blue_cells:
            new_blue_cells.append(blue_cell)
        self.green_cells = new_green_cells
        self.blue_cells = new_blue_cells

    def get_valid_moves(self, row, col):
        moves = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        valid_moves = []
        for r, c in moves:
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                valid_moves.append((r, c))
        return valid_moves

    def check_patient_health(app):
        if len(app.green_cells) <= 2 and len(app.blue_cells) <= 2:
            app.is_running = False
            app.show_patient_health_notification()

    def check_patient_sepsis(app):
        colored_cell_percentage = (len(app.green_cells) + len(app.blue_cells)) / (
            app.grid_size * app.grid_size
        )
        if (
            colored_cell_percentage >= 0.65
            and (len(app.green_cells) + len(app.blue_cells)) > 0
        ):
            app.is_running = False
            app.show_patient_sepsis_notification()
            
    def show_disclaimer_window(self):
        disclaimer_window = tk.Toplevel(self.root, background="#c299c2")
        disclaimer_window.title("Disclaimer")
        self.is_running = False
        disclaimer = (
            "This software is provided 'as is,' without any warranty, express or implied, about its operation.\n\n"
            "The use of this software is at your own risk. Author assumes no responsibility for direct, indirect, incidental, or consequential damages resulting from the use, whether proper or improper, of this software.\n\n"
            "By continuing to use this software, user agrees to be bound by the terms of this disclaimer.\n\n"
            "Source code of this software is distributed under the GPL-3.0 license, excluding audio effects and icons:\n"
            "https://www.gnu.org/licenses/gpl-3.0.en.html\n\n"
            "Notes:\n- Audio effects used in this software come from free sources found on YouTube, either without a license or under Creative Commons license (creativecommons.org).\n- Music is generated with Beatoven.ai and used with a valid worldwide license.\n"
            "- Programmed in Python language.\n\n"
            "Purpose of the software is to entertain and, at most, to help understand the behavior of bacteria and antibiotics in an enjoyable way.\n\nSimulations in this game are quite realistic but can still be influenced by random events (for entertainment purposes), and may not always represent real treatment situations or real situations in general.\n\nIt is the responsibility of the teacher and an exercise for the student to understand when the outcome of a game can be compared with real events to stimulate further exploration.\n\nSoftware developer does not assume responsibility for the accuracy of medical information included.\n\nGame can be a support for learning but requires the presence and/or explanations of an expert teacher who can benefit from offering simulations in classroom.\n\nStudents who approach this game to gain knowledge must responsibly compare the medical information presented in-game with information from accredited or recognized sources.\n\n©2023 Davide Nasato"
        )

        disclaimer_text = tk.Text(disclaimer_window, wrap="word", font=("DejaVu Sans Mono", 13), background="#c299c2")
        disclaimer_text.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(disclaimer_window, command=disclaimer_text.yview)
        scrollbar.pack(side="right", fill="y")
        disclaimer_text.config(yscrollcommand=scrollbar.set)
        disclaimer_text.insert("1.0", disclaimer)
        ok_button = tk.Button(
            disclaimer_window,
            text="Close",
            command=lambda: disclaimer_window.destroy(),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        ok_button.pack()
        self.center_window(disclaimer_window)

    def show_help_window(self):
        help_window = tk.Toplevel(self.root, background="#c299c2")
        help_window.title("Help - Game Rules")
        self.is_running = False

        rules = (
            "'Bacteria versus Antibiotics'\n\n"
            "Game Rules:\n\n"
            "1. Colored cells represent bacteria. Green, or purple if resistant to antibiotics:\n\n"
            "   - They duplicate during the game and are killed by antibiotics\n\n"
            "2. White cells are antibiotics; administer them by pressing 'Antibiotic':\n\n"
            "   - You can treat infection only when it starts causing symptoms\n"
            "   - Antibiotics are consumed and must be administered regularly\n"
            "   - Patient dies if they take too many antibiotics\n"
            "   - If antibiotics run out, bacteria become resistant\n\n"
            "3. You can induce resistance by pressing 'Resistance'.\n\n"
            "   - Bacteria require higher doses of antibiotics!\n"
            "   - They try to avoid being reached by antibiotics.\n"
            "   - If a resistant bacterium dies, it deactivates an antibiotic molecule.\n"
            "   - Deactivated antibiotics turn yellow and get destroyed.\n"
            "   - If you administer antibiotics for too many consecutive days,\n"
            "      you will develop resistance!\n"
            "   - You have a 5% chance of admitting a patient with resistance\n     but also the chance to receive random bonuses.\n\n"

            "4. Even if the patient is not infected with a resistant bacterium,\nthere are three difficulty levels:\n\n"
            "   - Easy: patient has an exceptional immune system!\n"
            "   - Routine: immune system works, but don't underestimate anything!\n"
            "   - Difficult: Patient is immunocompromised; infection will be tough!\n\n"

            "5. Pay attention to time; these circumstances can make you lose points:\n"
            "   - If the treatment lasts too long, patient might become depressed\n"
            "   - Patient might worsen and die with overly long treatment!\n"
            "   - Fatigue could lead to errors in therapy\n\n"
            "You will need to decide when to start treatment and how often to continue it.\n\nCaution:\nresistance requires more antibiotics, but you might kill the patient!\n\nBacteria will pass resistance through their plasmids.\nIf resistance develops, you'll need enough points to\nsustain the final challenge, which will be ONLY against resistant bacteria!\n\nA tip: your medical supervisor is breathing down your neck, waiting for your next mistake to fire you!\n\n"

            "Scoring:\n\n"
            "Points are earned for:\n"
            "   Duration of the patient's symptom-free life\n"
            "   Killing resistant and non-resistant bacteria\n"
            "   Healing from the illness\n\n"
            "Points are subtracted for:\n"
            "   Endangering the patient\n"
            "       - If you induce resistance\n"
            "       - If there's a risk of sepsis\n"
            "       - If you overdo antibiotics\n"
            "       - Taking too long to treat the person\n"
            "       - Administering the wrong therapy:\n"
            "         it happens if treatment is too long (red cells).\n"

            "   Patient's death\n"
            "   Administration of antibiotics\n"

            "   With each duplication of a resistant or non-resistant bacterium\n"
            "   If you get fired by medical supervisor\n\n"

            "   Keyboard Shortcuts:\n\n"
            "   ENTER   - Administer a dose of antibiotics\n"
            "   SPACE  - Induce resistance\n"
            "   ESC     - Restart game\n\n"
            "Good luck in your fight against infection!\n"
            "©2023 Davide Nasato."
        )

       
        help_text = tk.Text(help_window, wrap="word", font=("DejaVu Sans Mono", 13), background="#c299c2")
        help_text.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(help_window, command=help_text.yview)
        scrollbar.pack(side="right", fill="y")
        help_text.config(yscrollcommand=scrollbar.set)
        help_text.insert("1.0", rules)
        disclaimer_button = tk.Button(
            help_window,
            text="See Disclaimer",
            command=self.show_disclaimer_window,
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        disclaimer_button.pack(side="left")
        ok_button = tk.Button(
            help_window,
            text="OK",
            command=lambda: self.close_help_window(help_window),
            font=("DejaVu Sans Mono", 13, "bold"), background="#d3c8e6"
        )
        ok_button.pack(side="right")
        self.center_window(help_window)

    def close_help_window(self, window):
        window.destroy()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry("{}x{}+{}+{}".format(width, height, x, y))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x680")

    app = GridApp(root)
    import ctypes
    import sys
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    root.mainloop()
