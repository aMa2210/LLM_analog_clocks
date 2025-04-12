import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.patches import FancyArrowPatch
from PIL import Image

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


def draw_clock(hours_indicator, minutes_indicator, seconds_indicator, save_path):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')

    # Draw the main circle of the clock
    circle = plt.Circle((0, 0), radius=1, fc="#ffffff", ec="black", lw=3)
    ax.add_patch(circle)

    # Draw the ticks for hours, minutes, and seconds
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
        ax.plot([x_in, x_out], [y_in, y_out], lw=lw, color="black")

    # Add clock numbers
    for number in range(1, 13):
        number_angle = np.pi / 6 * (3 - number)
        x_num = 0.8 * np.cos(number_angle)
        y_num = 0.8 * np.sin(number_angle)
        ax.text(x_num, y_num, str(number), ha="center", va="center", fontsize=16, fontweight="bold")
    hours = hours_indicator
    minutes = minutes_indicator
    seconds = seconds_indicator
    if not hours_indicator:
        hours = 0
    if not minutes_indicator:
        minutes = 0
    if not seconds_indicator:
        seconds = 0
    # Calculate angles for the clock hands
    # hour_angle = np.pi / 6 * (3 - (hours % 12) - minutes / 60 - seconds / 3600)
    # minute_angle = np.pi / 30 * (15 - minutes - seconds / 60)
    hour_angle = np.pi / 30 * (15 - hours)
    minute_angle = np.pi / 30 * (15 - minutes)
    second_angle = np.pi / 30 * (15 - seconds)

    # Draw clock hands
    if hours_indicator:
        draw_bezier_curve(fig, hour_angle, 250, '1.png')
    if minutes_indicator:
        draw_bezier_curve(fig, minute_angle, 300, '2.png')
    if seconds_indicator:
        draw_bezier_curve(fig, second_angle, 400, '3.png')


    # Decorative center dot
    ax.add_patch(plt.Circle((0, 0), radius=0.02, fc="black"))

    # Hide axes
    plt.axis("off")
    plt.xlim(-1.05, 1.05)
    plt.ylim(-1.05, 1.05)
    # plt.show()
    # Save the image
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    1

# draw_clock(1, 2, 13, 'None')

#
# Create dataset folder
path_folder = "clock_one_hand_twisted_dataset/Hour"
os.makedirs(path_folder, exist_ok=True)
for hour in range(60):
    if hour == 0:
        hour = 60
    filename = f"Hour_{hour:02d}.png"
    path = os.path.join(path_folder, filename)
    draw_clock(hour, False, False, path)

path_folder = "clock_one_hand_twisted_dataset/Minute"
os.makedirs(path_folder, exist_ok=True)
for minute in range(60):
    if minute == 0:
        minute = 60
    filename = f"Minute_{minute:02d}.png"
    path = os.path.join(path_folder, filename)
    draw_clock(False, minute, False, path)


path_folder = "clock_one_hand_twisted_dataset/Second"
os.makedirs(path_folder, exist_ok=True)
for second in range(60):
    if second == 0:
        second = 60
    filename = f"Second_{second:02d}.png"
    path = os.path.join(path_folder, filename)
    draw_clock(False, False, second, path)


print("✅ Clock image dataset generated successfully!")
