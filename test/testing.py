value = '1'
possible_separators = [',', '.']
last_symbol = next((c for c in value[::-1] if c in possible_separators), None)

print(last_symbol)