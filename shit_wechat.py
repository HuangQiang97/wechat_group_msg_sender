import logging
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from wxpy import Bot

logging.basicConfig(level=logging.INFO, filename='wechat_group.log', filemode='a',
                    format='%(asctime)s  -> %(levelname)s: %(message)s')
logging.info('启动')


def gui():
    global check_buttons, send_time, msg_input,  groups, log_msg,  list_items
    window = tk.Tk()
    window.title('shit_wechat')
    window.geometry('600x650')

    label = tk.Label(window, text='要发送的消息：', font=('Arial', 12), width=12)
    label.place(x=10, y=10)
    msg_input = tk.Entry(window, show=None, font=('Arial', 14))
    msg_input.place(x=150, y=10)

    label = tk.Label(window, text='要发送的群：', font=('Arial', 12), width=12)
    label.place(x=10, y=50)
    check_buttons = [tk.IntVar() for _ in range(len(groups))]
    for i in range(len(groups)):
        group = groups[i].name
        c = tk.Checkbutton(window, text=group,
                           variable=check_buttons[i], onvalue=1, offvalue=0)
        c.place(x=145 + 100 * (i % 4), y=40 * (i // 4) + 50)

    label = tk.Label(window, text='发送时间：', font=('Arial', 12), width=12)
    label.place(x=10, y=300)
    hour = tk.StringVar()
    hour.set(['小时'] + [x for x in range(24)])
    list_items = tk.Listbox(window, listvariable=hour, height=6)
    list_items.place(x=145, y=300)

    log_msg = tk.StringVar()
    log_msg.set('logging msg')
    label = tk.Label(window, textvariable=log_msg,
                     font=('Arial', 10), width=50, bg='gray')
    label.place(x=150, y=450)

    button = tk.Button(window, text='Go', font=('Arial', 12),
                       width=10, height=1, command=click)
    button.place(x=250, y=500)

    window.mainloop()


def click():
    global send_init_flag, msg, check_buttons, send_time, msg_input, group_name, groups, list_items
    msg = msg_input.get()
    for i in range(len(check_buttons)):
        if check_buttons[i].get() == 1:
            group_name.append(groups[i].name)
    send_time = list_items.get(list_items.curselection())
    logging.info('msg:' + msg)
    logging.info('group_names:' + ','.join(group_name))
    logging.info('send_time:' + str(send_time))
    send_init_flag = True


group_name = []
msg = None
send_time = None

groups = []
log_msg = None
send_init_flag = False

msg_input = None
check_buttons = None
list_items = None
my_group = None

try:
    bot = Bot(cache_path=True)
    bot.groups(update=True, contact_only=False)
    groups = bot.groups()
    1/len(groups)
except:
    tk.messagebox.showerror(
        'Error', '登陆失败！请尝试登录网页版微信： https://wx.qq.com ，若网页版无法登录，则此脚本无法正常运行！')
    exit(-1)


gui_thread = threading.Thread(target=gui, name='gui_thread')
gui_thread.setDaemon(True)
gui_thread.start()

while not send_init_flag:
    pass
while True:
    h = datetime.now().hour
    logging.info('确认时间')
    now = datetime.now()
    now = str(now.hour) + ':' + str(now.minute) + '--->'
    if h == send_time:
        for i in range(len(group_name)):
            single_group = group_name[i]
            my_group = bot.groups().search(single_group)[0]
            logging.info('开始发送到：' + single_group)
            log_msg.set(now + '开始发送到：' + single_group)
            my_group.send_msg(msg)
        logging.info('发送完毕，24小时后再次确认时间自动发送')
        log_msg.set(now + '发送完毕，24小时后再次确认时间自动发送')
        time.sleep(60 * 60 * 24)
    else:
        logging.info('未到发送时间，一小时后再次自动确认时间')
        log_msg.set(now + '未到发送时间，一小时后再次自动确认时间')
        time.sleep(60 * 60)

