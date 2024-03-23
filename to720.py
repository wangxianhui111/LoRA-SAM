import os
from PIL import Image

# 指定输入文件夹和输出文件夹
input_folder = "C:/Users/WXH/Desktop/shiyanjieguo2"
output_folder = "C:/Users/WXH/Desktop/shiyanjieguo2"

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有图片文件
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # 打开图片文件
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path)

        # 计算缩放比例
        width, height = image.size
        aspect_ratio = width / height
        if aspect_ratio > 1:
            new_width = 720
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 720
            new_width = int(new_height * aspect_ratio)

        # 缩放图片
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 创建一个720×720的空白图片
        final_image = Image.new("RGB", (720, 720), (0, 0, 0))

        # 计算粘贴位置
        paste_x = (720 - new_width) // 2
        paste_y = (720 - new_height) // 2

        # 将缩放后的图片粘贴到空白图片上
        final_image.paste(resized_image, (paste_x, paste_y))

        # 保存处理后的图片到输出文件夹
        output_path = os.path.join(output_folder, filename)
        final_image.save(output_path)

print("图片缩放完成！")