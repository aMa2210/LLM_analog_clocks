import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import FancyArrowPatch
from PIL import Image
import pandas as pd

def draw_bezier_curve(fig, angle, width, file_name):
    angle = angle * 180 / np.pi

    # 打开PNG图片
    png_img = Image.open(file_name)

    # 计算图片的宽度和高度
    width_percent = (width / float(png_img.size[0]))  # 宽度的百分比
    new_height = int((float(png_img.size[1]) * float(width_percent)))  # 按比例计算新的高度
    png_img = png_img.resize((width, new_height))

    # 旋转PNG图片
    png_img = png_img.rotate(angle, expand=True)  # expand=True让图片适应旋转后的内容

    # 将图片转换为NumPy数组
    png_array = np.array(png_img)

    # 获取画布的大小
    fig_width, fig_height = fig.get_size_inches() * fig.dpi
    rotated_width, rotated_height = png_img.size

    # 计算PNG图片的左上角位置，使其居中
    x_offset = (fig_width - rotated_width) / 2 - 58  # 水平居中
    y_offset = (fig_height - rotated_height) / 2 - 60 # 垂直居中

    # 使用fig.figimage将图片叠加到图表上
    fig.figimage(png_array, xo=int(x_offset), yo=int(y_offset), alpha=1)


def draw_clock(hours, minutes, seconds, save_path):
    fig = plt.figure(figsize=(6, 6))  # 仅使用fig，而不创建ax
    fig.set_dpi(100)  # 设置dpi，确保图像的大小与分辨率合适

    # Draw the main circle of the clock (手动绘制时钟的圆形)
    circle = plt.Circle((0, 0), radius=1, fc="#ffffff", ec="black", lw=3)
    fig.gca().add_artist(circle)

    # Draw the ticks for hours, minutes, and seconds (绘制时钟的刻度)
    for i in range(60):
        tick_angle = np.pi / 30 * i
        if i % 5 == 0:
            length = 0.1  # longer tick every 5 minutes (for hours)
            lw = 3
        else:
            length = 0.05  # shorter tick for minutes and seconds
            lw = 1
        x_in = (1 - length) * np.cos(tick_angle)
        y_in = (1 - length) * np.sin(tick_angle)
        x_out = np.cos(tick_angle)
        y_out = np.sin(tick_angle)
        fig.gca().plot([x_in, x_out], [y_in, y_out], lw=lw, color="black")

    # Add clock numbers (添加数字)
    for number in range(1, 13):
        number_angle = np.pi / 6 * (3 - number)
        x_num = 0.8 * np.cos(number_angle)
        y_num = 0.8 * np.sin(number_angle)
        fig.gca().text(x_num, y_num, str(number), ha="center", va="center", fontsize=16, fontweight="bold")

    # Calculate angles for the clock hands (计算指针角度)
    hour_angle = np.pi / 6 * (3 - (hours % 12) - minutes / 60 - seconds / 3600)
    minute_angle = np.pi / 30 * (15 - minutes - seconds / 60)
    second_angle = np.pi / 30 * (15 - seconds)

    # Draw clock hands (images)
    draw_bezier_curve(fig, hour_angle, 250, '1.png')
    draw_bezier_curve(fig, minute_angle, 300, '2.png')
    draw_bezier_curve(fig, second_angle, 400, '3.png')

    # Decorative center dot (装饰性中心点)
    fig.gca().add_artist(plt.Circle((0, 0), radius=0.02, fc="black"))

    # Hide axes (隐藏坐标轴)
    plt.axis("off")
    plt.xlim(-1.05, 1.05)
    plt.ylim(-1.05, 1.05)

    # Show the figure
    plt.show()

    # Save the image
    # plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
    # plt.close(fig)


draw_clock(10, 45, 30, "path")


# folder_path = 'clock_twisted_hands_dataset'
# # Create dataset folder
# os.makedirs(folder_path, exist_ok=True)
#
#
# file_path = 'train-00000-of-00004.parquet'
# df = pd.read_parquet(file_path)
# df = df.head(150)
#
# for index, row in df.iterrows():
#     a = row['answer']
#     hour_24, minute, second = a.split(":")
#     hour_24 = int(hour_24)
#     minute = int(minute)
#     second = int(second)
#     hour_12 = hour_24 % 12
#     hour_12 = 12 if hour_12 == 0 else hour_12  # convert 0 hour to 12
#     filename = f"{hour_12:02d}_{minute:02d}_{second:02d}.png"
#     path = os.path.join(folder_path, filename)
#     draw_clock(hour_24, minute, second, path)




#
# # Generate images from 12_00_00.png to 11_59_59.png (12-hour format)
# for hour_24 in range(12):
#     hour_12 = hour_24 % 12
#     hour_12 = 12 if hour_12 == 0 else hour_12  # convert 0 hour to 12
#     for minute in range(60):
#         for second in range(60):
#             filename = f"{hour_12:02d}_{minute:02d}_{second:02d}.png"
#             path = os.path.join(folder_path, filename)
#             draw_clock(hour_24, minute, second, path)

print("✅ Clock image dataset generated successfully!")
