base = 1000
expo = int(base/10)

def lvl2xp(lvl):
    return(int(base + expo * (lvl**2)))

def totalxp(lvl, xp):
    lvl = lvl - 1
    basexp = lvl * base
    sqsum = lvl * (lvl+1) * ((2*lvl) + 1) / 6
    return(int(sqsum * expo + basexp + xp))
