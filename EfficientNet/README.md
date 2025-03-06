


**Función seed_everything(seed)**
Esta función garantiza la reproducibilidad de los resultados fijando las semillas para los generadores de números aleatorios en Python, NumPy y PyTorch.

**Descripción de los hiperparámetros:**

* seed = 42: Fija la semilla para asegurar reproducibilidad (el número 42 es popular en la comunidad de ciencia de datos por la referencia a The Hitchhiker's Guide to the Galaxy 😎).
* batch_size = 64: Cantidad de muestras por lote durante el entrenamiento.
epochs = 4: Número de veces que el modelo verá el conjunto completo de datos.

* lr (learning rate): Tasa de aprendizaje para el optimizador, controla cuánto se ajustan los pesos en cada paso.

* gamma: Parece ser el factor de decaimiento de la tasa de aprendizaje o un parámetro para funciones como learning rate scheduler.

* residual_dropout: Probabilidad de dropout en capas residuales para evitar sobreajuste.
