def label_colors(colors):
    labels = [[],[],[]]
    for index,row in enumerate(colors, start=0):
        for value in row:
            HUE = value[0]
            L = value[1]
            S = value[2]
            #Checar se o pixel for Branco: L > 150 e S < 30, valores escolhidos
            if L > 300:
                label = 'WHITE'
            elif HUE > 55 and HUE <= 70:
                label = 'YELLOW'
            elif HUE > 35 and HUE <= 55:
                label = 'ORANGE'
            elif HUE > 165 and HUE <= 265:
                label = 'BLUE'
            elif HUE > 70 and HUE <= 165:
                label = 'GREEN'
            else:
                label = 'RED'
            labels[index].append(label)
    return labels