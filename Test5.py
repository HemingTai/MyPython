from tkinter import *
import tkinter.messagebox as messagebox

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidget()
    # 在GUI中，每个Button、Label、输入框等，都是一个Widget。Frame则是可以容纳其他Widget的Widget，所有的Widget组合起来就是一棵树。
    # pack()方法把Widget加入到父容器中，并实现布局。pack()是最简单的布局，grid()可以实现更复杂的布局。
    # 在createWidgets()方法中，我们创建一个Label和一个Button，当Button被点击时，触发self.quit()使程序退出
    def createWidget(self):
        self.helloLabel = Label(self, text = 'Hello, world')
        self.helloLabel.pack()
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertBtn = Button(self, text = 'greet', command = self.hello)
        self.alertBtn.pack()
        self.quitBtn = Button(self, text = 'Quit', command = self.quit)
        self.quitBtn.pack()

    def hello(self):
        name = self.nameInput.get() or 'badboy'
        # tkMessageBox.showinfo()可以弹出消息对话框
        messagebox.showinfo('Message', 'Hello, %s' % name)

app = Application()
# 设置窗口标题
app.master.title('Hello')
# 运行
app.mainloop()






