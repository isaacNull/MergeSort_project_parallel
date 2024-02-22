# multithreaded vs sequential programming applied to the merge sort sorting algorithm
# 
# MANDELBROT SET FRACTAL 
# tested in 
# Processor : AMD Ryzen 7 3700U, 2300Mhz 
# GPU : Radeon Vega Mobile Gfx,
# Cores : 4, 8 (Logical()
# OS : Windows 11 Home OLT
# Architecture : x64

# Importar librerias 
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import time

# determina si el numero de iteraciones del pixel en el plano complejo 
def calculate_mandelbrot_set_pixel(c, max_iterations):
    z = c
    for k in range(max_iterations):
        if abs(z) > 2: #salen del radio 2 en el plano complejo
            return k
        z = z * z + c  #pertenecen al conjunto de mandelbrot
    return max_iterations

# genera el plano complejo de iteraciones en cada pixel 
# genera el conjunto de mandelbro de manera secuencial 
def generate_mandelbrot_set_sequential(xcoordinates, ycoordinates, max_iterations):
    M, N = len(ycoordinates), len(xcoordinates) # dimensiones del conjunto de mandelbrot
    mandelbrotSet = np.zeros((M, N), dtype=np.uint8) # creamos una matriz de ceros 

    for i in range(M):
        for j in range(N):
            x, y = xcoordinates[j], ycoordinates[i]
            c = x + y * 1j # numero complejo para c/u de las coordenadas 
            mandelbrotSet[i, j] = calculate_mandelbrot_set_pixel(c, max_iterations)

    return mandelbrotSet

# genera el conjunto de mandelbrot de manera paralela
def generate_mandelbrot_set_multithreaded(xcoordinates, ycoordinates, max_iterations):
    M, N = len(ycoordinates), len(xcoordinates)
    
    # with ThreadPoolExecutor(max_workers=16) as executor:
    #     mandelbrotSet = list(executor.map([0] * N, range(M)))
    
    mandelbrotSet = [[0] * N for _ in range(M)] # llenar de ceros una matriz M x N

    # para cada lista calculate_mandelbrot_set_pixel
    def calculate_row(i):
        row_values = [0] * N
        for j in range(N):
            x, y = xcoordinates[j], ycoordinates[i]
            c = x + y * 1j # numero complejo para c/u de las coordenadas
            row_values[j] = calculate_mandelbrot_set_pixel(c, max_iterations)
        return row_values

    # parte multithreading
    with ThreadPoolExecutor(max_workers=16) as executor:
        row_results = list(executor.map(calculate_row, range(M)))

    for i, row in enumerate(row_results):
        mandelbrotSet[i] = row

    return mandelbrotSet

def main():
    x1, y1 = -2.0, -1.0 # coordenadas del punto inferior izquierdo en el plano complejo
    x2, y2 = 2.0, 1.0   # coordenadas del punto superior derecho en el plano complejo
    linear_resolution = 500 # num puntos en los ejes x e y 
    max_iterations = 38 # numero maximo de iteraciones para generar el fractal

    # coordenadas equispaciadas 
    xcoordinates_seq = np.linspace(x1, x2, linear_resolution)
    ycoordinates_seq = np.linspace(y1, y2, linear_resolution)
    xcoordinates = [x1 + (x2 - x1) * i / linear_resolution for i in range(linear_resolution+1)]
    ycoordinates = [y1 + (y2 - y1) * i / linear_resolution for i in range(linear_resolution+1)]

    # Medimos el tiempo 
    t1 = time.perf_counter()
    mandelbrotSet = generate_mandelbrot_set_multithreaded(xcoordinates, ycoordinates, max_iterations)
    t2 = time.perf_counter()
    mandelbrotSet_seq = generate_mandelbrot_set_sequential(xcoordinates_seq, ycoordinates_seq, max_iterations)
    t3 = time.perf_counter()
    speedup = (t3-t2)/(t2-t1)

    print(f"Tiempo multithreading: {t2 - t1:.2f} segundos")
    print(f"Tiempo secuencial : {t3-t2:.2f} segundos")
    print(f'Speedup = {speedup}')
    print(f'Efficent = {speedup / 4}')

    plt.imshow(mandelbrotSet, extent=(x1, x2, y1, y2), cmap="hot")
    plt.colorbar()
    plt.title("Set de Mandelbrot (Multithreading)")
    plt.xlabel("Parte real")
    plt.ylabel("Parte imaginaria")
    plt.show()

    plt.imshow(mandelbrotSet_seq, extent=(x1, x2, y1, y2), cmap="hot")
    plt.colorbar()
    plt.title("Set de Mandelbrot (Secuencial)")
    plt.xlabel("Parte real")
    plt.ylabel("Parte imaginaria")
    plt.show()

if __name__ == "__main__":
    main()
