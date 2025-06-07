import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os

def run_script(times, input_value):
    try:
        # 使用 os.system 执行 gg.py
        result = os.system(f'python gg.py {times} {input_value}')
        if result == 0:
            messagebox.showinfo("结果", "脚本执行成功。")
        else:
            messagebox.showerror("错误", "脚本执行失败。")
    except Exception as e:
        messagebox.showerror("错误", str(e))

def start_script():
    times = times_entry.get()
    input_value = input_entry.get()

    try:
        times = int(times)
    except ValueError:
        messagebox.showerror("输入错误", "次数必须是一个整数。")
        return

    if not input_value:
        messagebox.showerror("输入错误", "输入不能为空。")
        return

    # 创建并启动线程
    threading.Thread(target=run_script, args=(times, input_value)).start()

def browse_file():
    filename = filedialog.askopenfilename(title="选择文件")
    if filename:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, filename)

# 创建主窗口
root = tk.Tk()
root.title("执行 gg.py")

# 创建和放置标签、输入框和按钮
times_label = tk.Label(root, text="次数:")
times_label.grid(row=0, column=0, padx=10, pady=10)

times_entry = tk.Entry(root)
times_entry.grid(row=0, column=1, padx=10, pady=10)

input_label = tk.Label(root, text="输入（字符串或文件路径）:")
input_label.grid(row=1, column=0, padx=10, pady=10)

input_entry = tk.Entry(root, width=50)
input_entry.grid(row=1, column=1, padx=10, pady=10)

browse_button = tk.Button(root, text="浏览文件", command=browse_file)
browse_button.grid(row=1, column=2, padx=10, pady=10)

start_button = tk.Button(root, text="开始", command=start_script)
start_button.grid(row=2, columnspan=3, pady=20)

# 运行 GUI 主循环
root.mainloop()
