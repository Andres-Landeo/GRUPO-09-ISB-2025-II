# **Reporte de laboratorio 7 - Filtrado Wavelet**

# **1. Introducción**

<p align="justify">
  El electrocardiograma (ECG) es una señal biopotencial que refleja la actividad eléctrica del corazón. Debido a su baja amplitud (del orden de milivoltios), está sujeta a interferencias externas como ruido muscular, deriva de la línea base y acoplamiento de la red eléctrica (60 Hz). Estos factores pueden distorsionar las ondas P, QRS y T, complicando su interpretación clínica.
</p>

<p align="justify">
  Para mitigar dichos efectos, se requiere un método de filtrado que elimine el ruido sin alterar la morfología cardíaca. En los últimos años, la Transformada Wavelet Discreta (DWT) se ha consolidado como una herramienta eficaz para este propósito, gracias a su capacidad de analizar señales no estacionarias en diferentes niveles de resolución. Esto permite separar las componentes de baja frecuencia (información fisiológica) de las de alta frecuencia (ruido) de forma eficaz [1] [2].
</p>


# **2. Objetivos**

## **2.1 Objetivo general:**

<p align="justify">
  Aplicar la Transformada Wavelet Discreta (DWT) para el filtrado de señales biomédicas (ECG, EMG y EEG), evaluando su capacidad para eliminar ruido y preservar la morfología fisiológica característica de cada tipo de señal.
</p>

## **2.2 Objetivos específicos:**


<p align="justify">

  - Definir los parámetros de descomposición y umbralización más adecuados según el contenido espectral de cada señal.
  
  - Implementar el filtrado DWT con la wavelet elegida para cada tipo de señal biomédica.
  
  - Evaluar la efectividad del filtrado mediante la comparación entre la señal original y la reconstruida.
  
  - Analizar y discutir la calidad del filtrado en función de la morfología conservada y la reducción de ruido.
</p>


# **3. Procedimiento: Diseño del filtro**

## **3.1 Filtrado Wavelet ECG**

## **3.1.1 Selección de la familia wavelet**

<p align="justify">
  Se seleccionó la Daubechies 4 (db4) como wavelet madre por ser una de las más utilizadas en el procesamiento de señales ECG. Su forma asimétrica y su soporte compacto permiten una excelente localización temporal, lo cual es esencial para capturar los picos del complejo QRS sin distorsionar las ondas P y T.
</p>

<p align="justify">
  Artículos que respaldan la elección:
</p>

<p align="justify">
  - Abdou et al. (2024) [1] compararon distintas familias de wavelet para ECG de un solo canal y concluyeron que db4 ofrece una mejor preservación morfológica frente a db6.  
</p>

<p align="justify">
  - Chandra et al. (2021) [2] implementaron un filtro adaptativo de alta velocidad basado en wavelets y comprobaron que db4 proporciona una mayor estabilidad temporal en el denoising de señales biomédicas.  
</p>

<p align="justify">
  - Akkaya et al. (2025) [3] destacaron que la db4 sigue siendo una de las wavelets más efectivas para señales no estacionarias por su equilibrio entre suavizado y resolución temporal.
</p>

<p align="justify">
  - Yusuf et al. (2020) [4] demostraron que la combinación de filtros Butterworth y wavelets Daubechies, particularmente db4, mejora significativamente la SNR en el preprocesamiento de señales ECG contaminadas con ruido.  
</p>

<p align="justify">
  - Xie et al. (2025) [5] propusieron un algoritmo de umbral adaptativo basado en análisis wavelet, validando que db4 permite una reducción de ruido más efectiva que métodos convencionales de filtrado.  
</p>


## **3.1.2 Parámetros definidos**

| Parámetro | Valor | Justificación |
|------------|--------|---------------|
| **Familia wavelet** | Daubechies 4 (db4) | Forma similar al QRS y excelente localización temporal |
| **Tipo de transformada** | Discrete Wavelet Transform (DWT) | Ideal para señales no estacionarias como el ECG |
| **Nivel de descomposición** | 4 niveles | Equilibrio adecuado entre la supresión de interferencias y la preservación de la morfología cardíaca |
| **Tipo de umbral** | Soft | Evita discontinuidades en la reconstrucción |
| **Valor de umbral** | 0.1 (experimental) | Ajuste que equilibra suavizado y preservación de picos |
| **Reconstrucción** | `pywt.waverec()` | Combina coeficientes umbralizados para recuperar la señal filtrada |

### **Justificación del número de niveles**

<p align="justify">
  Con una frecuencia de muestreo de 1000 Hz, una descomposición en cuatro niveles permite aislar las bandas relevantes:
</p>

- **D1–D2:** componentes de alta frecuencia, donde predominan el ruido de línea eléctrica y los artefactos musculares.  
- **D3–D4:** energía principal del complejo QRS, que contiene la información morfológica más relevante del ECG.  
- **A4:** componentes de baja frecuencia, que incluyen las ondas P, T y la deriva de línea base.   

<p align="justify">
  Esta configuración de cuatro niveles ofrece un equilibrio adecuado entre la supresión de interferencias y la preservación de la morfología cardíaca. La descomposición en cuatro niveles mediante la wavelet db4 permite eliminar eficazmente la interferencia de red eléctrica y el ruido de alta frecuencia sin alterar la forma del complejo QRS, mostrando una mejora significativa en la correlación y en la relación señal-ruido respecto a filtros convencionales [6].
</p>

## **3.2 Filtrado Wavelet EEG**

## **3.2.1 Selección de la familia wavelet**

<p align="justify">
Se utiliza Daubechies 6 porque combina buena resolución temporal y frecuencial, estabilidad numérica, semejanza con la forma de las ondas EEG y una longitud de filtro adecuada para captar los diferentes ritmos cerebrales sin distorsionar la señal.
</p>

## **3.2.2 Parámetros definidos**

| Parámetro | Valor | Justificación |
|------------|--------|---------------|
| **Familia wavelet** | Daubechies 6 (db6) | Presenta una forma de onda similar a los patrones EEG (oscilaciones suaves y transitorias), con buena localización temporal y frecuencial. Ofrece equilibrio entre resolución y suavidad, ideal para aislar ritmos cerebrales (δ, θ, α, β, γ). |
| **Tipo de transformada** | Discrete Wavelet Transform (DWT) | Permite analizar la señal EEG, que es no estacionaria, con resolución variable en tiempo y frecuencia, captando transitorios de actividad neuronal. |
| **Nivel de descomposición** | 5 niveles | Permite separar bandas de frecuencia asociadas a los ritmos cerebrales: A5 (δ), D5 (θ), D4 (α), D3 (β), D2–D1 (γ), manteniendo la coherencia espectral de la señal. |
| **Tipo de umbral** | Soft | Suaviza los coeficientes pequeños eliminando ruido sin introducir discontinuidades, preservando la forma de las oscilaciones EEG. |
| **Valor de umbral** | 0.1 (experimental) | Ajuste empírico que logra atenuar artefactos de bajo nivel (como parpadeos o ruido muscular) sin afectar la potencia relativa de las bandas EEG. |
| **Reconstrucción** | `pywt.waverec()` | Reconstruye la señal EEG a partir de los coeficientes umbralizados, conservando la morfología original y reduciendo componentes espurios.|

### **Justificación del número de niveles**

<p align="justify">
  Con una frecuencia de muestreo de 256 Hz, una descomposición en cinco niveles permite aislar las bandas de frecuencia más relevantes del EEG, asociadas a distintos estados cognitivos y de actividad cerebral:

  - **D1–D2**: componentes de alta frecuencia (32–128 Hz), donde predominan el ruido eléctrico, artefactos musculares (EMG) y actividad gamma residual.

  - **D3**: rango beta (16–32 Hz), relacionado con la actividad mental y concentración, presente durante tareas cognitivas como la resta mental.

  - **D4**: rango alfa (8–16 Hz), vinculado con estados de relajación o cierre ocular.

  - **D5**: rango theta (4–8 Hz), asociado con procesos de memoria y atención sostenida.

  - **A5**: rango delta (0–4 Hz), correspondiente a actividades de baja frecuencia y potenciales lentos corticales.
</p>

<p align="justify">
  Esta configuración de cinco niveles ofrece un equilibrio entre la separación efectiva de bandas cerebrales y la preservación de la morfología temporal de la señal EEG.
  La descomposición mediante la wavelet Daubechies 6 (db6) permite aislar las oscilaciones características de cada ritmo cerebral, reduciendo artefactos de alta frecuencia sin perder información significativa en los dominios alfa y beta.
  Este enfoque mejora la resolución tiempo-frecuencia y la interpretación neurofisiológica frente a filtros convencionales.
</p>

# **4. Resultados** 

## **4.1 Resultados - filtrado de ECG**

## **4.1.1 Filtrado - coeficientes y aproximación**

### **ECG Post ejercicio - coeficientes y aproximación**

<p align="center">
  <img src="Resultados/ECG_1_coeficientes.png">
</p>

### **ECG Reposo - coeficientes y aproximación**
<p align="center">
  <img src="Resultados/ECG_2_coeficientes.png">
</p>

## **4.1.2 Reconstrucción de las señales ECG**

### **ECG Post ejercicio - recontrucción**
<p align="center">
  <img src="Resultados/ECG_1_reconstruida.png">
</p>

### **ECG Reposo - recontrucción**
<p align="center">
  <img src="Resultados/ECG_2_reconstruida.png">
</p>

## **4.2 Resultados - filtrado de EEG**

## **4.2.1 Filtrado - coeficientes y aproximación**

### **EEG Resta mental - coeficientes y aproximación**
<p align="center">
  <img src="Resultados/EEG_coeficientes.png">
</p>

### **EEG Resta mental- recontrucción**
<p align="center">
  <img src="Resultados/EEG_reconstruida.png">
</p>

## **4.3 Resultados - filtrado de EMG**

## **4.3.1 Filtrado - coeficientes y aproximación**

### **EMG Elevación trapecio - coeficientes y aproximación**

<p align="center">
  <img src="Resultados/EMG1_coeficientes.png">
</p>

### **EMG Reposo - coeficientes y aproximación**
<p align="center">
  <img src="Resultados/EMG_reposo_coeficientes.png">
</p>

## **4.3.2 Reconstrucción de las señales EMG**

### **EMG Post ejercicio - recontrucción**
<p align="center">
  <img src="Resultados/EMG1_reconstruida.png">
</p>

### **EMG Reposo - recontrucción**
<p align="center">
  <img src="Resultados/EMG_reposo_reconstruida.png">
</p>

## **5. Discusión**

### **5.1 Filtrado Wavelet ECG**

<p align="justify">
  En los resultados de la DWT aplicada a las señales ECG post-ejercicio y reposo, se observa una buena separación de los componentes frecuenciales al descomponerlos en cuatro niveles con la wavelet db4. En ambos casos, los coeficientes de detalle D1 y D2 capturan principalmente el ruido de alta frecuencia y artefactos, mientras que los niveles D3 y D4 concentran la energía característica del complejo QRS. La componente de aproximación (A4) conserva las bajas frecuencias asociadas a las ondas P, T y la línea base.
</p>

<p align="justify">
  En la señal ECG post-ejercicio, hay una mayor variación entre amplitud y frecuencia, lo que va de acuerdo al incremento del ritmo cardíaco. A pesar de esto, la señal reconstruida mantiene una forma casi idéntica a la original, conservando la forma del complejo QRS y las ondas P y T, lo cual significa que se tiene un buen filtrado. Además, al superponer la señal original y la reconstruida se ve una alineación , con lo cual se evidencia que el filtrado eliminó de forma eficaz el ruido sin distorsionar la señal útil.
</p>

<p align="justify">
  En la señal ECG reposo, el resultado muestra una línea de base más estable y una forma más definida entre picos (intervalos RR), con lo cual se confirma la eficiencia del filtrado para reducir artefactos y atenuar fluctuaciones residuales. La señal reconstruida también mantiene las proporciones temporales entre las ondas y la amplitud característica del complejo QRS, lo que indica que se mantiene la información fisiológica importante.
</p>

<p align="justify">
  En general, los resultados confirman que la descomposición en cuatro niveles con la wavelet Daubechies 4 (db4) brinda un equilibrio óptimo entre la supresión de ruido y la conservación de la morfológica del ECG, tanto en condiciones de reposo como post-ejercicio. Esto demuestra que este método de filtrado da una alta relación señal-ruido (SNR) y preserva la integridad del complejo QRS, reforzando lo descrito en la literatura.
</p>

### **5.2 Filtrado Wavelet EEG**

<p align="justify">
La aplicación de la DWT con Daubechies 6 (db6) permitió separar eficazmente las bandas de frecuencia características del EEG en cinco niveles.
Los coeficientes D1–D2 corresponden al ruido y artefactos musculares, mientras que D3, D4 y D5 reflejan las bandas beta, alfa y theta, asociadas a procesos cognitivos.
</p>

<p align="justify">
Durante la tarea de resta mental, se observa un aumento en la energía de la banda beta (D3), vinculada a la actividad cortical y concentración, junto con una ligera disminución de las bandas alfa y theta, indicativa de mayor carga mental.
</p>

<p align="justify">
La señal reconstruida mantiene la morfología temporal original, evidenciando un filtrado adecuado sin pérdida de información relevante.
</p>

<p align="justify">
En conjunto, los resultados muestran que la wavelet db6 ofrece un equilibrio entre eliminación de ruido y preservación de ritmos cerebrales, permitiendo analizar con claridad la actividad neuronal durante procesos cognitivos.
</p>

### **5.3 Filtrado Wavelet EMG**

<p align="justify">
  En las EMG del trapecio (reposo y elevación) la descomposición DWT con db5 en 5 niveles separa la señal de forma coherente con la fisiología y con el contenido espectral típico de sEMG. Con Fs≈1 kHz, los detalles D1–D2 recogen sobre todo ruido fino y artefactos de alta frecuencia. Por otro lado, los D3–D4 concentran la actividad mioeléctrica útil donde aparecen los “bursts” del trapecio. Finalmente la aproximación A5 retiene muy baja frecuencia (deriva de electrodos/movimiento). En tus figuras esto se ve claro: D1–D2 tienen amplitud baja salvo en los bordes.

<p align="justify">
  En la señal EMG de elevación del trapecio, se aprecia que en D3–D5 hay paquetes de energía alineados con los picos de la señal original; la reconstruida resalta esos bursts y reduce el “grano” entre ellos. Por otro lado, La amplitud relativa y el timing de los bursts se preservan en vez de correrse o ensancharse, lo que sugiere un umbralado suave y una adecuada selección de wavelet, ya que db4 / sym4 son casi simétricos. Finalmente, el fondo entre los burst baja a casi 0, mejorando el SNR sin aplanar los picos. Si hubo red de 50/60 Hz, parte cae en D4; aplicar umbral algo mayor solo en D4 o combinar con tu notch IIR ayuda a dejar mínima interferencia residual [7].
</p>

<p align="justify">
  En la señal EMG en reposo, vemos que la señal reconstruida queda casi nula entre 1–9 s con pequeños restos solo en cambios bruscos: eso indica que el umbralado limpió el ruido de alta frecuencia (D1–D2) y artefactos ligeros en D3–D4 sin detectar falsa actividad muscular. El aumento final que se aprecia es debido al origen de la señal, puesto que en ese preciso instante se empezó a realizar el movimiento de flexión. Fue algo inherente a la señal y es una limitante con la cual se trabajo durante todo el laboratorio, la nula estándarización de señales. La señal de reposo obtuvo un alto CNR y una base limpia para comparar con la contracción [8].
</p>

<p align="justify">
  En conclusión, el análisis de la señal EMG del trapecio mediante la transformada wavelet (DWT con db5) demostró ser una herramienta altamente efectiva. Logró separar los componentes de la señal de manera coherente con la fisiología muscular: aisló el ruido en los niveles D1-D2, capturó la actividad muscular útil en los niveles D3-D4, y la deriva de baja frecuencia en A5. La reconstrucción de la señal mejoró significativamente la relación señal-ruido, preservando con precisión la amplitud y el timing de los "bursts" de contracción mientras suprimía casi por completo el ruido de fondo. Esto permitió una clara distinción entre los periodos de reposo y actividad, validando la elección de la wavelet y la estrategia de umbralizado para el procesamiento de señales EMG.

# **6. Referencias**

[1] A. Abdou et al., “Enhancement of single-lead dry-electrode ECG through wavelet,” *Frontiers in Signal Processing*, vol. 3, 2024. doi:10.3389/frsip.2024.1396077.

[2] M. Chandra, S. Mishra, and D. Patnaik, “Design and analysis of improved high-speed adaptive filter for biomedical signal denoising using wavelets,” *Biomedical Signal Processing and Control*, vol. 68, p. 102774, 2021. doi:10.1016/j.bspc.2020.102221.

[3] S. Akkaya, M. Kose, and O. Bayat, “Wavelet-Based Denoising Strategies for Non-Stationary Signals,” *Electronics*, vol. 14, no. 16, p. 3190, 2025. doi:10.3390/electronics14163190.

[4] S. D. Yusuf, F. C. Maduakolam, I. Umar, and A. Z. Loko, “Analysis of Butterworth filter for electrocardiogram de-noising using Daubechies wavelets,” *SSRG International Journal of Electronics and Communication Engineering*, vol. 7, no. 4, pp. 8–13, 2020.  

[5] H. Xie, J. Jiang, Z. Zhao, and J. Peng, “Thresholding noise reduction algorithm for ECG signals based on wavelet analysis,” in *Proc. 2025 5th Int. Conf. Autom. Control, Algorithm and Intell. Bionics*, pp. 507–513, 2025. doi:10.1145/3760269.3760349.

[6] M. J. Rodenas-Herraiz, A. Garcia-Rodriguez, and A. Alcaraz, “An Efficient Algorithm Based on Wavelet Transform to Reduce Powerline Noise From Electrocardiograms,” arXiv preprint, 2024. doi:10.48550/arXiv.2401.10694.

[7] C. Ouyang, L. Cai, B. Liu, *et al*., “An improved wavelet threshold denoising approach for surface electromyography signal,” *EURASIP Journal on Advances in Signal Processing*, vol. 2023, no. 1, **Art. no. 108**, 2023, doi: 10.1186/s13634-023-01066-3.

[8] M. Boyer, L. Bouyer, J. S. Roy, and A. Campeau-Lecours, “Reducing Noise, Artifacts and Interference in Single-Channel EMG Signals: A Review,” Sensors, vol. 23, no. 6, Art. no. 2927, 2023, doi: 10.3390/s23062927