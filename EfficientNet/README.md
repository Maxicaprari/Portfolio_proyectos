


**Función seed_everything(seed)**
Esta función garantiza la reproducibilidad de los resultados fijando las semillas para los generadores de números aleatorios en Python, NumPy y PyTorch.

**Descripción de los hiperparámetros:**

* seed = 42: Fija la semilla para asegurar reproducibilidad (el número 42 es popular en la comunidad de ciencia de datos por la referencia a The Hitchhiker's Guide to the Galaxy 😎).
* batch_size = 64: Cantidad de muestras por lote durante el entrenamiento.
epochs = 4: Número de veces que el modelo verá el conjunto completo de datos.

* lr (learning rate): Tasa de aprendizaje para el optimizador, controla cuánto se ajustan los pesos en cada paso.

* gamma: Parece ser el factor de decaimiento de la tasa de aprendizaje o un parámetro para funciones como learning rate scheduler.

* residual_dropout: Probabilidad de dropout en capas residuales para evitar sobreajuste.




# TRANSFORMACIÓN DE LOS DATOS 
Este código utiliza torchvision.transforms para preprocesar y aumentar imágenes antes de pasarlas a un modelo en PyTorch. Define transformaciones para el conjunto de entrenamiento (train_transforms), validación (val_transforms) y prueba (test_transforms).

**torchvision.transforms (T):** Módulo de PyTorch para aplicar transformaciones y aumentaciones a imágenes.

**InterpolationMode:** Define el tipo de interpolación para el cambio de tamaño. Aquí se usa BICUBIC, que es adecuado para mantener la calidad de las imágenes.

**Transformaciones aplicadas:**

* T.Resize(224, interpolation=InterpolationMode.BICUBIC):
Cambia el tamaño de las imágenes a 224x224 píxeles usando interpolación bicúbica.

* T.RandomResizedCrop(224):
Recorta aleatoriamente una región de la imagen y la redimensiona a 224x224, ayudando a la generalización.

* T.RandomHorizontalFlip():
Invierte la imagen horizontalmente con una probabilidad de 50%.

* T.RandomVerticalFlip():
Invierte la imagen verticalmente con una probabilidad de 50%.

* T.RandomRotation(20):
Rota la imagen aleatoriamente hasta ±20 grados.

* T.GaussianBlur(kernel_size=(7, 13), sigma=(0.1, 1.0)):
Aplica un desenfoque gaussiano aleatorio con tamaños de kernel y sigma variables, simulando ruido.

* T.ColorJitter(...):
Ajusta aleatoriamente el brillo, contraste, saturación y tono para aumentar la robustez del modelo.

* T.ToTensor():
Convierte la imagen a tensores y escala los valores de píxeles a [0, 1].

* T.Normalize(mean, std):
Normaliza los tensores usando las medias y desviaciones estándar típicas de ImageNet:

mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]

**Transformaciones para la validación**
* Sin aumentaciones aleatorias: Mantiene las imágenes consistentes para evaluar el rendimiento real.

* T.CenterCrop(224): Recorta el centro de la imagen a 224x224.

* T.ToTensor() y T.Normalize(...): Igual que en entrenamiento, para mantener la coherencia.

