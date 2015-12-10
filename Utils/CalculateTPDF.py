import math

t = 4.
df = 11.
step = t/100000.
print step
iters = 0.
rollingSum = 0.
numerator = math.gamma((df + 1)/2)
print numerator
denominator1 = math.gamma(df / 2)
print denominator1
denominator2 = math.sqrt(df * math.pi)

while iters < t-.02:
    denominator3 = (1 + (iters ** 2 / df)) ** ((df + 1) / 2)
    tpdf1 = (numerator / denominator1 / denominator2 / denominator3)
    iters += step
    #print iters
    denominator3 = (1 + (iters ** 2 / df)) ** ((df + 1) / 2)
    tpdf2 = (numerator / denominator1 / denominator2 / denominator3)

    rollingSum += step * (tpdf1 + tpdf1) / 2.
    #print iters
    #print (numerator / denominator1 / denominator2 / denominator3)
print rollingSum + 0.5
