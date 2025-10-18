import random

# Reproduzierbare «zufällige» Würfelwürfe
random.seed(42)
a = [random.randrange(6)+1 for _ in range(600)]
print(a)

# Zählen Sie, wie viel mal die Zahl 6 im Array a gespeichert ist
# Geben Sie den Text "Es sind ... 6en gewürfelt worden" aus. (Lsg 107)





# Finden Sie die Länge und Startindex der längsten Untersequenz ohne 6en. (Lsg 384, 23)
# Überlegen Sie sich genau und detailliert, wie man das von Hand machen würde und 
# übersetzen Sie in Python

