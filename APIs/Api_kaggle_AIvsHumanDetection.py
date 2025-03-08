# Establecer semilla para reproducibilidad
seed = 42
np.random.seed(seed)

# Descargar los datos del concurso
!kaggle competitions download -c detect-ai-vs-human-generated-images

# Descomprimir el archivo
!unzip -q detect-ai-vs-human-generated-images.zip -d ai-vs-human

# Configurar las rutas correctas
base_dir = '/content/ai-vs-human'
train_csv_path = os.path.join(base_dir, 'train.csv')
test_csv_path = os.path.join(base_dir, 'test.csv')

# Verificar que los archivos existen
print(f"¿Existe el directorio base? {os.path.exists(base_dir)}")
print(f"¿Existe train.csv? {os.path.exists(train_csv_path)}")
print(f"¿Existe test.csv? {os.path.exists(test_csv_path)}")

# Leer los archivos CSV
df_train = pd.read_csv(train_csv_path)
df_test = pd.read_csv(test_csv_path)

# Mostrar información básica
print("\nInformación del conjunto de entrenamiento:")
print(df_train.head())
print(f"Forma del DataFrame de entrenamiento: {df_train.shape}")

print("\nInformación del conjunto de prueba:")
print(df_test.head())
print(f"Forma del DataFrame de prueba: {df_test.shape}")

# Añadir la ruta completa a los nombres de archivo
# Asumiendo que las columnas se llaman 'file_name' en train y 'id' en test
if 'file_name' in df_train.columns:
    df_train['file_name'] = df_train['file_name'].apply(lambda x: os.path.join(base_dir, x))
if 'id' in df_test.columns:
    df_test['id'] = df_test['id'].apply(lambda x: os.path.join(base_dir, x))

# Preparar para el entrenamiento
all_image_paths = df_train['file_name'].values
all_labels = df_train['label'].values

# Dividir en train/validation (95% / 5%)
train_paths, val_paths, train_labels, val_labels = train_test_split(
    all_image_paths,
    all_labels,
    test_size=0.05,
    random_state=seed,
    shuffle=False
)

print(f"\nTrain Data: {len(train_paths)}")
print(f"Validation Data: {len(val_paths)}")

# Verificar la distribución de las etiquetas
print(f"\nDistribución de etiquetas en datos de entrenamiento:")
unique, counts = np.unique(train_labels, return_counts=True)
for u, c in zip(unique, counts):
    print(f"  Clase {u}: {c} imágenes ({c/len(train_labels)*100:.2f}%)")

print(f"\nDistribución de etiquetas en datos de validación:")
unique, counts = np.unique(val_labels, return_counts=True)
for u, c in zip(unique, counts):
    print(f"  Clase {u}: {c} imágenes ({c/len(val_labels)*100:.2f}%)")
