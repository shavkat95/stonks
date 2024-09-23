
def normalize(data):
    
    sum_ = sum(data)
    print('sum: '+str(sum_))
    
    for i in range(len(data)):
        data[i] = data[i] / sum_
    return data






# define data
data = [1.994017946,3.316749585,4.962779156,9.852216749,19.41747573,31.74603175,46.51162791,86.95652174,153.8461538,222.2222222,285.7142857,400,666.6666667,1960.784314,1960.784314,666.6666667,285.7142857,117.6470588,54.05405405,35.0877193,20.6185567,10.15228426,5.037783375,3.350083752,2.006018054]
# convert list of numbers to a list of probabilities
data = normalize(data)
# data = softmax(data)
# data = softmax(data)
# data = softmax(data)
# result = softmax(data)
# report the probabilities
print(data)
# report the sum of the probabilities
print(sum(data))


