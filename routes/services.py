import pandas as pd

xlsx_data = "data/HINDALCO_1D.xlsx"

data = pd.read_excel(xlsx_data)
print(data)
