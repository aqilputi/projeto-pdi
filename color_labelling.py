def label_colors(colors):
    labels = [[],[],[]]
    for index,row in enumerate(colors, start=0):
    #print(row)
        for value in row:
            #print(value)
            HUE = value[0]
            L = value[1]
            S = value[2]
            #Checar se o pixel for Branco: L > 150 e S < 30, valores escolhidos
            if L > 200:
                label = 'WHITE'
            elif HUE > 35 and HUE < 41:
                label = 'YELLOW'
            elif HUE > 5 and HUE < 16:
                label = 'ORANGE'
            elif HUE > 140 and HUE < 165:
                label = 'BlUE'
            elif HUE > 90 and HUE < 115:
                label = 'GREEN'
            else:
                label = 'RED'
            labels[index].append(label)
    return labels

colors = [
    [[160.39, 81.0, 229.81], [23.45, 233.5, 171.98], [35.96, 131.5, 255.0]],
    [[94.68, 61.5, 209.39], [252.03, 110.0, 215.59], [160.38, 78.5, 222.52]],
    [[8.21, 136.5, 250.7], [251.84, 102.0, 235.0], [160.59, 83.5, 200.03]],
]

print(label_colors(colors))
