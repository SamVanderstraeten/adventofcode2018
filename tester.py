s = [1,2,3,4,5,6,7,8,9,0]
searchlen = 4
sub = s[-(searchlen+1):-1]
r = ''.join(str(x) for x in sub)
print(r)