from PIL import Image

def resize_and_crop(input_path, output_path, target_width, target_height):
    # Rasmni ochish
    img = Image.open(input_path)
    
    # Rasmni nisbatini hisoblash
    width, height = img.size
    target_ratio = target_width / target_height
    img_ratio = width / height

    if img_ratio > target_ratio:
        # Rasm juda keng, yon tomonlarini qirqamiz
        new_width = int(target_ratio * height)
        offset = (width - new_width) // 2
        img = img.crop((offset, 0, width - offset, height))
    else:
        # Rasm juda baland, tepa va pastini qirqamiz
        new_height = int(width / target_ratio)
        offset = (height - new_height) // 2
        img = img.crop((0, offset, width, height - offset))

    # Oxirgi o'lchamga keltirish (640x360)
    img = img.resize((target_width, target_height), Image.LANCZOS)
    
    # Saqlash
    img.save(output_path, quality=95)
    print(f"Rasm tayyor: {output_path}")

# Ishlatish:
resize_and_crop("image.png", "description_pic.png", 640, 360)