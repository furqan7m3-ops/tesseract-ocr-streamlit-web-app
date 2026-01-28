"""Tkinter GUI for OCR application."""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
from pathlib import Path

from OCR.text_extractor import extract_text, extract_text_with_formatting
from OCR.image_preprocessor import preprocess_image, enhance_contrast, deskew_image, optimal_pipeline
from OCR.word_generator import create_ocr_document


class OCRApplication:
    """Main OCR Application GUI using Tkinter."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tesseract OCR Text Extractor")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables
        self.current_image_path = tk.StringVar()
        self.extracted_text = tk.StringVar()
        self.current_image = None
        self.is_processing = False
        
        # Setup GUI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Tesseract OCR Text Extractor", 
                                font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Main content frame (two columns)
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Image display and controls
        left_frame = ttk.LabelFrame(content_frame, text="Image", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Image display area
        self.image_label = ttk.Label(left_frame, text="No image loaded", 
                                     background="#f0f0f0", relief=tk.SUNKEN)
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons for image
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X)
        
        load_btn = ttk.Button(button_frame, text="Load Image", command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        preprocess_btn = ttk.Button(button_frame, text="Preprocess", command=self.preprocess_current)
        preprocess_btn.pack(side=tk.LEFT, padx=5)
        
        enhance_btn = ttk.Button(button_frame, text="Enhance Contrast", command=self.enhance_current)
        enhance_btn.pack(side=tk.LEFT, padx=5)
        
        deskew_btn = ttk.Button(button_frame, text="Deskew", command=self.deskew_current)
        deskew_btn.pack(side=tk.LEFT, padx=5)
        
        optimal_btn = ttk.Button(button_frame, text="🚀 Optimal Pipeline", command=self.optimal_pipeline_current)
        optimal_btn.pack(side=tk.LEFT, padx=5)
        
        # Right panel - Text extraction and options
        right_frame = ttk.LabelFrame(content_frame, text="OCR Results", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Processing options
        options_frame = ttk.LabelFrame(right_frame, text="Options", padding=5)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.with_formatting = tk.BooleanVar(value=True)
        format_check = ttk.Checkbutton(options_frame, text="Detect Formatting", 
                                       variable=self.with_formatting)
        format_check.pack(side=tk.LEFT, padx=5)
        
        # Extract text button
        extract_frame = ttk.Frame(right_frame)
        extract_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.extract_btn = ttk.Button(extract_frame, text="Extract Text", 
                                      command=self.extract_text_action)
        self.extract_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(extract_frame, variable=self.progress_var, 
                                        maximum=100, mode='indeterminate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Text display area with scrollbar
        text_frame = ttk.Frame(right_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.text_display = scrolledtext.ScrolledText(text_frame, height=15, 
                                                       wrap=tk.WORD, font=("Courier", 10))
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(right_frame)
        bottom_frame.pack(fill=tk.X)
        
        save_text_btn = ttk.Button(bottom_frame, text="Save Text", 
                                   command=self.save_text_to_file)
        save_text_btn.pack(side=tk.LEFT, padx=5)
        
        save_word_btn = ttk.Button(bottom_frame, text="Save as Word Doc", 
                                   command=self.save_as_word)
        save_word_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = ttk.Button(bottom_frame, text="Copy to Clipboard", 
                              command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(bottom_frame, text="Clear", 
                               command=self.clear_text)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=5, pady=5)
    
    def load_image(self):
        """Load image from file dialog."""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), 
                      ("All Files", "*.*")]
        )
        
        if file_path:
            self.current_image_path.set(file_path)
            self.display_image(file_path)
            self.status_var.set(f"Loaded: {Path(file_path).name}")
    
    def display_image(self, image_path):
        """Display image in the image label."""
        try:
            img = Image.open(image_path)
            # Resize to fit label (max 300x300)
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image, text="")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
    
    def extract_text_action(self):
        """Extract text from image with threading."""
        if not self.current_image_path.get():
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        # Run extraction in separate thread to avoid freezing UI
        thread = threading.Thread(target=self._extract_text_thread)
        thread.start()
    
    def _extract_text_thread(self):
        """Extract text in separate thread."""
        try:
            self.is_processing = True
            self.extract_btn.config(state=tk.DISABLED)
            self.progress.start()
            self.status_var.set("Processing...")
            
            image_path = self.current_image_path.get()
            
            if self.with_formatting.get():
                result = extract_text_with_formatting(image_path)
                text = result.get('text', '')
                self.formatting_info = result
            else:
                text = extract_text(image_path)
                self.formatting_info = None
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(1.0, text)
            self.extracted_text.set(text)
            
            self.status_var.set(f"Extracted {len(text)} characters")
        
        except Exception as e:
            messagebox.showerror("Error", f"Text extraction failed: {str(e)}")
            self.status_var.set("Error during extraction")
        
        finally:
            self.progress.stop()
            self.extract_btn.config(state=tk.NORMAL)
            self.is_processing = False
    
    def preprocess_current(self):
        """Preprocess current image."""
        if not self.current_image_path.get():
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            self.status_var.set("Preprocessing...")
            self.root.update()
            
            img = Image.open(self.current_image_path.get())
            preprocessed = preprocess_image(img)
            
            # Save preprocessed image
            output_path = "preprocessed_temp.png"
            preprocessed.save(output_path)
            
            self.current_image_path.set(output_path)
            self.display_image(output_path)
            self.status_var.set("Image preprocessed")
        
        except Exception as e:
            messagebox.showerror("Error", f"Preprocessing failed: {str(e)}")
    
    def enhance_current(self):
        """Enhance contrast of current image."""
        if not self.current_image_path.get():
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            self.status_var.set("Enhancing contrast...")
            self.root.update()
            
            img = Image.open(self.current_image_path.get())
            enhanced = enhance_contrast(img)
            
            # Save enhanced image
            output_path = "enhanced_temp.png"
            enhanced.save(output_path)
            
            self.current_image_path.set(output_path)
            self.display_image(output_path)
            self.status_var.set("Contrast enhanced")
        
        except Exception as e:
            messagebox.showerror("Error", f"Enhancement failed: {str(e)}")
    
    def deskew_current(self):
        """Deskew current image."""
        if not self.current_image_path.get():
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            self.status_var.set("Deskewing image...")
            self.root.update()
            
            img = Image.open(self.current_image_path.get())
            deskewed = deskew_image(img)
            
            # Save deskewed image
            output_path = "deskewed_temp.png"
            deskewed.save(output_path)
            
            self.current_image_path.set(output_path)
            self.display_image(output_path)
            self.status_var.set("Image deskewed")
        
        except Exception as e:
            messagebox.showerror("Error", f"Deskewing failed: {str(e)}")
    
    def optimal_pipeline_current(self):
        """Apply optimal preprocessing pipeline."""
        if not self.current_image_path.get():
            messagebox.showwarning("Warning", "Please load an image first")
            return
        
        try:
            self.status_var.set("Applying optimal pipeline...")
            self.root.update()
            
            img = Image.open(self.current_image_path.get())
            optimized = optimal_pipeline(img)
            
            # Save optimized image
            output_path = "optimal_temp.png"
            optimized.save(output_path)
            
            self.current_image_path.set(output_path)
            self.display_image(output_path)
            self.status_var.set("Optimal pipeline applied (Deskew → Enhance → Preprocess)")
        
        except Exception as e:
            messagebox.showerror("Error", f"Pipeline failed: {str(e)}")
    
    def save_text_to_file(self):
        """Save extracted text to file."""
        text = self.text_display.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "No text to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Success", f"Text saved to {file_path}")
                self.status_var.set(f"Saved to {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
    
    def save_as_word(self):
        """Save extracted text as Word document."""
        text = self.text_display.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "No text to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Files", "*.docx"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                create_ocr_document(
                    text,
                    image_path=self.current_image_path.get() if self.current_image_path.get() else None,
                    formatting_info=getattr(self, 'formatting_info', None),
                    output_path=file_path
                )
                messagebox.showinfo("Success", f"Document saved to {file_path}")
                self.status_var.set(f"Saved to {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create document: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy extracted text to clipboard."""
        text = self.text_display.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Warning", "No text to copy")
            return
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
            self.status_var.set("Copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy: {str(e)}")
    
    def clear_text(self):
        """Clear text display."""
        self.text_display.delete(1.0, tk.END)
        self.status_var.set("Cleared")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = OCRApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
