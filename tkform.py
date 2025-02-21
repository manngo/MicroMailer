'''
TKForm
'''

import tkinter
from tkinter import ttk
from tkinter.font import Font

from library import dbug

class TKForm(tkinter.Tk):
	'''Main Class'''
	def __init__(self, title='GTK Window'):
		super().__init__()
		self.title(title)
		# self.geometry('800x600')
		self.mainframe = ttk.Frame(self, padding='13 3 12 12')
		self.grid_columnconfigure(0, weight=1)
		self.mainframe.grid(column=0, row=0, sticky='NWES')

	def clear(self):
		for i in self.window.winfo_children():
			i.grid_forget()

	def addMenu(self, menu):
		menubar = tkinter.Menu(self)
		self['menu'] = menubar								#	Just in case for future reference
		application_menu = None

		for name, data in menu.items():
			if callable(data):
				if not application_menu:
					application_menu = tkinter.Menu(menubar)
					menubar.insert(0, 'cascade', menu=application_menu, label=self.title())
				application_menu.add_command(label=name, command=data)
			else:
				m = tkinter.Menu(menubar)					#	New menu
				menubar.add('cascade', menu=m, label=name)		#	Add hierarchical to menu bar aka add_cascade(…)
				for name, data in data.items():				#	Add labels & commands
					m.add_command(label=name, command=data)

	def add(self, widget, row, column, columnspan=1, rowspan=1, sticky='W', pad=(2,2)):
#		dbug(f'row: {row}, column: {column}')
		self.mainframe.grid_columnconfigure(row, weight=1)

		sticky = 'nsew'
		widget.grid(in_=self.mainframe, row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky, padx=pad[0], pady=pad[1])

	def show(self):
		self.mainloop()

class Label(ttk.Label):
	def __init__(self, parent, text, textvariable=None, **kwargs):
		self.parent = parent
		super().__init__(parent, text=text, textvariable=textvariable, **kwargs)

class BoldLabel(Label):
	def __init__(self, parent, text, textvariable=None, **kwargs):
		super().__init__(parent, text=text, textvariable=textvariable, **kwargs)
		self.configure(font=Font(weight='bold'))

class Textbox(ttk.Entry):
	def __init__(self, parent, textvariable=None, text=None, **kwargs):
		self.parent = parent
		super().__init__(parent, textvariable=textvariable)
		if text:
			self.insert(0, text)

class Textarea(tkinter.Text):
	def __init__(self, parent, height=None, width=None, text=None, **kwargs):
		self.parent = parent
		super().__init__(parent, height=height, width=width, **kwargs)
		if text:
			self.insert('0.0', text)

class Passwordbox(Textbox):
	def __init__(self, parent, textvariable=None, **kwargs):
		self.parent = parent
		super().__init__(parent, textvariable=textvariable, **kwargs)
		self.configure(show='•')

class Numberbox(Textbox):
	def check(self, value):
		try:
			value == '' or float(value)
			return True
		except:
			return False

	def __init__(self, parent, textvariable=None, text=None, **kwargs):
		super().__init__(parent, textvariable=textvariable, **kwargs)
		self.configure(validatecommand=(parent.register(self.check), '%P'), validate='key')
		if text:
			self.insert(0, text)

class Checkbox(ttk.Checkbutton):
	def __init__(self, parent, text, textvariable=None, onvalue=True, offvalue=False, **kwargs):
		super().__init__(parent, text=text, variable=textvariable, onvalue=onvalue, offvalue=offvalue, **kwargs)

class Button(ttk.Button):
	def __init__(self, parent, text, command, **kwargs):
		self.parent = parent
		super().__init__(parent, text=text, command=command, **kwargs)

class OKButton(Button):
	def __init__(self, parent, text, command, **kwargs):
		super().__init__(parent, text=text, command=command, **kwargs)
		self.configure(default='active')
		self.parent.bind('<Return>', command)
		self.parent.bind('<KP_Enter>', command)

class CancelButton(Button):
	def __init__(self, parent, text, command=None, **kwargs):
		if not command:
			command = lambda event=None: self.parent.destroy()

		super().__init__(parent, text=text, command=command, **kwargs)
		self.parent.bind('<Key-Escape>', command)
		self.parent.bind('<Command-.>', command)

class Combobox(ttk.Combobox):
	def __init__(self, parent, items, default=None, textvariable=None, **kwargs):
		self.parent = parent
		self.items = items
		self.textvariable = textvariable

		super().__init__(parent, **kwargs)

		self['values'] = [i[0] for i in items]
		default = self['values'].index(default) if default in self['values'] else 0
		default = min(max(0, int(default)), len(items) - 1)
		self.current(default)
		self.textvariable.set(items[self.current()][1])

		self.state(['readonly'])
		self.bind('<<ComboboxSelected>>', lambda : self.textvariable.set(self.items[self.current()][1]))

class MenuButton(ttk.OptionMenu):
	def __init__(self, parent, items, default=None, textvariable=None, **kwargs):
		self.parent = parent
		self.items = items
		self.textvariable = textvariable

		values = [i[0] for i in items]

		super().__init__(parent, textvariable, values[2], *values, command = lambda item=None: print(item), **kwargs)
#		self.configure(command = lambda : print(self.current()))
		self.bind('<<OptionMenuSelected>>', lambda item: self.textvariable.set(self.items[item][0]))


if __name__ == '__main__':
	gui = TKForm('Testing')

	def ok(*args):
		name = nameTextbox.get()

		print(f'ok: {name} aka {password.get()} wants a {thing.get()}')

	def cancel(*args):
		print('cancel')
		gui.destroy()

	password = tkinter.StringVar()
	thing = tkinter.StringVar()

	nameLabel = BoldLabel(gui, text='Name')
	nameTextbox = Textbox(gui, text='Fred')

	passwordLabel = Label(gui, text='Password')
	passwordTextbox = Passwordbox(gui, password)
	passwordPlain = Label(gui, '')
	passwordPlain.configure(textvariable=password)

	numberLabel = Label(gui, 'Number')
	numberTextbox = Numberbox(gui)

	okButton = OKButton(gui, text='OK', command=ok)
	cancelButton = CancelButton(gui, 'Cancel')

	#	Combobox
	thingLabel = Label(gui, '')
	thingLabel.configure(textvariable=thing)
	thingCombo = Combobox(gui, items=(
		('apple', 'a'),
		('banana', 'b'),
		('cherry', 'c'),
	), textvariable=thing, default='banana')

	gui.add(nameLabel, row=1, column=1)
	gui.add(nameTextbox, row=1, column=2)

	gui.add(passwordLabel, row=2, column=1)
	gui.add(passwordTextbox, row=2, column=2)
	gui.add(passwordPlain, row=3, column=2)

	gui.add(numberLabel, row=4, column=1)
	gui.add(numberTextbox, row=4, column=2)
	gui.add(okButton, row=5, column=3)
	gui.add(cancelButton, row=5, column=1)

	gui.add(thingLabel, row=6, column=3)
	gui.add(thingCombo, row=6, column=1, columnspan=2)


	menuThing = tkinter.StringVar()
	thingButton = MenuButton(
		gui, items={
			('apple', 'a'),
			('banana', 'b'),
			('cherry', 'c'),
		}, textvariable=menuThing)
	thingButtonLabel = Label(gui, '')
	thingButtonLabel.configure(textvariable=menuThing)
	gui.add(thingButton, row=7, column=1, columnspan=2)
	gui.add(thingButtonLabel, row=7, column=3, columnspan=2)


	#	Application Menu
	menuitems = {
		'File': {
			'Open': lambda: print('Open'),
			'Close': lambda: print('Close'),
		},
		'About': lambda: print('About …'),
		'Edit': {
			'Copy': lambda: print('Copy'),
			'Paste': lambda: print('Paste'),
			'Edit Again': {
				'Copy More': lambda: print('Copy More'),
				'Paste Some': lambda: print('Paste Some'),
			},
		},
	}

	gui.addMenu(menuitems)

	gui.show()

