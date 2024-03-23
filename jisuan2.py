import cv2
from skimage import measure
from skimage.color import rgb2gray
from scipy.spatial.distance import directed_hausdorff
import numpy as np
from PIL import Image
import os

def load_image_as_binary(image_path):
    """加载图像并转换为二值化格式"""
    image = Image.open(image_path).convert("L")  # 转换为灰度图
    return np.array(image) > 128  # 二值化

def calculate_iou(gt, pred):
    intersection = np.logical_and(gt, pred).sum()
    union = np.logical_or(gt, pred).sum()
    return intersection / union if union != 0 else 0

def calculate_pa(gt, pred):
    return np.mean(gt == pred)


def get_boundary(mask):
    """
    从二值掩码中提取边界.

    参数:
    mask (numpy.ndarray): 二值掩码.

    返回:
    numpy.ndarray: 边界掩码.
    """
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(mask.astype(np.uint8), kernel, iterations=1)
    eroded = cv2.erode(mask.astype(np.uint8), kernel, iterations=1)
    boundary = np.logical_xor(dilated, eroded)
    return boundary
def calculate_biou(gt, pred):
    """这里简化计算，实际BIoU计算可能更复杂"""
    """
    计算 Boundary IoU (BIOU) 指标.

    参数:
    gt (numpy.ndarray): 真实边界掩码,二值图像.
    pred (numpy.ndarray): 预测边界掩码,二值图像.

    返回:
    float: BIOU 值.
    """
    # 计算真实边界和预测边界
    gt_boundary = get_boundary(gt)
    pred_boundary = get_boundary(pred)

    # 计算交集面积
    intersection = np.logical_and(gt_boundary, pred_boundary).sum()

    # 计算并集面积
    union = gt_boundary.sum() + pred_boundary.sum() - intersection

    # 计算 BIOU
    biou = intersection / union

    return biou



def calculate_assd(gt, pred):
    gt_indices = np.argwhere(gt)
    pred_indices = np.argwhere(pred)
    if not len(gt_indices) or not len(pred_indices):
        return np.inf
    u_hausdorff = directed_hausdorff(gt_indices, pred_indices)[0]
    v_hausdorff = directed_hausdorff(pred_indices, gt_indices)[0]
    return (u_hausdorff + v_hausdorff) / 2

def calculate_metrics(folder_gt, folder_pred):
    ious, pas, bious, assds = [], [], [], []
    for filename in os.listdir(folder_gt):
        gt_path = os.path.join(folder_gt, filename)
        pred_path = os.path.join(folder_pred, filename)
        if os.path.exists(pred_path):
            gt = load_image_as_binary(gt_path)
            pred = load_image_as_binary(pred_path)
            ious.append(calculate_iou(gt, pred))
            pas.append(calculate_pa(gt, pred))
            bious.append(calculate_biou(gt, pred))
            assds.append(calculate_assd(gt, pred))
    return np.mean(ious), np.mean(pas), np.mean(bious), np.mean(assds)

# 设定文件夹路径
folder_gt = 'C:/Users/WXH/Desktop/jieguo/gt'
folder_pred = 'C:/Users/WXH/Desktop/jieguo/WithoutPE'

# 计算指标
mean_iou, mean_pa, mean_biou, mean_assd = calculate_metrics(folder_gt, folder_pred)
print(f"Average mIoU: {mean_iou}")
print(f"Average mPA: {mean_pa}")
print(f"Average BIoU: {mean_biou}")
print(f"Average ASSD: {mean_assd}")
