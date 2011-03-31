#Contains useful functions
def Slope(PosA, PosB):
    """Calculates the slope between two points"""
    if PosA[0] == PosB[0]:
        #The points are vertically aligned
        return 0;
    else:
        return (float(PosA[1]) -\
                float(PosB[1])) /\
               (float(PosA[0]) -\
                float(PosB[0]))
