elementos = ["a", "b", "c", "d", "e"]

temp = []
temp += "(", elementos[0], "|", elementos[1], ")"
for i in range(2, len(elementos)):
    temp2 = temp.copy()
    temp = []
    temp.append("(")
    temp += temp2
    temp.append("|")
    temp.append(elementos[i])
    temp.append(")")


print(temp)
