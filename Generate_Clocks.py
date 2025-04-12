import matplotlib.pyplot as plt
import numpy as np
import os


def draw_clock(hours, minutes, seconds, save_path):
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

    # Calculate angles for the clock hands
    hour_angle = np.pi / 6 * (3 - (hours % 12) - minutes / 60 - seconds / 3600)
    minute_angle = np.pi / 30 * (15 - minutes - seconds / 60)
    second_angle = np.pi / 30 * (15 - seconds)

    # Draw clock hands
    ax.plot([0, 0.5 * np.cos(hour_angle)], [0, 0.5 * np.sin(hour_angle)], lw=6, color="black")   # hour hand
    ax.plot([0, 0.75 * np.cos(minute_angle)], [0, 0.75 * np.sin(minute_angle)], lw=4, color="black")  # minute hand
    ax.plot([0, 0.85 * np.cos(second_angle)], [0, 0.85 * np.sin(second_angle)], lw=2, color="red")    # second hand

    # Decorative center dot
    ax.add_patch(plt.Circle((0, 0), radius=0.02, fc="black"))

    # Hide axes
    plt.axis("off")
    plt.xlim(-1.05, 1.05)
    plt.ylim(-1.05, 1.05)

    # Save the image
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)


# Create dataset folder
os.makedirs("clock_dataset", exist_ok=True)

# Generate images from 12_00_00.png to 11_59_59.png (12-hour format)
for hour_24 in range(12):
    hour_12 = hour_24 % 12
    hour_12 = 12 if hour_12 == 0 else hour_12  # convert 0 hour to 12
    for minute in range(60):
        for second in range(60):
            filename = f"{hour_12:02d}_{minute:02d}_{second:02d}.png"
            path = os.path.join("clock_dataset", filename)
            draw_clock(hour_24, minute, second, path)

print("✅ Clock image dataset generated successfully!")
