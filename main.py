from tkinter import messagebox
import tkinter as tk
import random
import sqlite3

conn = sqlite3.connect('scores.db')


class App:
    def __init__(self, c):
        self.root = tk.Tk()
        self.root.title("Menu")
        self.name = ''

        self.go = False
        self.counter = 0

        self.c = c
        # Database
        self.cursor = self.c.cursor()

        # High score list - reaction
        self.high_scores_r = list()
        # number mem
        self.high_scores_n = list()
        # number mem
        self.high_scores_w = list()
        # number mem
        self.high_scores_v = list()

        # Main menu
        self.reaction = React(self)
        self.num_mem = MemoryN(self)
        self.word_mem = MemoryW(self)
        self.vis_mem = MemoryV(self)

        self.react_but = tk.Button(text="Reaction Game", command=lambda: self.change('r'),
                                   font=("Helvetica", 25), width=20)
        self.n_mem_but = tk.Button(text="Number Memory Game", command=lambda: self.change('n'),
                                   font=("Helvetica", 25), width=20)
        self.w_mem_but = tk.Button(text="Word Memory Game", command=lambda: self.change('w'),
                                   font=("Helvetica", 25), width=20)
        self.v_mem_but = tk.Button(text="Visual Memory Game", command=lambda: self.change('v'),
                                   font=("Helvetica", 25), width=20)

        self.title_l = tk.Label(font=("Helvetica", 25), width=18)

        self.high_scores_d = dict()
        for i in range(1, 4):
            self.high_scores_d[i] = tk.Label(font=("Helvetica", 22))

        # Name area
        self.name_lab = tk.Label(text="Username:", font=("Helvetica", 12))
        self.name_ent = tk.Entry(font=("Helvetica", 12), width=16)
        self.name_but = tk.Button(text="Continue", command=self.login,
                                  font=("Helvetica", 12), width=15)

        self.name_lab.grid(column=0, row=0)
        self.name_ent.grid(column=0, row=1)
        self.name_but.grid(column=0, row=2)

        self.root.mainloop()

    def get_db(self):
        # High score list - reaction
        self.cursor = self.c.cursor()
        self.cursor.execute("SELECT name, reaction FROM scores")
        self.high_scores_r = [x for x in self.cursor]
        self.high_scores_r.sort(key=lambda pers: pers[1])
        self.high_scores_r += [['', '']] * (3-len(self.high_scores_r))
        # number mem
        self.cursor = self.c.cursor()
        self.cursor.execute("SELECT name, digits FROM scores")
        self.high_scores_n = [x for x in self.cursor]
        self.high_scores_n.sort(reverse=True, key=lambda pers: pers[1])
        for i in range(3):
            if self.high_scores_n[0][1] == "N/A":
                self.high_scores_n.append(self.high_scores_n[0])
                del self.high_scores_n[0]
        self.high_scores_n += [['', '']] * (3-len(self.high_scores_n))
        # words mem
        self.cursor = self.c.cursor()
        self.cursor.execute("SELECT name, words FROM scores")
        self.high_scores_w = [x for x in self.cursor]
        self.high_scores_w.sort(reverse=True, key=lambda pers: pers[1])
        for i in range(3):
            if self.high_scores_w[0][1] == "N/A":
                self.high_scores_w.append(self.high_scores_w[0])
                del self.high_scores_w[0]
        self.high_scores_w += [['', '']] * (3-len(self.high_scores_w))
        # vis mem
        self.cursor = self.c.cursor()
        self.cursor.execute("SELECT name, tiles FROM scores")
        self.high_scores_v = [x for x in self.cursor]
        self.high_scores_v.sort(reverse=True, key=lambda pers: pers[1])
        for i in range(3):
            if self.high_scores_v[0][1] == "N/A":
                self.high_scores_v.append(self.high_scores_v[0])
                del self.high_scores_v[0]
        self.high_scores_v += [['', '']] * (3-len(self.high_scores_v))

    def login(self):
        self.name = self.name_ent.get()
        if self.name:
            self.cursor.execute("SELECT name FROM scores")
            names = [x[0] for x in self.cursor]
            if self.name not in names:
                self.cursor.execute("INSERT INTO scores VALUES (?, 'N/A', 'N/A', 'N/A', 'N/A')", (self.name,))
                self.c.commit()
            self.name_lab.grid_forget()
            self.name_ent.grid_forget()
            self.name_but.grid_forget()
            self.draw()

    def draw(self):
        self.root.title("Menu")

        self.get_db()

        self.react_but.grid(column=0, row=0)
        self.n_mem_but.grid(column=0, row=1)
        self.w_mem_but.grid(column=0, row=2)
        self.v_mem_but.grid(column=0, row=3)

        self.title_l.grid(column=1, row=0)
        for i in sorted(self.high_scores_d):
            self.high_scores_d[i].grid(column=1, row=i)

        if not self.go:
            self.go = True
            self.update()

    def change(self, to):
        self.go = False

        self.react_but.grid_forget()
        self.n_mem_but.grid_forget()
        self.w_mem_but.grid_forget()
        self.v_mem_but.grid_forget()

        self.title_l.grid_forget()
        for i in sorted(self.high_scores_d):
            self.high_scores_d[i].grid_forget()

        if to == 'r':
            self.reaction.draw()
            
        elif to == 'n':
            self.num_mem.draw()

        elif to == 'w':
            self.word_mem.draw()

        elif to == 'v':
            self.vis_mem.draw()

    def update(self):
        if self.go:
            if 0 <= self.counter < 30:
                self.title_l.configure(text="Reaction Highscores")
                for i, r in zip(sorted(self.high_scores_d), self.high_scores_r):
                    col = "black"
                    if r[0] == self.name:
                        col = "green"
                    txt = ""
                    if r[0]:
                        txt = "{}. {}: N/A".format(i, *r)
                    if r[1] and r[1] != "N/A":
                        txt = "{}. {}: {}ms".format(i, *r)
                    self.high_scores_d[i].configure(text=txt, fg=col)
            elif 30 <= self.counter < 60:
                self.title_l.configure(text="Number Highscores")
                for i, r in zip(sorted(self.high_scores_d), self.high_scores_n):
                    col = "black"
                    if r[0] == self.name:
                        col = "green"
                    txt = ""
                    if r[0]:
                        txt = "{}. {}: N/A".format(i, *r)
                    if r[1] and r[1] != "N/A":
                        txt = "{}. {}: {} digits".format(i, *r)
                    self.high_scores_d[i].configure(text=txt, fg=col)
            elif 60 <= self.counter < 90:
                self.title_l.configure(text="Word Highscores")
                for i, r in zip(sorted(self.high_scores_d), self.high_scores_w):
                    col = "black"
                    if r[0] == self.name:
                        col = "green"
                    txt = ""
                    if r[0]:
                        txt = "{}. {}: N/A".format(i, *r)
                    if r[1] and r[1] != "N/A":
                        txt = "{}. {}: {} words".format(i, *r)
                    self.high_scores_d[i].configure(text=txt, fg=col)
            elif 90 <= self.counter < 120:
                self.title_l.configure(text="Visual Highscores")
                for i, r in zip(sorted(self.high_scores_d), self.high_scores_v):
                    col = "black"
                    if r[0] == self.name:
                        col = "green"
                    txt = ""
                    if r[0]:
                        txt = "{}. {}: N/A".format(i, *r)
                    if r[1] and r[1] != "N/A":
                        txt = "{}. {}: {} levels".format(i, *r)
                    self.high_scores_d[i].configure(text=txt, fg=col)
            self.counter += 1
            if self.counter == 120:
                self.counter = 0
            self.root.after(100, self.update)


class MemoryN:
    def __init__(self, app):
        self.app = app

        self.state = 0
        self.go = False
        self.digits = 0
        self.timer = 0
        self.current_num = 0
        
        self.back_but = tk.Button(text="←", font=("Helvetica", 20), borderwidth=0, command=self.back)
        self.title_lab = tk.Label(text="Number Game", font=("Helvetica", 25))
        self.num_lab = tk.Label(font=("Helvetica", 25))
        
        self.text = tk.Text(width=10, height=1, font=("Helvetica", 25))
        self.submit = tk.Button(text="Check", font=("Helvetica", 22),  command=self.click, width=10)
        
        self.bar = tk.Label(bg="light sky blue")
        
    def draw(self):
        self.app.root.title("Number Memory")
        self.go = True
        
        self.digits = 1
        self.timer = 3

        self.state = 0
        
        self.current_num = random.randint(10 ** (self.digits-1) - 1, (10 ** self.digits) - 1)

        self.num_lab.configure(text=self.current_num)
        self.bar.configure(width=self.timer*2)
        
        self.back_but.grid(row=1, column=0, sticky="W")
        self.title_lab.grid(row=1, column=1)
        self.num_lab.grid(row=2, column=0, columnspan=4)
        self.bar.grid(row=3, column=0, columnspan=4)

        self.update()        

    def undraw(self):
        self.go = False
        
        self.back_but.grid_forget()
        self.title_lab.grid_forget()
        self.num_lab.grid_forget()
        self.text.grid_forget()
        self.bar.grid_forget()
        self.submit.grid_forget()

    def back(self):
        self.undraw()
        self.app.draw()

    def update(self):
        if self.go:
            if self.state == 0 and self.timer > 0:
                self.timer -= 1
                self.bar.configure(width=self.timer*2+1)
            elif self.timer == 0 and self.state == 0:
                self.bar.configure(bg=self.app.root.cget("bg"))
                self.state = 1
            elif self.state == 1:
                self.text.configure(state='normal', fg="black")
                self.text.delete("1.0", "end")
                self.num_lab.grid_forget()
                self.bar.grid_forget()
                self.text.grid(row=2, column=0, columnspan=4)
                self.submit.grid(row=3, column=0, columnspan=4)
                self.submit.configure(state='normal')

                self.state = 2
            self.app.root.after(1000, self.update)
        
    def click(self):
        guess = self.text.get("1.0", "end").strip('\n')
        if guess == str(self.current_num):
            self.text.configure(fg="green", state='disabled')
            self.submit.configure(disabledforeground="green", state='disabled')
            self.digits += 1
            self.app.root.after(1000, self.new)
        else:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", self.current_num)
            self.text.configure(fg="red", state='disabled')
            self.submit.configure(disabledforeground="red", state='disabled')
            self.app.get_db()

            highscore = str(self.app.high_scores_n[0][1])
            if highscore.isdigit():
                if self.digits - 1 > int(highscore):
                    messagebox.showinfo("Woah!", "You just got the new highscore!")
            else:
                messagebox.showinfo("Woah!", "You just got the new highscore!")
            self.app.cursor.execute("UPDATE scores SET digits=? WHERE name=?", (str(self.digits - 1), self.app.name))
            self.app.c.commit()

            self.digits = 1

            self.app.root.after(2000, self.new)

    def new(self):
        if self.go:
            self.current_num = random.randint(10 ** (self.digits-1), (10 ** self.digits) - 1)
            self.timer = round(self.digits * 1.6)
            self.state = 0

            self.text.grid_forget()
            self.submit.grid_forget()

            self.num_lab.configure(text=self.current_num)
            self.bar.configure(width=self.timer*2)

            self.num_lab.grid(row=2, column=0, columnspan=4)
            self.bar.grid(row=3, column=0, columnspan=4)
            self.bar.configure(bg="light sky blue")


class React:
    def __init__(self, app):
        self.app = app

        self.go = False
        self.cooldown = 0
        self.timer = 0
        self.state = 0

        self.back_but = tk.Button(text="←", font=("Helvetica", 20), borderwidth=0, command=self.back) 
        self.title_lab = tk.Label(text="Reaction Game", font=("Helvetica", 25))
        self.big_but = tk.Button(text="Wait...", bg="indian red", command=self.click, font=("Helvetica", 25),
                                 width=20, height=8)
        
    def draw(self):
        self.app.root.title("Reaction")

        self.go = True
        self.cooldown = random.randint(3000, 6000)
        self.timer = 0
        self.state = 0
        
        self.big_but.configure(text="Wait...", bg="indian red")
        
        self.back_but.grid(row=1, column=0, sticky="W")
        self.title_lab.grid(row=1, column=1)
        self.big_but.grid(row=2, column=0, columnspan=4)
        
        self.update()

    def undraw(self):
        self.go = False
        self.back_but.grid_forget()
        self.title_lab.grid_forget()
        self.big_but.grid_forget()

    def back(self):
        self.undraw()
        self.app.draw()
        
    def update(self):
        if self.go:
            if self.state == 0 and self.cooldown > 0:
                self.cooldown -= 1
                    
            elif self.cooldown == 0:
                self.cooldown = random.randint(3000, 6000)
                self.state = 1
                
            if self.state == 1:
                self.big_but.configure(text="CLICK", bg="green yellow")
                self.timer += 1
                
            self.app.root.after(1, self.update)

    def click(self):
        if self.state == 1:
            self.state = 3
            self.big_but.configure(text="{}ms".format(self.timer), bg="white")

            self.app.get_db()
            highscore = str(self.app.high_scores_r[0][1])
            if highscore.isdigit():
                if self.timer < int(highscore):
                    messagebox.showinfo("Woah!", "You just got the new highscore!")
            else:
                messagebox.showinfo("Woah!", "You just got the new highscore!")
            self.app.cursor.execute("UPDATE scores SET reaction=? WHERE name=?", (str(self.timer), self.app.name))
            self.app.c.commit()

            self.timer = 0

        elif self.cooldown > 0 and self.state == 0:
            self.timer = 0
            self.big_but.configure(text="Too soon!", bg="light sky blue")
            self.state = 2
            
        elif self.cooldown > 0 and self.state == 2:
            self.timer = 0
            self.cooldown = random.randint(3000, 6000)
            self.big_but.configure(text="Wait...", bg="indian red")
            self.state = 0
            
        elif self.state == 3:
            self.timer = 0
            self.cooldown = random.randint(3000, 6000)
            self.big_but.configure(text="Wait...", bg="indian red")
            self.state = 0


class MemoryW:
    def __init__(self, app):
        self.app = app

        with open("FREQ.TXT", 'r') as f:
            self.all_words = [x.strip('\n') for x in f.readlines()]

        self.max = 10
        self.word = ''

        self.seen_l = []
        self.condensed = []

        self.back_but = tk.Button(text="←", font=("Helvetica", 20), borderwidth=0, command=self.back)
        self.title_lab = tk.Label(text="Word Game", font=("Helvetica", 25))

        self.go_but = tk.Button(text="Go?", bg="seagreen1", font=("Helvetica", 20), command=self.go, width=20)

        self.word_lab = tk.Label(text="", font=("Helvetica", 20), width=10)

        self.new_but = tk.Button(text="New", font=("Helvetica", 22),  command=self.new, width=5)
        self.seen_but = tk.Button(text="Seen", font=("Helvetica", 22),  command=self.seen, width=5)

    def go(self):
        self.go_but.grid_forget()
        self.word_lab.grid(row=2, column=1, columnspan=2)
        self.new_but.grid(row=2, column=0)
        self.seen_but.grid(row=2, column=3)

        random.shuffle(self.all_words)
        self.condensed = self.all_words[:self.max]
        self.max = 20
        self.word = ''
        self.seen_l = []

        self.pick_new()

    def new(self):
        if self.word not in self.seen_l:
            self.seen_l.append(self.word)
            self.new_but.configure(disabledforeground='green', state='disabled')
            self.seen_but.configure(disabledforeground='red', state='disabled')
            self.app.root.after(1000, self.pick_new)
        else:
            self.new_but.configure(disabledforeground='red', state='disabled')
            self.seen_but.configure(disabledforeground='green', state='disabled')
            self.app.root.after(1500, self.do_checks)

    def seen(self):
        if self.word in self.seen_l:
            self.new_but.configure(disabledforeground='red', state='disabled')
            self.seen_but.configure(disabledforeground='green', state='disabled')
            self.app.root.after(1000, self.pick_new)
        else:
            self.new_but.configure(disabledforeground='green', state='disabled')
            self.seen_but.configure(disabledforeground='red', state='disabled')
            self.app.root.after(1500, self.do_checks)

    def do_checks(self):
        self.app.get_db()

        highscore = str(self.app.high_scores_w[0][1])
        if highscore.isdigit():
            if len(self.seen_l) > int(highscore):
                messagebox.showinfo("Woah!", "You just got the new highscore!")
        else:
            messagebox.showinfo("Woah!", "You just got the new highscore!")
        self.app.cursor.execute("UPDATE scores SET words=? WHERE name=?", (str(len(self.seen_l)), self.app.name))
        self.app.c.commit()

        self.app.root.after(400, self.undraw())
        self.app.root.after(401, self.draw())

    def pick_new(self):
        if len(self.seen_l) >= (len(self.condensed) / 3) * 2:
            self.max += 7
            self.condensed = self.all_words[:self.max]
        self.word = random.choice(self.condensed)
        self.word_lab.configure(text=self.word)
        self.new_but.configure(state='normal')
        self.seen_but.configure(state='normal')

    def draw(self):
        self.app.root.title("Number Memory")

        self.max = 20
        self.word = ''
        self.seen_l = []

        self.go_but.grid(row=1, column=1)

        self.back_but.grid(row=1, column=0, sticky="W")
        self.title_lab.grid(row=1, column=1)
        self.go_but.grid(row=2, column=0, columnspan=4)

    def undraw(self):
        self.go_but.grid_forget()
        self.back_but.grid_forget()

        self.title_lab.grid_forget()
        self.word_lab.grid_forget()
        self.new_but.grid_forget()
        self.seen_but.grid_forget()

    def back(self):
        self.undraw()
        self.app.draw()


class MemoryV:
    def __init__(self, app):
        self.app = app

        self.grid = dict()
        self.lit = []
        self.picked = []

        self.level = 1

        self.back_but = tk.Button(text="←", font=("Helvetica", 20), borderwidth=0, command=self.back)
        self.title_lab = tk.Label(text="Visual Game", font=("Helvetica", 25))

        self.go_but = tk.Button(text="Go?", bg="seagreen1", font=("Helvetica", 20), command=self.go, width=20)
        self.frame = tk.Frame(bg="deepskyblue2")

    def draw(self):
        self.app.root.title("Visual Memory")

        self.go_but.grid(row=1, column=1)

        self.back_but.grid(row=1, column=0, sticky="W")
        self.title_lab.grid(row=1, column=1)
        self.go_but.grid(row=2, column=0, columnspan=4)

    def undraw(self):
        self.go_but.grid_forget()
        self.back_but.grid_forget()
        self.frame.grid_forget()
        for i in self.grid.copy():
            for b in self.grid[i].buttons.values():
                b.destroy()
            del self.grid[i]
        self.title_lab.grid_forget()

    def go(self):
        self.go_but.grid_forget()
        self.level = 1

        self.grid = dict()

        self.frame.grid(column=0, row=2, columnspan=20)
        for i in range(1, self.level+5):
            self.grid[i] = Row(self.frame, self.app, i, self.level + 4)
            self.grid[i].draw()
        self.pick_squares()

    def pick_squares(self):
        self.lit = []
        self.picked = []
        for r in self.grid.values():
            for b in r.buttons.values():
                b.configure(state='disabled', bg="blue2")
        n = random.randint(self.level+3, self.level+4)
        i = 1
        while i <= n:
            x = random.randint(1, self.level+4)
            y = random.randint(1, self.level+4)
            if [x, y] not in self.lit:
                self.lit.append([x, y])
                self.grid[y].buttons[x].configure(bg="turquoise2")
                i += 1
        self.app.root.after(1000+(self.level*1500), self.clear_squares)

    def clear_squares(self):
        for r in self.grid.values():
            for b in r.buttons.values():
                b.configure(bg="royal blue1", state='normal')

    def check(self):
        if sorted(self.lit) == sorted(self.picked):
            self.level += 1
            for r in self.grid.values():
                r.add()
            self.grid[len(self.grid)+1] = Row(self.frame, self.app, len(self.grid)+1, self.level + 4)
            self.grid[len(self.grid)].draw()

            for r in self.grid.values():
                for b in r.buttons.values():
                    b.configure(state='disabled')

            self.app.root.after(1000, self.pick_squares())

    def back(self):
        self.do_checks()
        self.undraw()
        self.app.draw()

    def do_checks(self):
        self.app.get_db()

        highscore = str(self.app.high_scores_v[0][1])
        if highscore.isdigit():
            if self.level-1 > int(highscore):
                messagebox.showinfo("Woah!", "You just got the new highscore!")
        else:
            messagebox.showinfo("Woah!", "You just got the new highscore!")
        self.app.cursor.execute("UPDATE scores SET tiles=? WHERE name=?", (str(self.level-1), self.app.name))
        self.app.c.commit()

        self.app.root.after(400, self.undraw())
        self.app.root.after(401, self.draw())


class Row:
    def __init__(self, root, app, row, width):
        self.root = root
        self.app = app
        self.row = row
        self.width = width

        self.buttons = dict()
        for i in range(1, width+1):
            self.buttons[i] = tk.Button(self.root, width=4, height=2, bg="blue2",
                                        state='disabled', command=lambda x=i: self.click(x))

    def draw(self):
        for i in self.buttons:
            self.buttons[i].grid(row=self.row, column=i)

    def add(self):
        l = len(self.buttons)
        self.buttons[l+1] = tk.Button(self.root, width=4, height=2, bg="blue2", state='disabled',
                                                      command=lambda: self.click(l+1))
        self.buttons[l+1].grid(row=self.row, column=l+1)

    def click(self, col):
        if [col, self.row] in self.app.vis_mem.lit:
            self.buttons[col].configure(bg="turquoise2", state='disabled')
            self.app.vis_mem.picked.append([col, self.row])
            self.app.vis_mem.check()
        else:
            self.buttons[col].configure(bg="violet red")
            for r in self.app.vis_mem.grid:
                for b in self.app.vis_mem.grid[r].buttons:
                    self.app.vis_mem.grid[r].buttons[b].configure(state='disabled')
                    if [b, r] in self.app.vis_mem.lit:
                        self.app.vis_mem.grid[r].buttons[b].configure(bg='turquoise2')
            self.app.root.after(1500, self.app.vis_mem.do_checks)

game = App(conn)
