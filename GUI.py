import tkinter as tk
from Client import Client


class ClientGUI:
    def __init__(self
                 , parent, ip, port, userName):
        self.root = parent
        self.root.title('Messanger')
        self.text = tk.Text(self.root, state='disabled', width=50, height=30)
        self.btn = tk.Button(self.root, text='Send', command=self.btnOk, width='10')
        self.txtBox = tk.Entry(self.root, width='50')
        self.text.pack(side='top')
        self.txtBox.pack(side='left')
        self.btn.pack(side='right')

        self.client = Client(ip, port, userName)

        self.root.after(1000, self.receive())

    def btnOk(self):
        self.receive()
        msg = self.txtBox.get()
        self.client.send(msg)
        self.textInsert(('Me', msg))
        self.txtBox.delete('0', 'end')

    def receive(self):
        msg = self.client.receive()
        if msg:
            self.textInsert(msg)
        self.root.after(1000, self.receive())
        
    def textInsert(self, text):
        self.text.config(state='normal')
        self.text.insert('end', text[0] + ' >> ' + text[1] + '\n')
        self.text.config(state='disabled')


if __name__=='__main__':
    root = tk.Tk()
    gui = ClientGUI(root, '127.0.0.1', 4444, 'qwe')
    root.mainloop()
