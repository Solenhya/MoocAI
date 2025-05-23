def TranslateSentiment(value):
    if value<-1:
        return "Negatif"
    elif value<1:
        return "Neutre"
    else:
        return "Positif"
