import math

def tadd(t1,t2):
    return (t1[0]+t2[0], t1[1]+t2[1])
def tsub(t1,t2):
    return (t1[0]-t2[0], t1[1]-t2[1])
def tmult(t1,t2):
    return (t1[0]*t2[0], t1[1]*t2[1])
def tdiv(t1, t2):
    return (t1[0] / t2[0], t1[1] / t2[1])
def tmod(t1,t2,t2weight):
    return  ((t1[0] + t2[0]*t2weight)/(t2weight+1),(t1[1] + t2[1]*t2weight)/(t2weight+1))
def neg(t):
    return(-t[0], -t[1])
def tnrml(t):
    magnitude = math.sqrt(t[0] * t[0] + t[1] * t[1])
    if magnitude > 0:
        return (t[0] / magnitude, t[1] / magnitude)
    else:
        return (0, 0)
def limit(vector, max_value):
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if magnitude > max_value:
        return (vector[0] * max_value / magnitude, vector[1] * max_value / magnitude)
    else:
        return vector
