from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import os
from typing import Tuple, Optional, List
import math

class ImageProcessor:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = None
        self.original_image = None
        self.load_image()
    
    def load_image(self):
        try:
            self.image = Image.open(self.image_path)
            self.original_image = self.image.copy()
            print(f"Loaded image: {self.image_path}")
            print(f"Original size: {self.image.size}")
            print(f"Format: {self.image.format}")
            print(f"Mode: {self.image.mode}")
        except Exception as e:
            print(f"Error loading image: {e}")
            raise
    
    def resize(self, width: int, height: int, maintain_aspect: bool = True) -> 'ImageProcessor':
        if maintain_aspect:
            self.image.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        
        print(f"Resized to: {self.image.size}")
        return self
    
    def resize_by_percentage(self, percentage: float) -> 'ImageProcessor':
        width, height = self.image.size
        new_width = int(width * percentage / 100)
        new_height = int(height * percentage / 100)
        return self.resize(new_width, new_height, maintain_aspect=False)
    
    def crop(self, left: int, top: int, right: int, bottom: int) -> 'ImageProcessor':
        self.image = self.image.crop((left, top, right, bottom))
        print(f"Cropped to: {self.image.size}")
        return self
    
    def crop_center(self, width: int, height: int) -> 'ImageProcessor':
        img_width, img_height = self.image.size
        left = (img_width - width) // 2
        top = (img_height - height) // 2
        right = left + width
        bottom = top + height
        return self.crop(left, top, right, bottom)
    
    def rotate(self, angle: float, expand: bool = True) -> 'ImageProcessor':
        self.image = self.image.rotate(angle, expand=expand, fillcolor='white')
        print(f"Rotated by {angle} degrees")
        return self
    
    def flip_horizontal(self) -> 'ImageProcessor':
        self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        print("Flipped horizontally")
        return self
    
    def flip_vertical(self) -> 'ImageProcessor':
        self.image = self.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        print("Flipped vertically")
        return self
    
    def convert_to_grayscale(self) -> 'ImageProcessor':
        self.image = self.image.convert('L')
        print("Converted to grayscale")
        return self
    
    def convert_to_rgb(self) -> 'ImageProcessor':
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
        print("Converted to RGB")
        return self
    
    def apply_blur(self, radius: float = 2.0) -> 'ImageProcessor':
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=radius))
        print(f"Applied blur (radius: {radius})")
        return self
    
    def apply_sharpen(self) -> 'ImageProcessor':
        self.image = self.image.filter(ImageFilter.SHARPEN)
        print("Applied sharpen filter")
        return self
    
    def adjust_brightness(self, factor: float) -> 'ImageProcessor':
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        print(f"Adjusted brightness by factor {factor}")
        return self
    
    def adjust_contrast(self, factor: float) -> 'ImageProcessor':
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        print(f"Adjusted contrast by factor {factor}")
        return self
    
    def adjust_saturation(self, factor: float) -> 'ImageProcessor':
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        print(f"Adjusted saturation by factor {factor}")
        return self
    
    def add_text(self, text: str, position: Tuple[int, int], 
                 font_size: int = 20, color: str = 'white') -> 'ImageProcessor':
        draw = ImageDraw.Draw(self.image)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        draw.text(position, text, fill=color, font=font)
        print(f"Added text: '{text}' at position {position}")
        return self
    
    def add_watermark(self, text: str, opacity: float = 0.5) -> 'ImageProcessor':
        watermark = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.image.size[0] - text_width) // 2
        y = (self.image.size[1] - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255, int(255 * opacity)), font=font)
        
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')
        
        self.image = Image.alpha_composite(self.image, watermark)
        print(f"Added watermark: '{text}'")
        return self
    
    def create_thumbnail(self, size: Tuple[int, int] = (128, 128)) -> 'ImageProcessor':
        self.image.thumbnail(size, Image.Resampling.LANCZOS)
        print(f"Created thumbnail: {self.image.size}")
        return self
    
    def reset(self) -> 'ImageProcessor':
        self.image = self.original_image.copy()
        print("Reset to original image")
        return self
    
    def save(self, output_path: str, format: Optional[str] = None, quality: int = 95):
        if format is None:
            format = self.image.format or 'PNG'
        
        save_kwargs = {'format': format}
        
        if format.upper() in ['JPEG', 'JPG']:
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
            if self.image.mode in ['RGBA', 'LA']:
                self.image = self.image.convert('RGB')
        
        self.image.save(output_path, **save_kwargs)
        print(f"Saved image to: {output_path}")
        print(f"Format: {format}, Size: {self.image.size}")

class BatchImageProcessor:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def get_image_files(self) -> List[str]:
        image_files = []
        for file in os.listdir(self.input_dir):
            if file.lower().endswith(self.supported_formats):
                image_files.append(os.path.join(self.input_dir, file))
        return image_files
    
    def resize_all(self, width: int, height: int, maintain_aspect: bool = True):
        image_files = self.get_image_files()
        print(f"Found {len(image_files)} images to process")
        
        for image_path in image_files:
            try:
                processor = ImageProcessor(image_path)
                processor.resize(width, height, maintain_aspect)
                
                filename = os.path.basename(image_path)
                output_path = os.path.join(self.output_dir, filename)
                processor.save(output_path)
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")
    
    def create_thumbnails_all(self, size: Tuple[int, int] = (128, 128)):
        image_files = self.get_image_files()
        print(f"Creating thumbnails for {len(image_files)} images")
        
        for image_path in image_files:
            try:
                processor = ImageProcessor(image_path)
                processor.create_thumbnail(size)
                
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(self.output_dir, f"{name}_thumb{ext}")
                processor.save(output_path)
                
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

def create_sample_image():
    sample_image = Image.new('RGB', (400, 300), color='lightblue')
    draw = ImageDraw.Draw(sample_image)
    
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((150, 130), "Sample Image", fill='darkblue', font=font)
    draw.rectangle([50, 50, 350, 250], outline='darkblue', width=3)
    
    sample_image.save('sample_image.png')
    print("Created sample image: sample_image.png")

def main():
    print("Image Processing Examples")
    print("=" * 50)
    
    create_sample_image()
    
    print("\n1. Basic image operations:")
    processor = ImageProcessor('sample_image.png')
    
    processor.resize(300, 200).rotate(45).adjust_brightness(1.2)
    processor.save('processed_image.png')
    
    print("\n2. Advanced operations:")
    processor.reset().convert_to_grayscale().apply_blur(1.5)
    processor.save('grayscale_blur.png')
    
    print("\n3. Text and watermark:")
    processor.reset().add_text("Hello World!", (50, 50), font_size=30, color='red')
    processor.add_watermark("WATERMARK", opacity=0.3)
    processor.save('text_watermark.png')
    
    print("\n4. Batch processing:")
    os.makedirs('batch_input', exist_ok=True)
    os.makedirs('batch_output', exist_ok=True)
    
    for i in range(3):
        img = Image.new('RGB', (200 + i*50, 150 + i*50), 
                       color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        img.save(f'batch_input/image_{i+1}.png')
    
    batch_processor = BatchImageProcessor('batch_input', 'batch_output')
    batch_processor.resize_all(150, 150, maintain_aspect=True)
    batch_processor.create_thumbnails_all((64, 64))
    
    print("\nImage processing completed!")

if __name__ == "__main__":
    import random
    main()