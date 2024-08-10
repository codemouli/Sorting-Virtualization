import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import sys
def swap(data, i, j):
    if i!=j:
        data[i], data[j] = data[j], data[i]
def quick_sort(data, start, end):
    if start>=end:
        return 
    pivot = data[end]
    pivot_index = start

    for i in range(start, end):
        if data[i]<pivot:
            swap(data, i, pivot_index)
            pivot_index+=1
        yield data
    swap(data, end, pivot_index)
    yield data

    yield from quick_sort(data, start, pivot_index-1)
    yield from quick_sort(data, pivot_index+1, end)


def bubble_sort(data, length):
    for i in range(length):
        for j in range(0, length-i-1):
            if data[j]>data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
            yield data


def merge_sort(data, left, right):

    if left>=right:
        return
    mid = (left+right)//2

    yield from merge_sort(data, left, mid)
    yield from merge_sort(data, mid+1, right)
    yield from merge(data, left, right, mid)

    yield data

def merge(data, left, right, mid):

    left_data = data[left:mid+1].copy()
    right_data = data[mid+1:right+1].copy()

    l, r = 0, 0
    k = left

    while l<len(left_data) and r<len(right_data):
        yield data
        if left_data[l] <= right_data[r]:
            data[k] = left_data[l]
            l+=1
        else:
            data[k] = right_data[r]
            r+=1
        k+=1
    while l<len(left_data):
        yield data
        data[k] = left_data[l]
        l+=1
        k+=1
    while r<len(right_data):
        yield data
        data[k] = right_data[r]
        r+=1
        k+=1
    
input_length = int(input("Please enter the array length you want to sort "))

if not isinstance(input_length, int):
    sys.exit("please enter the valid input. Kill the program")


# Creating random data for sort operation
input_data = np.random.permutation(np.random.randint(1, 50, input_length))

# creating a copy data for each sorting algorithm
bubble_data = input_data.copy()
merge_data = input_data.copy()
quick_data = input_data.copy()

# calling each sorting technique generator function
merge_generator = merge_sort(merge_data, 0, merge_data.size-1)
bubble_generator = bubble_sort(bubble_data, bubble_data.size)
quick_generator = quick_sort(quick_data, 0, quick_data.size-1)

# creating figure and adding bar chart with random data
figure, ax = plt.subplots(3, 1, figsize=(10,8))

merge_rects = ax[0].bar(range(0, merge_data.size), merge_data)
bubble_rects = ax[1].bar(range(0, bubble_data.size), bubble_data)
quick_rects = ax[2].bar(range(0, quick_data.size), quick_data)

# creating completion text object and text message to indicate that sorting is completed 
merge_completion_text_obj = ax[0].text(0.5, 1.05, '', transform=ax[0].transAxes, ha='center')
merge_completion_text = "Merge sort completed"
bubble_completion_text_obj = ax[1].text(0.5, 1.05, '', transform=ax[1].transAxes, ha='center')
bubble_completion_text = "Bubble sort completed"
quick_completion_text_obj = ax[2].text(0.5, 1.05, '', transform=ax[2].transAxes, ha='center')
quick_completion_text = "Quick sort completed"

# Added custom feature to display message when each animation is completed in figure 
class MyFuncAnimation(animation.FuncAnimation):

    def __init__(self, fig, func, frames=None, init_func=None, fargs=None,
                 save_count=None, *, cache_frame_data=True, completion_text_obj=None, completion_text=None, **kwargs):
        self._my_completion_text_obj= completion_text_obj
        self._my_completion_text = completion_text
        super().__init__(fig, func, frames, init_func, fargs,
                 save_count, cache_frame_data=cache_frame_data, **kwargs)

    def _step(self, *args, **kwargs):
        
        still_going = super()._step(*args)

        # custom code
        if not still_going:
            if self._my_completion_text_obj:
                message = self._my_completion_text or "This animation completed"
                self._my_completion_text_obj.set_text(message)
                self._fig.canvas.draw_idle()
            return False
        return True

# funtion to update data in figure
def merge_update(generator, rects):
    for rect, data in zip(rects, generator):
        rect.set_height(data)
draw_check = [True]
merge_ani = MyFuncAnimation(figure,merge_update, frames= merge_generator, fargs=(merge_rects,), 
                            cache_frame_data=False, interval=20, 
                            repeat=False, completion_text_obj=merge_completion_text_obj, 
                            completion_text=merge_completion_text)


def bubble_update(generator, rects):
    for rect, data in zip(rects, generator):
        rect.set_height(data)

bubble_ani = MyFuncAnimation(figure, bubble_update, frames=bubble_generator, fargs=(bubble_rects,),
                              cache_frame_data=False, interval=20, repeat= False,  
                              completion_text_obj=bubble_completion_text_obj,
                                completion_text=bubble_completion_text)

def quick_update(generator, rects):
    for rect, data in zip(rects, generator):
        rect.set_height(data)
    
quick_ani = MyFuncAnimation(figure, quick_update, frames=quick_generator, fargs=(quick_rects, ),
                             cache_frame_data=False, interval=20, repeat=False, 
                             completion_text_obj=quick_completion_text_obj, 
                             completion_text=quick_completion_text)
plt.subplots_adjust(top=0.945, bottom=0.045, hspace=0.24)

plt.show()