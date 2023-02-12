from flet import *
import pytesseract
import cv2


def main(page:Page):
	resulttext = Column(scroll="always")

	def scanocrnow(e):
		page.snack_bar = SnackBar(
			Column([
				Row([
					Text("Process you text ...",
						size=30,weight="bold"
					),
					ProgressRing()

					],alignment="center")

				],alignment="center"),
			bgcolor="green"

			)
		page.snack_bar.open = True
		page.update()

		# AND GET YOU FILE 
		for x in e.files:
			print(x.path)
			image = cv2.imread(x.path)
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			text = pytesseract.image_to_string(gray)
			with open("output.txt", "w") as file:
				file.write(text)
				resulttext.controls.append(
                    Text(text,weight="bold")
                    )
				page.update()
    


	def copytext(e):
		# AND COPY TO CLIPBOARD YOU TEXT RESULT
		with open("output.txt","r") as file:
			text = file.read()
			print(text)
			page.set_clipboard(text)
			page.update()


	# CREATE UPLOAD PICK FILE
	file_picker = FilePicker(
		on_result=scanocrnow

		)

	page.overlay.append(file_picker)

	page.add(
	Column([
	Text("Ocr image text to text",size=30,weight="bold"),
	ElevatedButton("Scan Image upload",
		bgcolor="blue",color="white",
	on_click=lambda e:file_picker.pick_files()
	),

	# AND CREATE COPY ICON FOR COPY TEXT RESULT
	IconButton(icon="copy",on_click=copytext),
	resulttext


	])
	)


flet.app(target=main)
