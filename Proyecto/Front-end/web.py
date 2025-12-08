import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

#------Programa principal------#
st.title("Clasificación objetiva de la técnica en levantamiento de pesas usando EMG superficial")

codigo_procesamiento="""import pandas as pd
import numpy as np
import os
import re 

# --- CONFIGURACIÓN Y CONSTANTES ---
# La ubicación base de los archivos de fatiga.
FATIGUE_DIR_BASE = 'Fatigue_index'
NUM_SUBJECTS = 13 

# Mapeo de trials que SÍ queremos procesar (5, 6, 9, 10, 11, 12)
TRIAL_MAP_FILENAMES = {
    'trial_5.csv': 'R BICEPS', 'trial_6.csv': 'L BICEPS',
    'trial_9.csv': 'R DELT ANT', 'trial_10.csv': 'L DELT ANT',
    'trial_11.csv': 'R DELT POST', 'trial_12.csv': 'L DELT POST'
}

# Nombres de los archivos
EMG_FEATURES_FILE = "EMG_All_Subjects_Features_Normalized.csv"
FATIGUE_OUTPUT_FILE = "Fatigue_Perception_Times_Subset.csv"
MERGED_OUTPUT_FILE = "EMG_Fatigue_Analysis_Subset.csv"

# --- FUNCIONES PARA EL ANÁLISIS DE FATIGA AUTOPERCIBIDA ---

def find_transition_time(data, start_label, end_label):
    # Encuentra el tiempo (en segundos) de la primera transición de start_label a end_label.
    if data.empty:
        return np.nan

    # La transición ocurre cuando la etiqueta anterior era 'start_label' 
    # y la etiqueta actual es 'end_label'.
    # Usamos .copy() para evitar SettingWithCopyWarning en .shift()
    temp_data = data.copy()
    transition = (temp_data['label'].shift(1) == start_label) & (temp_data['label'] == end_label)
    
    first_transition_index = transition[transition].index
    
    if not first_transition_index.empty:
        # Devuelve el valor de 'time' correspondiente al *primer* instante de transición
        return data.loc[first_transition_index[0], 'time']
    else:
        return np.nan

def process_fatigue_data(subject_id, trial_map_filenames):
    # Procesa los archivos de fatiga para un sujeto y extrae los tiempos de transición.

    subject_fatigue_times = []
    
    for trial_file_key in trial_map_filenames.keys():
        
        # Extraemos el número de trial (ej: de 'trial_5.csv' extraemos '5')
        match = re.search(r'trial_(\d+)\.csv', trial_file_key)
        if not match:
            continue
            
        trial_num = match.group(1) 
        
        # Construcción de la ruta del archivo de fatiga (ej: 'Trial_5.csv')
        fatigue_file_name = f'Trial_{trial_num}.csv'
        fatigue_path = os.path.join(FATIGUE_DIR_BASE, f'subject_{subject_id}', fatigue_file_name)
        
        time_to_fatigue_1 = np.nan
        time_to_fatigue_2 = np.nan
        
        if os.path.exists(fatigue_path):
            try:
                # Leer el archivo
                fatigue_data = pd.read_csv(fatigue_path, header=0, delimiter=',')
                
                # Asegurar que las columnas existan y renombrar para estandarizar
                time_col = [col for col in fatigue_data.columns if 'time' in col.lower()]
                label_col = [col for col in fatigue_data.columns if 'label' in col.lower()]
                
                if time_col and label_col:
                    fatigue_data = fatigue_data[[time_col[0], label_col[0]]]
                    fatigue_data.columns = ['time', 'label']
                    
                    # Extraer tiempos de transición
                    time_to_fatigue_1 = find_transition_time(fatigue_data, 0, 1)
                    time_to_fatigue_2 = find_transition_time(fatigue_data, 1, 2)
                
            except Exception:
                # Silenciamos errores menores si no se puede procesar un archivo
                pass
        
        # Añadir los resultados al listado
        subject_fatigue_times.append([
            f'Subject_{subject_id}', 
            trial_file_key, 
            time_to_fatigue_1, 
            time_to_fatigue_2
        ])

    return pd.DataFrame(subject_fatigue_times, 
                         columns=['Subject', 'Trial', 'Time_Fatigue_Level_1 [s]', 'Time_Fatigue_Level_2 [s]'])

# --- EJECUCIÓN MAESTRA ---

# 1. Extracción de Tiempos de Fatiga
print("="*80)
print("INICIANDO EXTRACCIÓN DE TIEMPOS DE FATIGA")
print("="*80)

FATIGUE_DATA_ALL = []
for i in range(1, NUM_SUBJECTS + 1):
    fatigue_df = process_fatigue_data(i, TRIAL_MAP_FILENAMES)
    FATIGUE_DATA_ALL.append(fatigue_df)

final_fatigue_df = pd.concat(FATIGUE_DATA_ALL, ignore_index=True)

# Guardar el archivo CSV de tiempos de fatiga
final_fatigue_df.to_csv(FATIGUE_OUTPUT_FILE, index=False)
print(f"\n Tiempos de fatiga guardados en '{FATIGUE_OUTPUT_FILE}'.")


# 2. Unificación de Datos EMG y Fatiga
print("\n" + "="*80)
print("INICIANDO UNIFICACIÓN DE DATOS EMG Y TIEMPOS DE FATIGA")
print("="*80)
try:
    # Cargar el archivo de características EMG normalizadas
    emg_df = pd.read_csv(EMG_FEATURES_FILE)
    
    # Fusionar los DataFrames por 'Subject' y 'Trial'. 
    merged_df = pd.merge(emg_df, final_fatigue_df, on=['Subject', 'Trial'], how='left')
    
    # Guardar el archivo unificado
    merged_df.to_csv(MERGED_OUTPUT_FILE, index=False)
    
    print(f" Datos de EMG y Fatiga Unificados y guardados en '{MERGED_OUTPUT_FILE}'.")
    
    # Mostrar el resultado unificado (formato de salida requerido)
    print("--- SALIDA REQUERIDA: MUESTRA DEL ARCHIVO UNIFICADO ---")
    display_cols = ['Subject', 'Trial', 'RMS (Avg) [% MVC]', 'iEMG (Avg) [V.s]', 'MNF (Avg) [Hz]', 'MDF (Avg) [Hz]', 'Time_Fatigue_Level_1 [s]', 'Time_Fatigue_Level_2 [s]']
    
    # Aseguramos el orden y formato de salida
    print(merged_df[display_cols].head(12).to_string(float_format="{:.4f}".format, index=False))
    print("...")

except FileNotFoundError:
    print(f" ERROR: No se encontró el archivo de características EMG: '{EMG_FEATURES_FILE}'. Por favor, asegúrate de que el archivo exista.")
except Exception as e:
    print(f" ERROR al intentar fusionar los datos: {e}")
"""

st.markdown("El siguiente código muestra el procesamiento de los datos de fatiga autopercibida y su unificación con las características EMG normalizadas.")
st.code(codigo_procesamiento, language='python')

st.markdown("A continuación, al cargar el documento de prueba se va mostrar los resultados del modelo de Machine Learning usado.")

st.markdown("#### En caso no disponga del documento .csv a analizar, lo puede encontrar en" \
"el repositorio con el nombre de Extracted.csv")

archivo=st.file_uploader("Subir archivo en formato .csv ", type=["csv"])
test=st.number_input("Escoger porcentaje de elementos para prueba (test size)", min_value=0.1, max_value=0.9, value=0.3, step=0.05)
if archivo is not None:
    # Codigo de ML adapatado para usarlo en front-end de Streamlit

    st.write("Tener en cuenta que el porcentaje restante es de las muestras entrenadas por el modelo (Random Forest).")
    st.markdown("###### Mostrando dataset cargado:")
    # Carga
    df = pd.read_csv(archivo,sep=';')
    df.columns = df.columns.str.strip()
    df.dropna(inplace=True)

    st.dataframe(df)

    # Creación de etiquetas
    # Usamos la mediana para definir quién se fatiga rápido (1) y quién lento (0)
    target_col = 'Time_Fatigue_Level_2 [s]'
    median_time = df[target_col].median()

    # 0: Alta Resistencia (Tiempo > Mediana)
    # 1: Baja Resistencia (Tiempo <= Mediana)
    df['Fatigue_Type'] = (df[target_col] <= median_time).astype(int)

    # Seleccionamos las variables predictoras (Features)
    features = ['RMS (Avg) [% MVC]', 'iEMG (Avg) [V.s]', 'MNF (Avg) [Hz]', 'MDF (Avg) [Hz]']
    X = df[features]
    y = df['Fatigue_Type']


    # Entrenamiento del Random Forest
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=42, stratify=y)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Predicciones
    y_pred = rf_model.predict(X_test)

    # Matriz de confusión
    # Calcular la matriz numérica
    cm = confusion_matrix(y_test, y_pred)

    # Etiquetas para la gráfica
    labels = ['Alta resistencia (0)', 'Baja resistencia (1)']

    # Configurar el gráfico
    fig,ax=plt.subplots(figsize=(6, 5))  
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=labels, 
                yticklabels=labels, annot_kws={"size": 16},ax=ax)

    ax.set_title('Matriz de confusión - Detección de fatiga', fontsize=14)
    ax.set_ylabel('Valor real', fontsize=12)
    ax.set_xlabel('Predicción del modelo', fontsize=12)
    st.pyplot(fig)

    # Métricas
    acc = accuracy_score(y_test, y_pred)
    st.metric(label="Exactitud (Precisión): ", value=f"{acc:.2%}")
    st.subheader("Interpretación de la matriz:")
    st.metric(label="- Aciertos clase 0 (Verdaderos negativos): ", value=f"{cm[0,0]}")
    st.metric(label="- Aciertos clase 1 (Verdaderos positivos): ", value=f"{cm[1,1]}")
    st.metric(label="- Errores (confusiones): ", value=f"{cm[0,1] + cm[1,0]}")

    # Reporte detallado por clase
    st.subheader("Reporte de Clasificación:")
    st.write(classification_report(y_test, y_pred, target_names=['Alta Resistencia (0)', 'Baja Resistencia (1)']))

    # Extraemos qué variables fueron más útiles para el modelo
    importances = pd.Series(rf_model.feature_importances_, index=features).sort_values(ascending=False)

    st.subheader("Importancia de las características (¿Qué tanto influyen en la fatiga?):")
    st.dataframe(importances)