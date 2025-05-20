def EstimateRemaining(start,current,required,timed):
    left = required-current
    done= current-start
    if(done>0):
        timeleft = timed*(left/done)
        return timeleft
    return "Inconnue"
