

string = '012345678901234567890123456789012345678901234567890123456789'

lista = []
lista =  [v for v in string if v not in lista ]

#lista = [v for v in string]

print(lista)