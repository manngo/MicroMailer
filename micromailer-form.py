import tkinter.filedialog

from library import *
import tkform
import micromailer

defaults = readIni(resource_path('micromailer.ini'))['micromailer']
prefs = Prefs(['.micro-mailer', 'prefs.json'])

#	Form
form = tkform.TKForm('Send Email')
form.geometry('480x368')

# #	fonts
# labelFont = tkinter.font.nametofont("TkTextFont")
# #labelFont.config(weight='bold', size=12)
# headingFont = labelFont.copy()
# headingFont.config(size=24)
# comboboxFont = labelFont.copy()
# comboboxFont.config(weight='normal', size=12)
# entryFont = tkinter.font.nametofont("TkFixedFont")
# #entryFont.config(size=12)
# linkFont = entryFont.copy()
# linkFont.config(weight='normal', underline=False)
# linkHoverFont = entryFont.copy()
# linkHoverFont.config(weight='bold', underline=True)
#
# #	ttk Styles
# #tkinter.ttk.Style().configure('TLabel',foreground="#666666", font=labelFont)
# tkinter.ttk.Style().configure('heading.TLabel', foreground='#133796', font=headingFont)
# tkinter.ttk.Style().configure('link.TLabel',foreground='#133796',font=linkFont)
# tkinter.ttk.Style().configure('link.hover.TLabel',foreground='#133796',font=linkHoverFont)
# tkinter.ttk.Style().configure('TListbox',weight='normal', font=comboboxFont)
# form.option_add('*TCombobox*Listbox.font', comboboxFont)   # apply font to combobox list
#
#	form variables
subject = tkinter.StringVar(form, 'Test')
fromName = tkinter.StringVar(form, 'Name')
fromEmail = tkinter.StringVar(form, 'user@example.com')
fromAddress = tkinter.StringVar(form, f'{fromName.get()} <{fromEmail.get()}>')
toName = tkinter.StringVar(form, 'Other Name')
toEmail = tkinter.StringVar(form, 'user@example.net')
toAddress = tkinter.StringVar(form, f'{toName.get()} <{toEmail.get()}>')
body = '''message'''.strip()
attachment = tkinter.StringVar(form, '')
savePrefs = tkinter.BooleanVar(form, True)

def updateAddresses(*args):
	if name := fromNameTextbox.get():
		fromAddress.set(f'{fromNameTextbox.get()} <{fromEmailTextbox.get()}>')
	else:
		fromAddress.set(fromEmailTextbox.get())

	if name := toNameTextbox.get():
		toAddress.set(f'{toNameTextbox.get()}  <{toEmailTextbox.get()}>')
	else:
		toAddress.set(toEmailTextbox.get())

def doSendMail(*args):
	data = {
		'from-address': fromAddress.get(),
		'to-address': toAddress.get(),
		'subject': subject.get(),
		'message': messageTextbox.get('1.0', tkinter.END).strip(),
		'attachment': attachment.get(),
	}
	errors = micromailer.checkMail(data)

	if not errors:
		okButton.configure(state=tkinter.DISABLED)
		micromailer.sendMail(data)
		tkinter.messagebox.showinfo(title='Sent', message='Message Sent')
		okButton.configure(state=tkinter.ACTIVE)

		#	save prefs
		data = {
			'from-name': fromName.get(),
			'from-email': fromEmail.get(),
			'to-name': toName.get(),
			'to-email': toEmail.get(),
			'subject': subject.get(),
			'message': messageTextbox.get('1.0', tkinter.END).strip(),
			'attachment': attachment.get(),
		}

		if savePrefs.get():
			prefs.save(data)

	else:
		tkinter.messagebox.showerror(title='Missing Data', message='\n'.join(errors))

heading = tkform.Label(form, 'Send Email', style="heading.TLabel")
form.add(heading, row=1, column=1, columnspan=8)

fromNameLabel = tkform.BoldLabel(form, 'From Name (optional)')
fromNameTextbox = tkform.Textbox(form,textvariable=fromName)
fromEmailLabel = tkform.BoldLabel(form, 'From Email')
fromEmailTextbox = tkform.Textbox(form, textvariable=fromEmail)

form.add(fromNameLabel, row=2, column=1, columnspan=4)
form.add(fromNameTextbox, row=3, column=1, columnspan=4, sticky='we')
form.add(fromEmailLabel, row=2, column=5, columnspan=4)
form.add(fromEmailTextbox, row=3, column=5, columnspan=4, sticky='we')

fromAddressLabel = tkform.Label(form, 'From Address')
fromAddressValue = tkform.Label(form, '', textvariable=fromAddress)
fromName.trace(mode='w', callback=updateAddresses)
fromEmail.trace(mode='w', callback=updateAddresses)
#form.add(fromAddressLabel, row=4, column=1)
form.add(fromAddressValue, row=4, column=1, columnspan=8, sticky='we')

toNameLabel = tkform.BoldLabel(form, 'To Name (optional)')
toNameTextbox = tkform.Textbox(form, textvariable=toName)
toEmailLabel = tkform.BoldLabel(form, 'To Email')
toEmailTextbox = tkform.Textbox(form, textvariable=toEmail)

form.add(toNameLabel, row=5, column=1, columnspan=4)
form.add(toNameTextbox, row=6, column=1, columnspan=4, sticky='we')
form.add(toEmailLabel, row=5, column=5, columnspan=4)
form.add(toEmailTextbox, row=6, column=5, columnspan=4, sticky='we')

toAddressLabel = tkform.Label(form, 'To Address')
toAddressValue = tkform.Label(form, '', textvariable=toAddress)
toName.trace(mode='w', callback=updateAddresses)
toEmail.trace(mode='w', callback=updateAddresses)
#form.add(toAddressLabel, row=7, column=1)
form.add(toAddressValue, row=7, column=1, columnspan=8, sticky='we')

subjectLabel = tkform.BoldLabel(form, 'Subject')
subjectTextbox = tkform.Textbox(form, textvariable=subject)
form.add(subjectLabel, row=8, column=1)
form.add(subjectTextbox, row=8, column=2, columnspan=7, sticky='we')

messageLabel = tkform.BoldLabel(form, 'Message:')
messageTextbox = tkform.Textarea(form, height=4, width=80, text=body)
form.add(messageLabel, row=9, column=1, columnspan=8)
form.add(messageTextbox, row=10, column=1, columnspan=8, sticky='we')

def getAttachment():
	path = tkinter.filedialog.askopenfilename(title='Attach File')
	if path:
		attachmentTextbox.delete(0, 'end')
		attachmentTextbox.insert(0, path)

attachmentTextbox = tkform.Textbox(form, textvariable=attachment)
attachmentButton = tkform.Button(form, text='Attach …', command=getAttachment)
form.add(attachmentTextbox, row=11, column=1, columnspan=7, sticky='we')
form.add(attachmentButton, row=11, column=8)

savePrefsCheckbox = tkform.Checkbox(form, 'Save Prefs', textvariable=savePrefs)
form.add(savePrefsCheckbox, row=12, column=1)
okButton = tkform.OKButton(form, text='OK', command=doSendMail)
cancelButton = tkform.CancelButton(form, 'Cancel')
form.add(okButton, row=12, column=8)
form.add(cancelButton, row=12, column=7)

def setForm(data):
	subject.set(data['subject'])
	fromName.set(data['from-name'])
	fromEmail.set(data['from-email'])
	toName.set(data['to-name'])
	toEmail.set(data['to-email'])
	messageTextbox.delete('0.0', tkinter.END)
	messageTextbox.insert('0.0', data['message'])
	attachment.set(data['attachment'])

	updateAddresses()

prefs.load()

#	ini file
if len(sys.argv) > 1:
	inipath = sys.argv[1]
	if os.path.isfile(inipath):
		inidata = readIni(inipath)['micromailer']
		setForm(inidata)
		prefs.save(inidata)
elif prefsData := prefs.load():
	setForm(prefsData)
prefs.load()
form.show()
