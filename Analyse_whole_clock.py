import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

filenames = ['twisted_hands.xlsx']
filenames = ['whole_clock_previous.xlsx']


def time_to_seconds(time_obj):
    if not isinstance(time_obj, str):
        time_str = time_obj.strftime('%H:%M:%S') if len(str(time_obj).split(':')) == 3 else time_obj.strftime('%H:%M:%S')[
                                                                                        :-3]
    else:
        time_str = time_obj
    if len(time_str.split(":")) == 3:
        hours, minutes, seconds = map(int, time_str.split(':'))
    else:
        hours, minutes = map(int, time_str.split(':'))
        seconds = 0

    return hours * 3600 + minutes * 60 + seconds


for filename in filenames:
    df = pd.read_excel(filename)

    number = df['answer'].apply(time_to_seconds)
    extracted_answer = df['extracted_answer'].apply(time_to_seconds)

    # max error is 6 hour, if the difference is more than 6 hours, then substract it
    time_difference = 6 * 3600
    diff = extracted_answer - number
    abs_diff = abs(extracted_answer - number)
    extracted_answer[(abs_diff > time_difference) & (diff > 0)] = 2*time_difference-extracted_answer[(abs_diff > time_difference) & (diff > 0)]
    extracted_answer[(abs_diff > time_difference) & (diff <= 0)] = 2*time_difference+extracted_answer[(abs_diff > time_difference) & (diff <= 0)]

    # 计算MAE
    mae = mean_absolute_error(number, extracted_answer)
    print(f'MAE: {mae}')
    c = number - extracted_answer
    # 绘制散点图
    plt.figure(figsize=(6, 6))
    # plt.scatter(number, number-extracted_answer, color='blue', label='GPT-4o')
    plt.scatter(number, extracted_answer, color='blue', label='GPT-4o', s=10)

    # 添加斜率为1的参考线
    plt.plot([0, 48000], [0, 48000], color='red', linestyle='--', label='Perfect Match (y=x)')
    # plt.plot([0, 59], [0, 0], color='red', linestyle='--')

    # 设置图表标题和轴标签
    # plt.title(f'Scatter plot for {filename.replace(".xlsx","")}')
    plt.xlabel('Ground Truth')
    # plt.ylabel('Error')
    plt.ylabel('Prediction')

    # # 设置x轴范围
    # plt.xlim(0, 59)
    # plt.ylim(0, 59)

    # 显示图例
    plt.legend()

    # # 显示图形
    # plt.show()
    plt.savefig(filename.replace(".xlsx",".png"), bbox_inches='tight', pad_inches=0.1)