#‎14.04.2026 ‏‎11:07:35 - 14:35 21.04.2026
#SilverMiner
#Accurate FloatBob calculator
#Made cuz there are formulas for other math tables in doom
#but I haven't found formulae for FloatBob, so I made one.
#I suspect it could be calculated from finesine, but I'm lazy to try

import math

def calculate_floatbob(x):
    a = 0.098220141219
    b = 524287.426427
    c = 0.00080802
    
    p0 = -423.791967
    p1 = -23.78662478
    p2 = 0.0015513871
    p3 = -0.000023900279
    
    sin_part = b * math.sin(a * x + c)
    
    polynomial = p0 + p1 * x + p2 * (x ** 2) + p3 * (x ** 3)
    
    cos_part = polynomial * math.cos(a * x)
    
    return round(sin_part + cos_part)


def main():
    reslist = []
    for x in range(0, 64):
        result = calculate_formula(x)
        reslist.append(result)
    print(reslist)
        
if __name__ == "__main__":
    main()
