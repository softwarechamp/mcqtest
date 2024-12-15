from openpyxl import load_workbook

# Load the workbook and select the active sheet
input_file = "SingleRecord.xlsx"
workbook = load_workbook(input_file)
sheet = workbook.active

# Read headers (optional)
headers = [cell.value for cell in sheet[1]]  # Assuming headers are in the first row
print("Headers:", headers)

# Read the first record (after headers)
record_row = 2  # Assuming the first record is in the second row
record = [cell.value for cell in sheet[record_row]]
print("Record:", record)