from PIL import Image
import os

# 文件夹路径
folder_path = 'C:/Users/WXH/Desktop/jieguo/simple'

# 获取文件夹中所有文件的列表
file_list = os.listdir(folder_path)

# 过滤出图像文件
image_files = [f for f in file_list if f.endswith(('.png', '.jpeg', '.jpg', '.gif', '.bmp'))]

# 处理每个图像文件
for filename in image_files:
    file_path = os.path.join(folder_path, filename)
    try:
        # 打开图像文件
        img = Image.open(file_path)
        # 获取图像的像素值
        pixels = list(img.getdata())
        width, height = img.size
        print(f"Image: {filename}")
        print(f"Width: {width}, Height: {height}")
        print(f"Pixels: {pixels}\n")
    except Exception as e:
        print(f"Error processing {filename}: {e}")
