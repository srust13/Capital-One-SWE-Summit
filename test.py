def use():
    myset={"four"}
    mylist=["one","two","one"]
    for i in mylist:
        myset.add(i)
    myset=list(myset)
    myset.sort(), mylist.sort() 
    return myset, mylist

print(use()[0])

print(use()[1])