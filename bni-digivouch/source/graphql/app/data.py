import tinydb, openpyxl

wb = openpyxl.load_workbook(filename='digital-product.xlsx')

db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)

key = []

def setup():
	global db, wb, key
	sheet_ranges = wb['yg dijual']

	is_first_row = True
	
	for row in sheet_ranges.values:
		if is_first_row:
			for value in row:
				key.append(value)
			is_first_row = False
		else:
			iterator = iter(key)
			db_row = {}
			for value in row:
				field = next(iterator)
				print(field + ': ' +value)
				db_row[field]= value
			db.insert(db_row)
