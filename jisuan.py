from PIL import Image
import numpy as np
import os


def calculate_iou(gt, pred):
    """计算单张图片的IoU"""
    intersection = np.logical_and(gt, pred)
    union = np.logical_or(gt, pred)
    iou = np.sum(intersection) / np.sum(union)
    return iou


def calculate_pixel_accuracy(gt, pred):
    """计算单张图片的Pixel Accuracy"""
    correct = np.sum(gt == pred)
    total = gt.size
    return correct / total


def calculate_accuracy(gt, pred):
    """计算单张图片的Accuracy"""
    correct = np.sum(gt == pred)
    total = gt.size
    return correct / total


def load_images(folder1, folder2):
    """从两个文件夹中加载图片，并计算平均mIoU、mPA和Acc"""
    ious = []
    pas = []
    accs = []

    # 确保文件夹1和文件夹2中图片数量相同且对应相匹配
    for filename in os.listdir(folder1):
        if filename.endswith('.jpg'):
            gt_path = os.path.join(folder1, filename)
            pred_path = os.path.join(folder2, filename)

            gt_image = Image.open(gt_path)
            pred_image = Image.open(pred_path)

            gt = np.array(gt_image) > 128  # 将图像二值化
            pred = np.array(pred_image) > 128  # 将图像二值化

            ious.append(calculate_iou(gt, pred))
            pas.append(calculate_pixel_accuracy(gt, pred))
            accs.append(calculate_accuracy(gt, pred))

    # 计算指标的平均值
    mean_iou = np.mean(ious)
    mean_pa = np.mean(pas)
    mean_acc = np.mean(accs)

    return mean_iou, mean_pa, mean_acc


# 示例用法
folder1 = 'C:/Users/WXH/Desktop/jieguo/gt'  # 实际标注（ground truth）文件夹路径
folder2 = 'C:/Users/WXH/Desktop/jieguo/simple'  # 预测结果文件夹路径

mean_iou, mean_pa, mean_acc = load_images(folder1, folder2)
print(f"Average mIoU: {mean_iou:.4f}")
print(f"Average mPA: {mean_pa:.4f}")
print(f"Average Acc: {mean_acc:.4f}")

