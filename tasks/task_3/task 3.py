from modules.Table import Table

table = Table()
table.load_table('unified.csv', 'u2.csv', set_types=True)
copy = table.get_rows_by_number(3, copy_table=True)
table.save_table('splitted.csv', max_rows=5)

print(copy)

table.print_table()
