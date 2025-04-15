import tkinter as tk
from PIL import ImageTk, Image
import os
import json

class ImageViewer:
    def __init__(self, root, image_folder):
        self.root = root
        self.image_folder = image_folder
        
        with open('src\\packageInfo.json', 'r', encoding='utf-8') as f:
            packageInfo = json.load(f)
        
        self.rating = [f for f in packageInfo]
            
        # Get list of image files
        self.images = [f["imagePath"] for f in packageInfo]
        self.current_index = 0
        
        # Create UI elements
        self.setup_ui()
        
    def setup_ui(self):
        # Frame for buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        next_button = tk.Button(button_frame, text="bad", 
                            command=self.badImage)
        next_button.pack(side=tk.LEFT, padx=5)
        next_button = tk.Button(button_frame, text="good", 
                            command=self.goodImage)
        next_button.pack(side=tk.LEFT, padx=5)
        next_button = tk.Button(button_frame, text="misc", 
                            command=self.miscImage)
        next_button.pack(side=tk.LEFT, padx=5)
        
        # Frame for image
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10)
        
        # Initialize image display
        self.show_current_image()
    
    def show_current_image(self):
        # Clear previous image
        for widget in self.image_frame.winfo_children():
            widget.destroy()
            
        # Load and display current image
        image_path = os.path.join(self.image_folder, self.images[self.current_index])
        image = Image.open(image_path)
        
        # Resize image if it's too large
        max_size = 800
        if max(image.size) > max_size:
            scale = max_size / max(image.size)
            new_size = tuple(int(dim * scale) for dim in image.size)
            image = image.resize(new_size)
        
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.image_frame, image=photo)
        label.image = photo  # Keep a reference!
        label.pack()
        
    def goodImage(self):
        if len(self.images) <= 1:
            return
        self.rating[self.current_index]['good']=True
        self.current_index = (self.current_index + 1) % len(self.images)
        print(self.current_index)
        if self.current_index == 0:
            self.saveData()
            print(self.rating)
            quit()
        self.show_current_image()

    def badImage(self):
        if len(self.images) <= 1:
            return
        self.rating[self.current_index]['good']=False
        self.current_index = (self.current_index + 1) % len(self.images)
        print(self.current_index)
        if self.current_index == 0:
            self.saveData()
            print(self.rating)
            quit()
        self.show_current_image()
    
    def saveData(self):
        with open('src\\exportData.json', 'w', encoding='utf-8') as f:
            json.dump(self.rating, f)
    
    def miscImage(self):
        if len(self.images) <= 1:
            return
        self.rating[self.current_index]['good']='misc'
        self.current_index = (self.current_index + 1) % len(self.images)
        print(self.current_index)
        if self.current_index == 0:
            self.saveData()
            print(self.rating)
            quit()
        self.show_current_image()
def main():
    # Create main window
    root = tk.Tk()
    root.title("Website Rater")
    
    # Replace 'your_images_folder' with your actual folder path
    viewer = ImageViewer(root, 'src')
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()