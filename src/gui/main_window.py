import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
import json
from pathlib import Path


class SoundboardApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Soundboard")

        # Load configuration
        self.config = self.load_config()
        self.setup_theme()

        width = self.config['window']['width']
        height = self.config['window']['height']

        self.root.geometry(
            f"{width}x{height}")
        self.root.resizable(self.config['window']['resizable'],
                            self.config['window']['resizable'])

        # Initialize pygame mixer
        pygame.mixer.init()

        # Data
        self.soundboards = {}
        self.current_board = None
        self.sound_buttons = []

        # Load existing soundboards
        self.load_soundboards()

        # Create UI
        self.create_widgets()

        # Set initial state - disable buttons if no soundboard selected
        self.update_button_states()

    def load_config(self):
        """Load configuration from config.json"""
        config_file = Path("data/config.json")
        default_config = {
            "theme": "dark",
            "window": {
                "width": 500,
                "height": 350,
                "resizable": False
            },
            "audio": {
                "supported_formats": ["*.mp3", "*.wav", "*.ogg"],
                "default_volume": 0.7
            },
            "ui": {
                "button_grid": {
                    "rows": 2,
                    "columns": 3
                },
                "button_size": 70,
                "max_label_length": 10
            }
        }

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config: {e}. Using defaults.")
                return default_config
        else:
            # Create default config file
            config_file.parent.mkdir(exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def setup_theme(self):
        """Setup theme colors based on config"""
        if self.config['theme'] == 'dark':
            self.colors = {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'button_bg': '#404040',
                'button_fg': '#ffffff',
                'button_inactive': '#505050',
                'button_active': '#4caf50',
                'button_hover': '#555555',
                'frame_bg': '#333333',
                'dropdown_bg': '#404040'
            }
        else:  # light theme
            self.colors = {
                'bg': '#ffffff',
                'fg': '#000000',
                'button_bg': '#f0f0f0',
                'button_fg': '#000000',
                'button_inactive': '#e0e0e0',
                'button_active': '#4caf50',
                'button_hover': '#e8e8e8',
                'frame_bg': '#f5f5f5',
                'dropdown_bg': '#ffffff'
            }

        # Apply theme to root window
        self.root.configure(bg=self.colors['bg'])

    def create_widgets(self):
        # Top menu frame
        menu_frame = tk.Frame(self.root, height=40, bg=self.colors['frame_bg'])
        menu_frame.pack(fill='x', padx=10, pady=5)
        menu_frame.pack_propagate(False)

        # Soundboard dropdown
        self.board_var = tk.StringVar()
        self.dropdown = ttk.Combobox(
            menu_frame,
            textvariable=self.board_var,
            values=list(self.soundboards.keys()),
            state='readonly',
            width=20
        )
        self.dropdown.pack(side='left')
        self.dropdown.bind('<<ComboboxSelected>>', self.load_selected_board)

        # Buttons frame
        button_frame = tk.Frame(menu_frame, bg=self.colors['frame_bg'])
        button_frame.pack(side='left', padx=5)

        # New board button
        self.new_button = tk.Button(
            button_frame,
            text="New",
            command=self.new_board,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_hover']
        )
        self.new_button.pack(side='left', padx=2)

        # Theme toggle button
        self.theme_button = tk.Button(
            button_frame,
            text="🌙" if self.config['theme'] == 'light' else "☀️",
            command=self.toggle_theme,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground=self.colors['button_hover'],
            font=('Arial', 12)
        )
        self.theme_button.pack(side='left', padx=2)

        # Sound buttons grid
        self.board_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.board_frame.pack(expand=True, fill='both', padx=20, pady=10)

        self.create_sound_buttons()

    def create_sound_buttons(self):
        self.sound_buttons = []

        rows = self.config['ui']['button_grid']['rows']
        cols = self.config['ui']['button_grid']['columns']
        button_size = self.config['ui']['button_size']

        for i in range(rows):
            self.board_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.board_frame.grid_columnconfigure(j, weight=1)

        for i in range(rows * cols):
            row = i // cols
            col = i % cols

            container = tk.Frame(self.board_frame, bg=self.colors['bg'])
            container.grid(row=row, column=col, padx=15, pady=15)

            # Circular button
            canvas = tk.Canvas(
                container,
                width=button_size,
                height=button_size,
                highlightthickness=0,
                bg=self.colors['bg']
            )
            canvas.pack()

            circle = canvas.create_oval(
                5, 5, button_size-5, button_size-5,
                fill=self.colors['button_inactive'],
                outline=self.colors['button_fg'],
                width=2
            )

            # Label
            label = tk.Label(
                container,
                text="SoundName",
                font=('Arial', 9),
                bg=self.colors['bg'],
                fg=self.colors['fg']
            )
            label.pack(pady=2)

            button_data = {
                'canvas': canvas,
                'circle': circle,
                'label': label,
                'sound_file': None,
                'position': i,
                'container': container
            }
            self.sound_buttons.append(button_data)

            # Click events
            canvas.bind('<Button-1>', lambda e, pos=i: self.button_click(pos))
            canvas.bind('<Button-3>', lambda e, pos=i: self.right_click(pos))

    def update_button_states(self):
        """Enable/disable buttons based on whether a soundboard is selected"""
        has_board = self.current_board is not None

        for button in self.sound_buttons:
            if has_board:
                button['canvas'].configure(state='normal')
                button['label'].configure(fg=self.colors['fg'])
            else:
                button['canvas'].configure(state='disabled')
                button['label'].configure(fg=self.colors['button_inactive'])

    def button_click(self, pos):
        if not self.current_board:
            messagebox.showwarning("No Soundboard",
                                   "Please create/select a soundboard first!")
            return

        button = self.sound_buttons[pos]
        if button['sound_file']:
            # Play sound
            try:
                pygame.mixer.music.load(button['sound_file'])
                pygame.mixer.music.set_volume(
                    self.config['audio']['default_volume'])
                pygame.mixer.music.play()
            except pygame.error as e:
                messagebox.showerror("Pygame Error", f"Could not play: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error: {e}")
        else:
            # Add sound
            self.add_sound(pos)

    def right_click(self, pos):
        if not self.current_board:
            messagebox.showwarning("No Soundboard",
                                   "Please create/select a soundboard first!")
            return

        button = self.sound_buttons[pos]
        if button['sound_file']:
            # Remove sound
            button['sound_file'] = None
            button['canvas'].itemconfig(button['circle'],
                                        fill=self.colors['button_inactive'])
            button['label'].config(text="SoundName")
            self.save_boards()
        else:
            # Add sound
            self.add_sound(pos)

    def add_sound(self, pos):
        if not self.current_board:
            messagebox.showwarning("No Soundboard",
                                   "Please create/select a soundboard first")
            return

        file_path = filedialog.askopenfilename(
            title="Select Sound",
            filetypes=[("Audio Files", " ".join(
                self.config['audio']['supported_formats']))]
        )

        if file_path:
            button = self.sound_buttons[pos]
            button['sound_file'] = file_path
            button['canvas'].itemconfig(button['circle'],
                                        fill=self.colors['button_active'])

            # Get filename without extension
            name = Path(file_path).stem
            max_length = self.config['ui']['max_label_length']
            if len(name) > max_length:
                name = name[:max_length] + "..."
            button['label'].config(text=name)

            # Auto-save when sound is added
            self.save_boards()

    def new_board(self):
        name = tk.simpledialog.askstring("New Board", "Board name:")
        if name and name.strip():
            name = name.strip()
            if name in self.soundboards:
                messagebox.showwarning("Board Exists",
                                       f"Soundboard '{name}' already exists!")
                return

            self.soundboards[name] = []
            self.dropdown['values'] = list(self.soundboards.keys())
            self.board_var.set(name)
            self.current_board = name
            self.clear_all_buttons()
            self.update_button_states()
            self.save_boards()
            messagebox.showinfo("Success",
                                f"Soundboard '{name}' created successfully!")

    def clear_all_buttons(self):
        for button in self.sound_buttons:
            button['sound_file'] = None
            button['canvas'].itemconfig(button['circle'],
                                        fill=self.colors['button_inactive'])
            button['label'].config(text="SoundName")

    def load_selected_board(self, event):
        board_name = self.board_var.get()
        self.current_board = board_name
        self.clear_all_buttons()
        self.update_button_states()

        if board_name in self.soundboards:
            for sound_data in self.soundboards[board_name]:
                pos = sound_data['pos']
                if 0 <= pos < len(self.sound_buttons):
                    button = self.sound_buttons[pos]
                    button['sound_file'] = sound_data['file']
                    button['canvas'].itemconfig(button['circle'],
                                                fill=self.colors[
                                                    'button_active'])
                    button['label'].config(text=sound_data['name'])

    def _apply_widget_theme(self, widget):
        """Apply theme recursively to all widgets"""
        widget_type = widget.winfo_class()

        try:
            if widget_type == 'Frame':
                widget.configure(bg=self.colors['frame_bg'])
            elif widget_type in ('Label', 'Button'):
                widget.configure(
                    bg=self.colors['bg'],
                    fg=self.colors['fg']
                )
            elif widget_type == 'Entry':
                widget.configure(
                    bg=self.colors['bg'],
                    fg=self.colors['fg'],
                    insertbackground=self.colors['fg']
                )
            elif widget_type == 'TButton':  # For ttk.Button if you use ttk
                style = ttk.Style()
                style.configure('TButton', background=self.colors['button_bg'],
                                foreground=self.colors['button_fg'])

            # Add more widget types as needed
        except (tk.TclError, AttributeError) as e:
            print(f"Warning: Couldn't apply theme to {widget}: {e}")

        # Recurse through children
        for child in widget.winfo_children():
            self._apply_widget_theme(child)

    def apply_theme(self):
        """Apply the theme colors to the entire UI"""
        self.setup_theme()  # Load theme colors from config

        # Apply to root window
        self.root.configure(bg=self.colors['bg'])

        # Apply to child widgets
        for widget in self.root.winfo_children():
            self._apply_widget_theme(widget)

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.config['theme'] == 'dark':
            self.config['theme'] = 'light'
        else:
            self.config['theme'] = 'dark'
        self.save_config()
        self.apply_theme()

        # Show restart message
        messagebox.showinfo("Theme Changed",
                            "Theme has been applied")

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open("data/config.json", 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def load_soundboards(self):
        data_file = Path("data/soundboards.json")
        if data_file.exists():
            try:
                with open(data_file, 'r') as f:
                    self.soundboards = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to decode JSON: {e}")
            except (IOError, OSError) as e:
                print(f"Warning: File access error: {e}")

    def save_boards(self):
        if self.current_board:
            sounds = []
            for i, button in enumerate(self.sound_buttons):
                if button['sound_file']:
                    sounds.append({
                        'pos': i,
                        'file': button['sound_file'],
                        'name': button['label'].cget('text')
                    })
            self.soundboards[self.current_board] = sounds

        # Ensure data directory exists
        Path("data").mkdir(exist_ok=True)

        try:
            with open("data/soundboards.json", 'w') as f:
                json.dump(self.soundboards, f, indent=2)
        except IOError as e:
            messagebox.showerror("Error", f"Failed to save soundboards: {e}")

    def run(self):
        # Auto-save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.save_boards()
        self.root.destroy()


if __name__ == "__main__":
    import tkinter.simpledialog
    app = SoundboardApp()
    app.run()
