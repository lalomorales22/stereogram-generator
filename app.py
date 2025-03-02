#!/usr/bin/env python3
"""
Stereogram Sorcery: The AI Depth Illusion

Unleash the magic of 3D illusions and hidden messages with this enchanting Python app.
Craft your own stereogram spells using mystical depth maps, enchanted patterns, and secret incantations.
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import numpy as np
import requests
import base64
from io import BytesIO
import logging

# Set up cosmic logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger("StereogramSorcery")

class StereogramSorcery:
    def __init__(self, root):
        try:
            logger.info("Summoning the Stereogram Sorcery app...")
            self.root = root
            self.root.title("Stereogram Sorcery: The AI Depth Illusion")
            self.root.geometry("1200x700")
            self.root.minsize(900, 600)
            self.root.configure(bg="#121212")  # Dark magic background

            # Mystic API settings (replace with your API key as needed)
            self.default_api_key = "ENTER-KEY-HEYE"
            self.api_host = "https://api.stability.ai"
            self.api_engine = "stable-diffusion-v1-6"
            
            # Image and array holders for magical ingredients
            self.depth_img = None
            self.pattern_img = None
            self.depth_array = None
            self.pattern_array = None
            self.result_img = None
            self.is_generating = False
            
            # Set up enchanted styles and layout
            self.setup_styles()
            self.create_layout()
            logger.info("The spell is ready! App initialized successfully.")
        except Exception as e:
            logger.error(f"Error during summoning: {e}")
            messagebox.showerror("Initialization Error", f"Failed to initialize the magic: {e}")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        # Define our mystical color palette
        self.bg_color = "#121212"      
        self.accent_color = "#2E2E2E"  
        self.text_color = "#E0E0E0"    
        self.primary_color = "#1976D2" 
        self.hover_color = "#3E3E3E"   
        
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 10))
        self.style.configure("TButton", 
                             background=self.accent_color,
                             foreground=self.text_color,
                             borderwidth=2,
                             relief="flat",
                             font=("Segoe UI", 10))
        self.style.map("TButton", 
                       background=[("active", self.hover_color)],
                       foreground=[("active", self.primary_color)])
        self.style.configure("Primary.TButton", 
                             background=self.accent_color,
                             foreground=self.text_color,
                             borderwidth=2,
                             relief="flat",
                             font=("Segoe UI", 10))
        self.style.map("Primary.TButton", 
                       background=[("active", self.primary_color)],
                       foreground=[("active", "#FFFFFF")])
        self.style.configure("Vertical.TScrollbar",
                             troughcolor=self.bg_color,
                             background=self.accent_color,
                             arrowcolor=self.primary_color,
                             borderwidth=0)

    def create_layout(self):
        try:
            self.main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
            self.main_pane.pack(fill=tk.BOTH, expand=True)
            
            # Left panel: Wizard Controls (300px wide)
            self.controls_frame = ttk.Frame(self.main_pane, width=300)
            self.main_pane.add(self.controls_frame, weight=0)
            
            # Right panel: Magical Preview
            self.preview_frame = ttk.Frame(self.main_pane)
            self.main_pane.add(self.preview_frame, weight=3)
            
            self.setup_controls()
            self.setup_preview()
            
            # Hidden notification label (appears like a magical scroll)
            self.notification = ttk.Label(self.root, text="", background=self.primary_color, foreground="white", padding=10)
            self.notification.place(relx=1, y=20, anchor="ne", width=300)
            self.notification.place_forget()
        except Exception as e:
            logger.error(f"Error creating layout: {e}")
            raise

    def setup_controls(self):
        try:
            self.control_canvas = tk.Canvas(self.controls_frame, bg=self.bg_color, highlightthickness=0, bd=0)
            self.control_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.control_scrollbar = ttk.Scrollbar(self.controls_frame, orient=tk.VERTICAL, command=self.control_canvas.yview, style="Vertical.TScrollbar")
            self.control_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.control_canvas.configure(yscrollcommand=self.control_scrollbar.set)
            self.controls_content = ttk.Frame(self.control_canvas)
            self.control_canvas_window = self.control_canvas.create_window((0, 0), window=self.controls_content, anchor=tk.NW, width=280)
            
            title_label = ttk.Label(self.controls_content, text="Stereogram Sorcery", style="TLabel", font=("Segoe UI", 16, "bold"))
            title_label.pack(pady=(15, 20), fill=tk.X, padx=10)
            
            # Notebook: Manual and AI wizardry tabs
            self.input_notebook = ttk.Notebook(self.controls_content)
            self.input_notebook.pack(fill=tk.X, padx=10, pady=5)
            self.manual_tab = ttk.Frame(self.input_notebook)
            self.ai_tab = ttk.Frame(self.input_notebook)
            self.input_notebook.add(self.manual_tab, text="Manual Magic")
            self.input_notebook.add(self.ai_tab, text="AI Enchantment")
            
            self.setup_manual_tab()
            self.setup_ai_tab()
            
            # Stereogram Spell Settings
            self.add_section_header("Stereogram Spell Settings")
            self.shift_strength_var = tk.IntVar(value=15)
            self.shift_strength_label = ttk.Label(self.controls_content, text=f"Shift Strength: {self.shift_strength_var.get()}", style="TLabel")
            self.shift_strength_label.pack(fill=tk.X, padx=10, pady=(10, 0))
            shift_scale = ttk.Scale(self.controls_content, from_=5, to=50, orient=tk.HORIZONTAL,
                                    variable=self.shift_strength_var, command=self.update_shift_label)
            shift_scale.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            self.pattern_scale_var = tk.DoubleVar(value=1.0)
            self.pattern_scale_label = ttk.Label(self.controls_content, text=f"Pattern Scale: {self.pattern_scale_var.get():.1f}", style="TLabel")
            self.pattern_scale_label.pack(fill=tk.X, padx=10, pady=(10, 0))
            pattern_scale = ttk.Scale(self.controls_content, from_=0.5, to=2.0, orient=tk.HORIZONTAL,
                                      variable=self.pattern_scale_var, command=self.update_pattern_scale_label)
            pattern_scale.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # Updated Depth Contrast Slider with gentler range
            self.depth_contrast_var = tk.DoubleVar(value=.03)
            self.depth_contrast_label = ttk.Label(self.controls_content, text=f"Depth Contrast: {self.depth_contrast_var.get():.2f}", style="TLabel")
            self.depth_contrast_label.pack(fill=tk.X, padx=10, pady=(10, 0))
            depth_scale = ttk.Scale(self.controls_content, from_=.01, to=.05, orient=tk.HORIZONTAL,
                                    variable=self.depth_contrast_var, command=self.update_depth_contrast_label)
            depth_scale.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # Hidden Spell (Secret Message)
            self.add_section_header("Secret Spell")
            ttk.Label(self.controls_content, text="Spell to Hide", style="TLabel").pack(fill=tk.X, padx=10, pady=(10, 0))
            self.hidden_message = scrolledtext.ScrolledText(self.controls_content, height=3, bg="#1E1E1E", fg=self.text_color)
            self.hidden_message.pack(fill=tk.X, padx=10, pady=(5, 5))
            self.enable_stego_var = tk.BooleanVar(value=True)
            enable_stego = ttk.Checkbutton(self.controls_content, text="Enable Spell Embedding", variable=self.enable_stego_var, style="TCheckbutton")
            enable_stego.pack(padx=10, pady=(0, 10), anchor=tk.W)
            
            # Output Settings
            self.add_section_header("Final Spell Output")
            ttk.Label(self.controls_content, text="Output Format", style="TLabel").pack(fill=tk.X, padx=10, pady=(10, 0))
            self.format_var = tk.StringVar(value="png")
            format_frame = ttk.Frame(self.controls_content)
            format_frame.pack(fill=tk.X, padx=10, pady=(5, 5))
            ttk.Radiobutton(format_frame, text="PNG", variable=self.format_var, value="png", style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
            ttk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, value="jpeg", style="TRadiobutton").pack(side=tk.LEFT)
            # Bind change of format to toggle JPEG quality settings
            self.format_var.trace_add("write", lambda *args: self.toggle_jpeg_quality())
            
            self.jpeg_quality_frame = ttk.Frame(self.controls_content)
            self.jpeg_quality_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            self.jpeg_quality_var = tk.DoubleVar(value=0.85)
            self.jpeg_quality_label = ttk.Label(self.jpeg_quality_frame, text=f"JPEG Quality: {int(self.jpeg_quality_var.get()*100)}%", style="TLabel")
            self.jpeg_quality_label.pack(fill=tk.X)
            jpeg_scale = ttk.Scale(self.jpeg_quality_frame, from_=0.3, to=1.0, orient=tk.HORIZONTAL,
                                   variable=self.jpeg_quality_var, command=self.update_jpeg_quality_label)
            jpeg_scale.pack(fill=tk.X)
            if self.format_var.get() != "jpeg":
                self.jpeg_quality_frame.pack_forget()
            
            # Mystic API Portal
            self.add_section_header("Mystic API Portal")
            ttk.Label(self.controls_content, text="Stability AI API Key", style="TLabel").pack(fill=tk.X, padx=10, pady=(10, 0))
            self.api_key = ttk.Entry(self.controls_content)
            self.api_key.pack(fill=tk.X, padx=10, pady=(5, 5))
            self.api_key.insert(0, self.default_api_key)
            ttk.Label(self.controls_content, text="Default: " + self.default_api_key[:10] + "...", foreground="#777777", font=("Segoe UI", 8)).pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # Action Buttons: Cast your spells!
            self.generate_btn = ttk.Button(self.controls_content, text="CAST STEREOGRAM SPELL", style="Primary.TButton",
                                           command=self.generate_stereogram)
            self.generate_btn.pack(fill=tk.X, padx=10, pady=(15, 5))
            self.download_btn = ttk.Button(self.controls_content, text="SAVE ENCHANTMENT",
                                           command=self.download_stereogram)
            self.download_btn.pack(fill=tk.X, padx=10, pady=5)
            self.decode_btn = ttk.Button(self.controls_content, text="REVEAL SECRET SPELL",
                                         command=self.show_decode_dialog)
            self.decode_btn.pack(fill=tk.X, padx=10, pady=5)
            self.help_btn = ttk.Button(self.controls_content, text="ABOUT THIS SORCERY",
                                       command=self.show_help)
            self.help_btn.pack(fill=tk.X, padx=10, pady=(5, 20))
            
            self.controls_content.bind("<Configure>", self.update_scrollregion)
        except Exception as e:
            logger.error(f"Error setting up controls: {e}")
            raise

    def setup_manual_tab(self):
        try:
            ttk.Label(self.manual_tab, text="Mystic Depth Map", style="TLabel").pack(fill=tk.X, pady=(10, 5))
            depth_frame = ttk.Frame(self.manual_tab)
            depth_frame.pack(fill=tk.X, pady=(0, 10))
            self.depth_btn = ttk.Button(depth_frame, text="Browse...", command=self.load_depth_map)
            self.depth_btn.pack(side=tk.LEFT, padx=(0, 5))
            self.depth_label = ttk.Label(depth_frame, text="No file selected", style="TLabel")
            self.depth_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.depth_preview_frame = ttk.Frame(self.manual_tab, height=100)
            self.depth_preview_frame.pack(fill=tk.X, pady=(0, 10))
            self.depth_preview_frame.pack_propagate(False)
            self.depth_preview_label = ttk.Label(self.depth_preview_frame, text="No depth map selected", background="#1E1E1E", padding=10, style="TLabel")
            self.depth_preview_label.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(self.manual_tab, text="Enchanted Pattern", style="TLabel").pack(fill=tk.X, pady=(10, 5))
            pattern_frame = ttk.Frame(self.manual_tab)
            pattern_frame.pack(fill=tk.X, pady=(0, 10))
            self.pattern_btn = ttk.Button(pattern_frame, text="Browse...", command=self.load_pattern)
            self.pattern_btn.pack(side=tk.LEFT, padx=(0, 5))
            self.pattern_label = ttk.Label(pattern_frame, text="No file selected", style="TLabel")
            self.pattern_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.pattern_preview_frame = ttk.Frame(self.manual_tab, height=100)
            self.pattern_preview_frame.pack(fill=tk.X, pady=(0, 10))
            self.pattern_preview_frame.pack_propagate(False)
            self.pattern_preview_label = ttk.Label(self.pattern_preview_frame, text="No pattern selected", background="#1E1E1E", padding=10, style="TLabel")
            self.pattern_preview_label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            logger.error(f"Error setting up manual tab: {e}")
            raise

    def setup_ai_tab(self):
        try:
            ttk.Label(self.ai_tab, text="AI Incantation", style="TLabel").pack(fill=tk.X, pady=(10, 5))
            self.ai_prompt = scrolledtext.ScrolledText(self.ai_tab, height=4, bg="#1E1E1E", fg=self.text_color)
            self.ai_prompt.pack(fill=tk.X, pady=(0, 10))
            self.ai_prompt.insert(tk.END, "An underwater realm with luminescent creatures")
            ttk.Label(self.ai_tab, text="Generate As:", style="TLabel").pack(fill=tk.X, pady=(10, 5))
            self.gen_type_var = tk.StringVar(value="depthMap")
            gen_frame = ttk.Frame(self.ai_tab)
            gen_frame.pack(fill=tk.X, pady=(0, 10))
            ttk.Radiobutton(gen_frame, text="Depth Map", variable=self.gen_type_var, value="depthMap", style="TRadiobutton").pack(side=tk.LEFT, padx=(0, 10))
            ttk.Radiobutton(gen_frame, text="Pattern", variable=self.gen_type_var, value="pattern", style="TRadiobutton").pack(side=tk.LEFT)
            self.ai_gen_btn = ttk.Button(self.ai_tab, text="ENCHANT WITH AI", style="Primary.TButton",
                                         command=self.generate_with_ai)
            self.ai_gen_btn.pack(fill=tk.X, pady=(10, 5))
        except Exception as e:
            logger.error(f"Error setting up AI tab: {e}")
            raise

    def setup_preview(self):
        try:
            self.preview_notebook = ttk.Notebook(self.preview_frame)
            self.preview_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.result_tab = ttk.Frame(self.preview_notebook)
            self.depth_tab = ttk.Frame(self.preview_notebook)
            self.pattern_tab = ttk.Frame(self.preview_notebook)
            self.preview_notebook.add(self.result_tab, text="Final Enchantment")
            self.preview_notebook.add(self.depth_tab, text="Mystic Depth Map")
            self.preview_notebook.add(self.pattern_tab, text="Enchanted Pattern")
            self.result_canvas = tk.Canvas(self.result_tab, bg=self.bg_color, highlightthickness=1, highlightbackground="#3E3E3E")
            self.result_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.depth_canvas = tk.Canvas(self.depth_tab, bg=self.bg_color, highlightthickness=1, highlightbackground="#3E3E3E")
            self.depth_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.pattern_canvas = tk.Canvas(self.pattern_tab, bg=self.bg_color, highlightthickness=1, highlightbackground="#3E3E3E")
            self.pattern_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            self.result_canvas.create_text(200, 200, text="No enchantment cast yet", fill=self.text_color, font=("Segoe UI", 12), tags="placeholder_text")
            self.depth_canvas.create_text(200, 200, text="No depth map revealed", fill=self.text_color, font=("Segoe UI", 12), tags="placeholder_text")
            self.pattern_canvas.create_text(200, 200, text="No pattern discovered", fill=self.text_color, font=("Segoe UI", 12), tags="placeholder_text")
            self.loading_frame = ttk.Frame(self.preview_frame)
            self.loading_label = ttk.Label(self.loading_frame, text="Conjuring...", style="TLabel")
            self.loading_label.pack(pady=20)
            self.progress = ttk.Progressbar(self.loading_frame, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
            self.progress.pack(pady=10)
            self.loading_frame.place_forget()
        except Exception as e:
            logger.error(f"Error setting up preview: {e}")
            raise

    def add_section_header(self, text):
        ttk.Separator(self.controls_content, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=(15, 10))
        header = ttk.Label(self.controls_content, text=text, style="TLabel", font=("Segoe UI", 12, "bold"))
        header.pack(fill=tk.X, padx=10)

    def update_scrollregion(self, event):
        try:
            self.control_canvas.configure(scrollregion=self.control_canvas.bbox("all"))
        except Exception as e:
            logger.error(f"Error updating scroll region: {e}")

    def update_shift_label(self, value):
        try:
            value = int(float(value))
            self.shift_strength_label.config(text=f"Shift Strength: {value}")
        except Exception as e:
            logger.error(f"Error updating shift label: {e}")

    def update_pattern_scale_label(self, value):
        try:
            value = float(value)
            self.pattern_scale_label.config(text=f"Pattern Scale: {value:.1f}")
        except Exception as e:
            logger.error(f"Error updating pattern scale label: {e}")

    def update_depth_contrast_label(self, value):
        try:
            value = float(value)
            self.depth_contrast_label.config(text=f"Depth Contrast: {value:.2f}")
        except Exception as e:
            logger.error(f"Error updating depth contrast label: {e}")

    def update_jpeg_quality_label(self, value):
        try:
            value = float(value)
            self.jpeg_quality_label.config(text=f"JPEG Quality: {int(value*100)}%")
        except Exception as e:
            logger.error(f"Error updating JPEG quality label: {e}")

    def toggle_jpeg_quality(self):
        try:
            if self.format_var.get() == "jpeg":
                self.jpeg_quality_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            else:
                self.jpeg_quality_frame.pack_forget()
        except Exception as e:
            logger.error(f"Error toggling JPEG quality: {e}")

    def load_depth_map(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select Mystic Depth Map",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path:
                return
            self.depth_img = Image.open(file_path)
            self.depth_array = np.array(self.depth_img.convert("L"))
            self.depth_label.config(text=os.path.basename(file_path))
            self.update_depth_preview()
            if self.pattern_img:
                self.show_notification("Both magical ingredients ready for the spell!")
            self.preview_notebook.select(1)
            self.show_notification("Mystic depth map loaded!")
        except Exception as e:
            logger.error(f"Error loading depth map: {e}")
            messagebox.showerror("Error", f"Failed to load depth map: {e}")

    def load_pattern(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select Enchanted Pattern",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
            )
            if not file_path:
                return
            self.pattern_img = Image.open(file_path)
            self.pattern_array = np.array(self.pattern_img.convert("RGB"))
            self.pattern_label.config(text=os.path.basename(file_path))
            self.update_pattern_preview()
            if self.depth_img:
                self.show_notification("Both magical ingredients ready for the spell!")
            self.preview_notebook.select(2)
            self.show_notification("Enchanted pattern loaded!")
        except Exception as e:
            logger.error(f"Error loading pattern image: {e}")
            messagebox.showerror("Error", f"Failed to load pattern image: {e}")

    def update_depth_preview(self):
        try:
            if not self.depth_img:
                return
            thumbnail = self.resize_image_to_fit(self.depth_img, self.depth_preview_frame.winfo_width(), 100)
            photo = ImageTk.PhotoImage(thumbnail)
            self.depth_preview_label.config(image=photo, text="")
            self.depth_preview_label.image = photo
            self.update_canvas_image(self.depth_canvas, self.depth_img)
        except Exception as e:
            logger.error(f"Error updating depth preview: {e}")

    def update_pattern_preview(self):
        try:
            if not self.pattern_img:
                return
            thumbnail = self.resize_image_to_fit(self.pattern_img, self.pattern_preview_frame.winfo_width(), 100)
            photo = ImageTk.PhotoImage(thumbnail)
            self.pattern_preview_label.config(image=photo, text="")
            self.pattern_preview_label.image = photo
            self.update_canvas_image(self.pattern_canvas, self.pattern_img)
        except Exception as e:
            logger.error(f"Error updating pattern preview: {e}")

    def update_canvas_image(self, canvas, img):
        try:
            canvas.delete("all")
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            if canvas_width <= 1 or canvas_height <= 1:
                canvas.create_text(200, 200, text="Loading...", fill=self.text_color)
                self.root.after(100, lambda: self.update_canvas_image(canvas, img))
                return
            resized = self.resize_image_to_fit(img, canvas_width, canvas_height)
            photo = ImageTk.PhotoImage(resized)
            setattr(canvas, 'image', photo)
            img_width, img_height = resized.size
            x = (canvas_width - img_width) // 2
            y = (canvas_height - img_height) // 2
            canvas.create_image(x, y, anchor=tk.NW, image=photo)
        except Exception as e:
            logger.error(f"Error updating canvas image: {e}")
            center_x = max(canvas.winfo_width(), 200) // 2
            center_y = max(canvas.winfo_height(), 200) // 2
            canvas.create_text(center_x, center_y, text="Error displaying image", fill="#D32F2F")

    def resize_image_to_fit(self, img, width, height):
        if not img:
            return None
        try:
            if width <= 0 or height <= 0:
                return img
            img_width, img_height = img.size
            scale = min(width / max(img_width, 1), height / max(img_height, 1))
            if scale < 1:
                new_width = max(int(img_width * scale), 1)
                new_height = max(int(img_height * scale), 1)
                return img.resize((new_width, new_height), Image.LANCZOS)
            return img
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return img

    def show_notification(self, message, is_error=False):
        try:
            self.notification.configure(background=self.primary_color if not is_error else "#D32F2F", text=message)
            self.notification.place(relx=1, y=20, anchor="ne")
            self.root.after(3000, self.notification.place_forget)
        except Exception as e:
            logger.error(f"Error showing notification: {e}")

    def generate_stereogram(self):
        try:
            if not self.depth_img or not self.pattern_img:
                self.show_notification("Both depth map and pattern are required", True)
                return
            if self.is_generating:
                return
            self.is_generating = True
            self.loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.loading_label.configure(text="Casting stereogram spell...")
            self.progress.start(10)
            thread = threading.Thread(target=self._generate_stereogram_thread)
            thread.daemon = True
            thread.start()
        except Exception as e:
            logger.error(f"Error initiating stereogram generation: {e}")
            self.is_generating = False

    def _generate_stereogram_thread(self):
        try:
            shift_strength = self.shift_strength_var.get()
            pattern_scale = self.pattern_scale_var.get()
            contrast = self.depth_contrast_var.get()
            # Apply our gentler contrast adjustment
            depth_enhanced = self.adjust_contrast(self.depth_array, contrast)
            pattern_width = int(self.pattern_img.width * pattern_scale)
            pattern_height = int(self.pattern_img.height * pattern_scale)
            pattern_scaled = self.pattern_img.resize((pattern_width, pattern_height), Image.LANCZOS)
            pattern_tiled = Image.new("RGB", self.depth_img.size)
            for y in range(0, self.depth_img.height, pattern_height):
                for x in range(0, self.depth_img.width, pattern_width):
                    pattern_tiled.paste(pattern_scaled, (x, y))
            pattern_array = np.array(pattern_tiled)
            width, height = self.depth_img.size
            result_array = np.zeros((height, width, 3), dtype=np.uint8)
            for y in range(height):
                row = np.zeros((width, 3), dtype=np.uint8)
                row[:shift_strength] = pattern_array[y, :shift_strength]
                for x in range(shift_strength, width):
                    depth_val = depth_enhanced[y, x] / 255.0
                    shift = int(depth_val * shift_strength)
                    if x - shift < shift_strength:
                        row[x] = pattern_array[y, x]
                    else:
                        row[x] = row[x - shift]
                result_array[y] = row
            self.result_img = Image.fromarray(result_array.astype(np.uint8))
            if self.enable_stego_var.get():
                message = self.hidden_message.get("1.0", tk.END).strip()
                if message:
                    self.result_img = self.embed_message(self.result_img, message)
            self.root.after(0, self.update_result_preview)
        except Exception as e:
            self.root.after(0, lambda: self.show_notification(f"Error: {e}", True))
            logger.error(f"Error generating stereogram: {e}")
        finally:
            self.root.after(0, self.hide_loading)
            self.is_generating = False

    def adjust_contrast(self, image_array, contrast_factor):
        try:
            f = image_array.astype(np.float32)
            # Use a gentler contrast adjustment by blending the original value with the full contrast effect.
            # This prevents extreme clamping that can black out the image.
            multiplier = 0.5 * contrast_factor + 0.5  # When contrast_factor is 1.0, multiplier is 1.0
            adjusted = (f - 128) * multiplier + 128
            adjusted = np.clip(adjusted, 0, 255)
            return adjusted.astype(np.uint8)
        except Exception as e:
            logger.error(f"Error adjusting contrast: {e}")
            return image_array

    def update_result_preview(self):
        try:
            if not self.result_img:
                return
            self.update_canvas_image(self.result_canvas, self.result_img)
            self.preview_notebook.select(0)
            self.show_notification("Stereogram spell cast successfully!")
        except Exception as e:
            logger.error(f"Error updating result preview: {e}")

    def hide_loading(self):
        try:
            self.progress.stop()
            self.loading_frame.place_forget()
        except Exception as e:
            logger.error(f"Error hiding loading frame: {e}")

    def download_stereogram(self):
        try:
            if not self.result_img:
                self.show_notification("No stereogram has been generated", True)
                return
            file_format = self.format_var.get()
            file_path = filedialog.asksaveasfilename(
                title="Save Enchantment",
                defaultextension=f".{file_format}",
                filetypes=[(f"{file_format.upper()} files", f"*.{file_format}")],
                initialfile=f"stereogram.{file_format}"
            )
            if not file_path:
                return
            if file_format == "jpeg":
                quality = int(self.jpeg_quality_var.get() * 100)
                self.result_img.save(file_path, quality=quality)
            else:
                self.result_img.save(file_path)
            self.show_notification(f"Enchantment saved as {os.path.basename(file_path)}")
        except Exception as e:
            logger.error(f"Error saving stereogram: {e}")
            self.show_notification(f"Error saving file: {e}", True)

    def generate_with_ai(self):
        try:
            if self.is_generating:
                return
            prompt = self.ai_prompt.get("1.0", tk.END).strip()
            if not prompt:
                self.show_notification("Please enter an incantation", True)
                return
            gen_type = self.gen_type_var.get()
            api_key = self.api_key.get().strip() or self.default_api_key
            self.is_generating = True
            self.loading_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.loading_label.configure(text=f"Conjuring {gen_type}...")
            self.progress.start(10)
            thread = threading.Thread(target=self._generate_with_ai_thread, args=(prompt, gen_type, api_key))
            thread.daemon = True
            thread.start()
        except Exception as e:
            logger.error(f"Error initiating AI enchantment: {e}")
            self.is_generating = False

    def _generate_with_ai_thread(self, prompt, gen_type, api_key):
        try:
            if gen_type == "depthMap":
                enhanced_prompt = f"Depth map for {prompt}. Clear grayscale image with strong contrast."
            else:
                enhanced_prompt = f"{prompt}. Create a seamless repeating pattern with subtle details."
            self.root.after(0, lambda: self.loading_label.configure(text="Connecting to the arcane API..."))
            url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            payload = {
                "text_prompts": [{"text": enhanced_prompt, "weight": 1.0}],
                "cfg_scale": 7,
                "height": 512,
                "width": 512,
                "samples": 1,
                "steps": 30
            }
            self.root.after(0, lambda: self.loading_label.configure(text="Awaiting the oracle's response..."))
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code != 200:
                error_message = f"API error: {response.status_code}"
                try:
                    error_json = response.json()
                    if "message" in error_json:
                        error_message += f" - {error_json['message']}"
                except:
                    pass
                logger.error(f"API error details: {response.text}")
                raise Exception(error_message)
            response_json = response.json()
            if "artifacts" in response_json and len(response_json["artifacts"]) > 0:
                image_data = base64.b64decode(response_json["artifacts"][0]["base64"])
                image = Image.open(BytesIO(image_data))
            else:
                raise Exception("No image data found in API response")
            if gen_type == "depthMap":
                if image.mode != "L":
                    image = image.convert("L")
                self.depth_img = image
                self.depth_array = np.array(image)
                self.root.after(0, lambda: self.depth_label.config(text=f"AI Generated ({prompt[:20]}...)"))
                self.root.after(0, self.update_depth_preview)
                self.root.after(0, lambda: self.preview_notebook.select(1))
                self.root.after(0, lambda: self.show_notification("AI depth map conjured successfully"))
            else:
                if image.mode != "RGB":
                    image = image.convert("RGB")
                self.pattern_img = image
                self.pattern_array = np.array(image)
                self.root.after(0, lambda: self.pattern_label.config(text=f"AI Generated ({prompt[:20]}...)"))
                self.root.after(0, self.update_pattern_preview)
                self.root.after(0, lambda: self.preview_notebook.select(2))
                self.root.after(0, lambda: self.show_notification("AI pattern conjured successfully"))
            if self.depth_img and self.pattern_img:
                self.root.after(0, lambda: self.show_notification("Both magical ingredients acquired. Ready to cast the spell!"))
        except Exception as e:
            logger.error(f"Error in AI enchantment: {e}")
            self.root.after(0, lambda: self.show_notification(f"Error: {e}", True))
        finally:
            self.root.after(0, self.hide_loading)
            self.is_generating = False

    def embed_message(self, image, message):
        try:
            if image.mode != "RGB":
                image = image.convert("RGB")
            img_array = np.array(image)
            height, width, _ = img_array.shape
            message_bytes = message.encode('utf-8')
            length = len(message_bytes)
            message_data = length.to_bytes(4, byteorder='big') + message_bytes
            max_bytes = (height * width * 3) // 8
            if len(message_data) > max_bytes:
                raise ValueError(f"Message too large: {len(message_data)} bytes exceeds maximum of {max_bytes} bytes")
            binary_message = ''.join(format(byte, '08b') for byte in message_data)
            data_index = 0
            for y in range(height):
                for x in range(width):
                    for c in range(3):
                        if data_index < len(binary_message):
                            img_array[y, x, c] = (img_array[y, x, c] & 0xFE) | int(binary_message[data_index])
                            data_index += 1
                        else:
                            break
                    if data_index >= len(binary_message):
                        break
                if data_index >= len(binary_message):
                    break
            return Image.fromarray(img_array)
        except Exception as e:
            logger.error(f"Error embedding message: {e}")
            return image

    def extract_message(self, image):
        try:
            if image.mode != "RGB":
                image = image.convert("RGB")
            img_array = np.array(image)
            height, width, _ = img_array.shape
            binary_data = ''
            for y in range(height):
                for x in range(width):
                    for c in range(3):
                        binary_data += str(img_array[y, x, c] & 1)
                        if len(binary_data) == 32:
                            length = int(binary_data[:32], 2)
                            total_bits_needed = 32 + (length * 8)
                            while len(binary_data) < total_bits_needed:
                                y_pos = (y * width * 3 + x * 3 + c + 1) // (width * 3)
                                x_pos = ((y * width * 3 + x * 3 + c + 1) // 3) % width
                                c_pos = (y * width * 3 + x * 3 + c + 1) % 3
                                if y_pos >= height:
                                    return "[ERR] Message data incomplete"
                                binary_data += str(img_array[y_pos, x_pos, c_pos] & 1)
                            message_bits = binary_data[32:total_bits_needed]
                            message_bytes = bytearray(int(message_bits[i:i+8], 2) for i in range(0, len(message_bits), 8))
                            try:
                                return message_bytes.decode('utf-8')
                            except UnicodeDecodeError:
                                return "[ERR] Invalid UTF-8 data"
            return "[ERR] No hidden message found"
        except Exception as e:
            logger.error(f"Error extracting message: {e}")
            return f"[ERR] Failed to extract message: {e}"

    def show_decode_dialog(self):
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("Reveal Secret Spell")
            dialog.geometry("400x300")
            dialog.configure(bg=self.bg_color)
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()
            content = ttk.Frame(dialog)
            content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            ttk.Label(content, text="Reveal Secret Spell", style="TLabel", font=("Segoe UI", 16, "bold")).pack(pady=(0, 15))
            file_frame = ttk.Frame(content)
            file_frame.pack(fill=tk.X, pady=5)
            file_path_var = tk.StringVar()
            ttk.Label(file_frame, text="Select image with secret spell:", style="TLabel").pack(anchor=tk.W)
            file_button_frame = ttk.Frame(file_frame)
            file_button_frame.pack(fill=tk.X, pady=5)
            ttk.Button(file_button_frame, text="Browse...", command=lambda: self.select_decode_file(file_path_var)).pack(side=tk.LEFT, padx=(0, 5))
            file_label = ttk.Label(file_button_frame, text="No file selected", style="TLabel")
            file_label.pack(side=tk.LEFT, fill=tk.X)
            ttk.Label(content, text="Decoded spell:", style="TLabel").pack(anchor=tk.W, pady=(10, 5))
            decoded_text = scrolledtext.ScrolledText(content, height=6, bg="#1E1E1E", fg=self.text_color)
            decoded_text.pack(fill=tk.X, pady=5)
            ttk.Button(content, text="Reveal Spell", style="Primary.TButton",
                       command=lambda: self.decode_message(file_path_var.get(), decoded_text)).pack(fill=tk.X, pady=5)
            ttk.Button(content, text="Close", command=dialog.destroy).pack(fill=tk.X, pady=5)
            def update_file_label(*args):
                file_label.config(text=os.path.basename(file_path_var.get()) if file_path_var.get() else "No file selected")
            file_path_var.trace_add("write", update_file_label)
            dialog.update_idletasks()
            width = dialog.winfo_width()
            height = dialog.winfo_height()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
            dialog.geometry(f"+{x}+{y}")
        except Exception as e:
            logger.error(f"Error showing decode dialog: {e}")

    def select_decode_file(self, path_var):
        try:
            file_path = filedialog.askopenfilename(
                title="Select Image with Secret Spell",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
            )
            if file_path:
                path_var.set(file_path)
        except Exception as e:
            logger.error(f"Error selecting decode file: {e}")

    def decode_message(self, file_path, output_text):
        try:
            if not file_path:
                self.show_notification("Please select an image file", True)
                return
            img = Image.open(file_path)
            message = self.extract_message(img)
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", message)
            if message.startswith("[ERR]"):
                self.show_notification("Error decoding spell", True)
            else:
                self.show_notification("Spell revealed successfully!")
        except Exception as e:
            logger.error(f"Error decoding message: {e}")
            output_text.delete("1.0", tk.END)
            output_text.insert("1.0", f"[ERR] Failed to decode: {e}")
            self.show_notification(f"Error: {e}", True)

    def show_help(self):
        try:
            dialog = tk.Toplevel(self.root)
            dialog.title("About Stereogram Sorcery")
            dialog.geometry("600x500")
            dialog.configure(bg=self.bg_color)
            dialog.transient(self.root)
            dialog.grab_set()
            canvas = tk.Canvas(dialog, bg=self.bg_color, highlightthickness=0)
            scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
            content = ttk.Frame(canvas)
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")
            ttk.Label(content, text="Stereogram Sorcery", style="TLabel", font=("Segoe UI", 16, "bold")).pack(pady=(20, 10))
            self.add_help_section(content, "What are Stereograms?", [
                "Stereograms are mystical images that reveal a hidden 3D illusion when viewed correctly.",
                "To see the magic:",
                "1. Get close to the screen",
                "2. Let your eyes relax as if gazing into the void",
                "3. Slowly step back until the hidden world emerges."
            ])
            self.add_help_section(content, "Casting the Spell", [
                "Depth Map: Your blueprint of depth; white is near, black is distant.",
                "Pattern: A repeating texture that creates the illusion.",
                "Shift Strength: Controls the intensity of the 3D effect."
            ])
            self.add_help_section(content, "AI Enchantment", [
                "Use descriptive incantations to summon depth maps or patterns using Stability AI.",
                "The API key can be updated in the Mystic API Portal."
            ])
            self.add_help_section(content, "Secret Spells", [
                "Hide secret messages within your stereogram using ancient LSB steganography.",
                "Note: Only PNG preserves the hidden spells flawlessly."
            ])
            ttk.Button(content, text="Close", command=dialog.destroy, style="Primary.TButton").pack(pady=20)
            def configure_canvas(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=event.width)
            content.bind("<Configure>", configure_canvas)
            canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
            dialog.update_idletasks()
            width = dialog.winfo_width()
            height = dialog.winfo_height()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
            dialog.geometry(f"+{x}+{y}")
        except Exception as e:
            logger.error(f"Error showing help: {e}")

    def add_help_section(self, parent, title, paragraphs):
        try:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, padx=20, pady=10)
            ttk.Label(frame, text=title, style="TLabel", font=("Segoe UI", 12, "bold")).pack(fill=tk.X, pady=(0, 5))
            for paragraph in paragraphs:
                ttk.Label(frame, text=paragraph, wraplength=500, justify=tk.LEFT, style="TLabel").pack(fill=tk.X, padx=10, pady=2, anchor=tk.W)
        except Exception as e:
            logger.error(f"Error adding help section: {e}")

def main():
    try:
        root = tk.Tk()
        app = StereogramSorcery(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        messagebox.showerror("Critical Error", f"An unexpected error occurred: {e}\n\nSee console for details.")

if __name__ == "__main__":
    main()
