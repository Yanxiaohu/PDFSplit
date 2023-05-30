import os
import PyPDF2
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox

root = Tk()
root.title('PDF分解')


class CounterApp:
    def __init__(self, master):
        self.master = master
        self.count = 1
        self.add_button = tk.Button(master, text="增加", command=self.increment)
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.sub_button = tk.Button(master, text="减少", command=self.decrement)
        self.sub_button.pack(side=tk.LEFT)
        self.label1 = tk.Label(master, text="每{}页，分解为一个PDF文件".format(self.count))
        self.label1.pack(side=tk.LEFT, padx=10)

    def increment(self):
        self.count += 1
        self.label1.config(text="每{}页，分解为一个PDF文件".format(self.count))

    def decrement(self):
        self.count -= 1
        if self.count <= 1:
            self.count = 1
        self.label1.config(text="每{}页，分解为一个PDF文件".format(self.count))

    def getCount(self):
        return self.count


app = CounterApp(root)


def errorMessage():
    tkinter.messagebox.showerror(title='', message='分页数不准确，请调整后上传！')


def successMessage():
    result = tkinter.messagebox.askquestion(title='', message='文件解析成功,是否前往打开？', )
    if result == 'yes':
        path = os.path.realpath(os.getcwd() + '/PDF分页存放/')
        os.startfile(path)


def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])
    # 打开 PDF 文件
    input_pdf = open(file_path, 'rb')
    count = app.getCount()
    # 使用 PyPDF2 库创建 PdfFileReader 对象
    pdf_reader = PyPDF2.PdfReader(input_pdf)

    # 获取 PDF 的总页数
    page_count = len(pdf_reader.pages)
    all_count = len(pdf_reader.pages)
    if count >= all_count:
        errorMessage()
        return
        # 创建输出目录
    if not os.path.exists('PDF分页存放'):
        os.makedirs('PDF分页存放')

    # 从完整路径中提取文件名
    file_name_with_extension = os.path.basename(file_path)
    # 分离文件名和扩展名
    file_name, extension = os.path.splitext(file_name_with_extension)
    # 分页并保存到本地
    while page_count > 0:
        # 创建新的 PDF 文档
        output_pdf = PyPDF2.PdfWriter()
        if count == 1:
            page_count -= 1
            # 添加当前页面到新的 PDF 文档中
            output_pdf.add_page(pdf_reader.pages[page_count])
            # 保存新的 PDF 文档到文件中
            output_file_name = f"PDF分页存放/{file_name}-{page_count + 1}.pdf"
            with open(output_file_name, 'wb') as output_pdf_file:
                output_pdf.write(output_pdf_file)
        else:
            cache_count = count
            while cache_count > 0:
                cache_count -= 1
                page_count -= 1
                if page_count >= 0:
                    output_pdf.add_page(pdf_reader.pages[all_count - page_count - 1])
                page_number = all_count - page_count
                if (all_count - page_count) % count == 0:
                    page_number = page_number / count
                else:
                    page_number = page_number / 2 + 1
                output_file_name = f"PDF分页存放/{file_name}-{int(page_number)}.pdf"
            with open(output_file_name, 'wb') as output_pdf_file:
                output_pdf.write(output_pdf_file)
    successMessage()
    # 关闭输入 PDF 文件
    input_pdf.close()


upload_button = Button(root, text="上传并分解", font=("宋体", 20), command=choose_file)
upload_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.mainloop()  # 进入事件循环
