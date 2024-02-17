

# por legibilidade, devolve uma lista de maps (que associam  valores de uma linha aos vários titulos das tabelas)
# podia só fazer lista de listas tmb
def parseCSV(filename: chr) -> [[str]]:
    parsedCSV = []
    f = open(filename,'r')
    lines = f.readlines()
    fields = lines[0].strip().split(",")
    for line in lines[1:]:
        splitLine = line.strip().split(",")
        lineMap = {fields[i]: splitLine[i] for i in range(len(fields))} # criar map que associa cada campo ao respetivo valor
        parsedCSV.append(lineMap)
    return parsedCSV

#gerar estatísticas
def generateStatistics(csv):
    modalidades = set()
    aptos = 0
    inaptos = 0
    escaloes = [0] * 20 # criar array com 20 zeros

    for line in csv:
        #modalidades
        modalidades.add(line['modalidade'])
        #aptidao
        if (line['resultado'] == "true"):
            aptos += 1
        else:
            inaptos += 1

        #escaloes
        intervalo = int(line['idade']) // 5 # divisao inteira
        escaloes[intervalo] += 1

    totalAtletas = aptos + inaptos

    print(f"Modalidades desportivas encontradas: {sorted(modalidades)}\n")
    print(f"Atletas| aptos: {(aptos / totalAtletas) * 100}% inaptos: {(inaptos / totalAtletas) * 100}%\n")
    print("Escalões intervalos:")
    for i in range(0,20):
        if (escaloes[i] != 0):
            print(f"[{i*5},{i*5+4}]: {(escaloes[i] / totalAtletas) * 100:.2f}%")

def main():
    csv = parseCSV("emd.csv")
    generateStatistics(csv)



if __name__ == "__main__":
    main()