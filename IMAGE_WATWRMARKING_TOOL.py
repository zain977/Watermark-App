import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os

# إعدادات الواجهة
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WatermarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Watermark Tool")
        self.geometry("600x500")
        self.resizable(False, False)

        self.image_path = None

        # عنوان
        self.title_label = ctk.CTkLabel(self, text="Image Watermark Tool", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        # زرار رفع صورة
        self.upload_btn = ctk.CTkButton(self, text="Upload Image", command=self.upload_image, width=200, height=40)
        self.upload_btn.pack(pady=10)

        # إدخال النص
        self.watermark_entry = ctk.CTkEntry(self, placeholder_text="Enter Watermark Text", width=400, height=40, font=("Arial", 14))
        self.watermark_entry.pack(pady=15)

        # اختيار مكان العلامة
        self.position_label = ctk.CTkLabel(self, text="Select Watermark Position:", font=("Arial", 14))
        self.position_label.pack(pady=5)

        self.position_var = ctk.StringVar(value="Bottom Right")
        self.position_menu = ctk.CTkOptionMenu(self, variable=self.position_var, values=["Top Left", "Top Right", "Center", "Bottom Left", "Bottom Right"], width=200, height=35)
        self.position_menu.pack(pady=10)

        # زرار إضافة العلامة
        self.add_btn = ctk.CTkButton(self, text="Add Watermark & Save", command=self.add_watermark, width=250, height=45)
        self.add_btn.pack(pady=20)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            messagebox.showinfo("Success", "Image uploaded successfully!")

    def add_watermark(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        text = self.watermark_entry.get()
        if not text.strip():
            messagebox.showerror("Error", "Please enter watermark text.")
            return

        img = Image.open(self.image_path).convert("RGBA")
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))

        draw = ImageDraw.Draw(txt_layer)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        text_width, text_height = draw.textsize(text, font=font)

        # تحديد مكان العلامة
        pos = self.position_var.get()
        if pos == "Top Left":
            position = (10, 10)
        elif pos == "Top Right":
            position = (img.width - text_width - 10, 10)
        elif pos == "Center":
            position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
        elif pos == "Bottom Left":
            position = (10, img.height - text_height - 10)
        else:  # Bottom Right
            position = (img.width - text_width - 10, img.height - text_height - 10)

        # إضافة النص بالشفافية
        draw.text(position, text, font=font, fill=(255, 255, 255, 150))

        watermarked = Image.alpha_composite(img, txt_layer)

        # حفظ الصورة
        save_path = os.path.splitext(self.image_path)[0] + "_watermarked.png"
        watermarked.save(save_path)

        messagebox.showinfo("Done", f"Watermarked image saved:\n{save_path}")


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()