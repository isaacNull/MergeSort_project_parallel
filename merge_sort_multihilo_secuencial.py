# multithreaded vs sequential programming applied to the merge sort sorting algorithm
# 
#
# tested in 
# Processor : AMD Ryzen 7 3700U, 2300Mhz 
# GPU : Radeon Vega Mobile Gfx,
# Cores : 4, 8 (Logical()
# OS : Windows 11 Home OLT
# Architecture : x64

# Importar librerias 
import random
import time
from concurrent.futures import ThreadPoolExecutor
import timeit

# numero de elementos de un array
MAX_ITEMS = 1000000

# funcion recursiva secuencial del merge sort
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    # dividimos por la mitad el array
    # Calculamos el elemento medio
    midddle = len(arr) // 2 #redondea al menor
    left = arr[:midddle]    #arr de la izquierda
    right = arr[midddle:]   #arr de la derecha

    # Aplicamos recursivadad
    left = merge_sort(left)   
    right = merge_sort(right)

    return merge(left, right)

# funcion merge para fusionar los array, funciona a nivel global
def merge(left, right):
    arr_merge = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            arr_merge.append(left[left_index])
            left_index += 1
        else:
            arr_merge.append(right[right_index])
            right_index += 1

    # si ya no queda un array de un lado o del otro
    if left_index < len(left):
        arr_merge.extend(left[left_index:])
    if right_index < len(right):
        arr_merge.extend(right[right_index:])

    return arr_merge

# funcion recursiva paralela multihilo de merge sort
def threaded_merge_sort(arr, depth=0, max_depth=2):
    if len(arr) <= 1:
        return arr

    midddle = len(arr) // 2
    left = arr[:midddle]
    right = arr[midddle:]

    if depth < max_depth:
        with ThreadPoolExecutor(max_workers=8) as executor:
            left_future = executor.submit(
                threaded_merge_sort, left, depth + 1, max_depth
            )
            right_future = executor.submit(
                threaded_merge_sort, right, depth + 1, max_depth
            )
            left = left_future.result()
            right = right_future.result()
    else:
        left = threaded_merge_sort(left, depth + 1, max_depth)
        right = threaded_merge_sort(right, depth + 1, max_depth)

    return merge(left, right)


if __name__ == "__main__":
    #Creamos y llenamos un array con numeros aleatorios del 1 al 1000  
    arr = [random.randint(1, 10000) for _ in range(MAX_ITEMS)]
    # print(f'El siguiente array ha ordenar es : {arr}')

    # Medir el tiempo 
    start_time = time.time()    
    sorted_arr = merge_sort(arr)
    end_time = time.time()
    print(f"Tiempo de algoritmo merge sort Threaded: {end_time - start_time:.5f} segundos")

    start_time = time.time()
    sorted_arr_threaded = threaded_merge_sort(arr)
    end_time = time.time()
    print(f"Tiempo de algoritmo merge sort Non-threaded: {end_time - start_time:.5f} segundos")
