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
        if L > 100 and S < 30:
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
