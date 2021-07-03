import requests
import re
import csv
import time

def strip_tags(text):
	clean = re.compile('<.*?>')
	text = re.sub(clean, '', text)
	text = re.sub('\s+', ' ', text)
	text = text.replace('\n', '').replace('\r', '')
	text = text.strip()
	return text

with open('data.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	for letter in range(65, 91): # A to Z
		url = "http://controltowers.co.uk/" + chr(letter) + "list.htm"
		x = requests.get(url)
		content = x.content.decode("iso-8859-1")
		table_start = content.find('<table width="640" border="0" align="center">')
		table_end = content.find('</table>', table_start)
		body = content[table_start:table_end]
		
		row = []
		offset = 0
		
		while True:
			offset = body.find("<tr ", offset)
			if offset == -1:
				break
			row_end = body.find("</tr>", offset)
			row_html = body[offset:row_end]
			cell_offset = 0
			while True:
				cell_offset = row_html.find("<td ", cell_offset)
				if cell_offset == -1:
					offset = row_end
					break
				end = row_html.find("</td>", cell_offset)
				cell = strip_tags(row_html[cell_offset:end])
				cell_offset = end
				row.append(cell)
			if not (len(row) == 1 and row[0] == ""):
				print(row)
				writer.writerow(row)
			row = []
		
		time.sleep(1)