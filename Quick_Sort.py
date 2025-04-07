def partitioning(elements,start,end):
    pivot_index = start
    pivot = elements[pivot_index]
    
    while start < end:
        while start < len(elements) and elements[start] <= pivot:
            start += 1
        while start < len(elements) and elements[end] > pivot:   
            end -= 1
        
        if start < end:
            elements[start], elements[end] = elements[end], elements[start]

    elements[pivot_index], elements[end] = elements[end], elements[pivot_index]
    return end

def quick_sort(elements,start,end):
    #partition the elements - left is lesser and right is greater 
    #first element is the pivot
    #use start(2nd) and end (last) pointers - move start to right when lesser than pivot - stop when greater than pivot - check end and move left 
    #if end is greater than pivot - stop when end is lesser than pivot - swap with start - swap with pivot when end crossed start  
    if start <end : 
        partition_index = partitioning(elements,start,end)
        quick_sort(elements,start,partition_index-1) #left   partition  
        quick_sort(elements,partition_index + 1 ,end) #right  partition 


if __name__ == "__main__":
    elements = [23,6,4,-1,0,12,8,3,1]
    start = 0  
    end = len(elements)-1 
    quick_sort(elements,start, end )
    print(elements)

