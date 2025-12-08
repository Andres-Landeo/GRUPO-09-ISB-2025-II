# **Clasificador de señal EMG para reconocer la correcta ejecución del ejercicio de levantar pesas en adultos**

## **Resumen**
Desarrollo de un sistema de monitoreo basado en señales EMG y la técnica de bosque aleatorio para clasificar la ejecución correcta o incorrecta durante ejercicios de levantamiento de pesas. Utilizando señales electromiográficas de músculos clave como el bíceps y deltoides, el sistema analiza la activación muscular y la fatiga para identificar patrones de mala técnica.

## **Palabras clave**
Machine learning, aprendizaje por computadora, random forest, árboles de decisión, fisioterapia, electromiografía.

---

## **1. Introducción**
El ejercicio de levantamiento de pesas es bastante utilizado en fisioterapia y entrenamiento funcional debido a su accesibilidad y beneficios para la salud musculoesquelética. Sin embargo, incluso con cargas bajas, el volumen repetitivo de movimientos puede inducir fatiga neuromuscular, lo cual es un indicador de una mala ejecución puesto que altera el patrón normal de activación en músculos como el bíceps y los deltoides. Además, esta alteración favorece compensaciones y desajustes técnicos que elevan el riesgo de lesiones por sobreuso, especialmente en hombros y región lumbar [1].

Estudios recientes muestran que en actividades de levantamiento de pesas, las zonas más afectadas por lesiones son la zona lumbar (23–31%) y los hombros (11–17%), lo cual deja clara la importancia de supervisar la técnica de ejecución aun cuando se tienen condiciones controladas o recreativas [1]. A pesar de ello, la evaluación tradicional de la técnica se sigue realizando de forma visual y depende del criterio humano, con lo cual se tienen limitaciones para identificar errores sutiles o patrones de fatiga temprana.

La electromiografía superficial (EMG) permite medir objetivamente la activación muscular en tiempo real, lo que permite ofrecer una alternativa precisa y no invasiva para evaluar la calidad del movimiento. La literatura demuestra que características como RMS, iEMG, MNF y MDF pueden capturar cambios relevantes asociados al esfuerzo y la fatiga muscular [2], [3].

De acuerdo a este contexto, el presente proyecto busca desarrollar un sistema de clasificación basado en machine learning para diferenciar ejecuciones correctas e incorrectas durante el levantamiento de pesas, empleando características derivadas de señales EMG.

---

## **2. Antecedentes**
Las técnicas de ML existen desde (), e incluyen a las de deep learning o IA que comenzaron su desarrollo en (). Estas técnicas consisten en la generación de una lógica de procesamiento de información con mínima intervención humana, ya sea por métodos iterativos, estadísticos, o combinados. Mientras que las técnicas de machine learning clásico dan énfasis al uso de herramientas estadísticas y conceptos como la entropía de la información para la creación de algoritmos de aprendizaje automatizado, las de deep learning se basan en el uso de redes neuronales para el mismo propósito, simplificando aún más el proceso al reducir la necesidad de diseño de algoritmos.

Por ello, las técnicas de deep learning o IA, al usar redes neuronales que permiten elevadas cantidades de permutaciones y cambios en la comunicación entre nodos, tienen la propiedad de ser generalizables a cualquier contexto, y en la actualidad han mostrado mucho potencial con los métodos iterativos de aprendizaje al detectar grandes cantidades de patrones poco reconocibles para los humanos en datos no estructurados []. Sin embargo, tienen limitaciones importantes comparadas con el ML clásico: que requiere de una elevada cantidad de recursos computacionales, que la lógica de procesamiento de información tiene visibilidad prácticamente nula para el programador, y que son sensibles al overfitting y sesgo con poca capacidad de corregirlo que no sea aumentar o modificar los datos de entrenamiento, aumentar los recursos computacionales, o limitar las capacidades de aprendizaje.

Gracias a la cantidad de recursos requeridos por los sistemas basados en deep learning, es común que se apliquen solo con computadoras poderosas y a través de la nube, lo que limita la capacidad de detección en tiempo real por el tiempo de procesamiento, el costo, o los requerimientos de conexión a la red y la latencia. Por ello, las técnicas de ML clásico son las mejor adaptadas a sistemas ligeros y en tiempo real.

La técnica de Random Forest o de bosques aleatorios se basa en la generación de un conjunto o “ensemble” de árboles de decisión, que por su parte son construidos por algoritmos que se basan en el concepto de la entropía de la información (ej.: algoritmo ). Los árboles de decisión buscan hacer particiones sucesivas de los datos de entrenamiento, minimizando la entropía cada vez. Cada vez que una partición logra la clasificación adecuada, se detienen las particiones sucesivas a esa rama del árbol, continuando hasta que se cumpla para todas las ramas. Debido a que al generalizar este algoritmo cada partición o nodo en el árbol representará un probabilidad, los árboles de decisión requieren de una aleatorización.

---

## **3. Planteamiento del problema**
A pesar de la alta prevalencia de lesiones relacionadas con ejercicios de fuerza, no existen herramientas accesibles que permitan monitorear de forma automática y en tiempo real la correcta ejecución del levantamiento de pesas. La supervisión humana puede ser subjetiva, inconsistente y difícil de mantener en sesiones no supervisadas, sobre todo en poblaciones vulnerables. Esto genera la necesidad de un sistema objetivo que evalúe la técnica a partir de biomarcadores musculares medidos mediante EMG.

---

## **4. Propuesta de solución**
Se propone un sistema basado en señales EMG y un modelo de clasificación tipo Random Forest que pueda ser capaz de distinguir entre ejecuciones correctas e incorrectas durante el levantamiento de pesas. El sistema utiliza las señales EMG de bíceps y deltoides, a partir de las cuales se extraen características temporales y espectrales. Estas características se incorporan a un modelo de machine learning entrenado para identificar patrones que estén asociados a fatiga o pérdida de control, indicadores que ayudan a identificar una incorrecta ejecución del ejercicio para posteriormente generar alertas en tiempo real.

---

## **5. Materiales y Métodos**

### **5.1 Base de datos utilizada**
Se empleó el dataset público **A Comprehensive Dataset of Surface Electromyography and Self-Perceived Fatigue Levels for Muscle Fatigue Analysis**, que contiene señales EMG de 13 participantes realizando distintos movimientos de flexión con pesos ligeros [2].  
Se registraron señales de bíceps braquial (derecho e izquierdo) y de las tres porciones del deltoides.

### **5.2 Preprocesamiento de señales EMG**
Los archivos fueron organizados por sujeto, músculo y ensayo. Posteriormente, se realizó:

- Segmentación del tramo activo de la señal.  
- Selección del canal correspondiente a cada músculo.  
- Normalización por %MVC (Maximum Voluntary Contraction), para hacer comparables señales entre sujetos y reducir variabilidad por fuerza individual o diferencias anatómicas.

### **5.3 Extracción de características**
Se calcularon:

- RMS (Root Mean Square): indica la activación promedio; se obtiene como la raíz del promedio de los cuadrados de la señal.  
- iEMG (integrated EMG): mide el esfuerzo total de la contracción; corresponde a la integral de la señal rectificada.  
- MNF (Mean Frequency): centro de gravedad espectral; disminuye con fatiga.  
- MDF (Median Frequency): frecuencia que divide la potencia espectral en dos mitades; también disminuye bajo fatiga [3].  
- Tiempos hasta los niveles de fatiga reportados en el dataset (Fatigue Level 1 y 2).

Todos estos parámetros se consolidaron en una matriz de datos lista para clasificación.

### **5.4 Entrenamiento del modelo**
- División entrenamiento/prueba: 70/30.  
- Etiquetado: basado en la media del tiempo de fatiga (alta vs. baja resistencia).  
- Modelo utilizado: Random Forest Classifier por su robustez, baja latencia y resistencia al overfitting.  
- Se evaluó la precisión, matriz de confusión y errores de clasificación.

---

## **6. Resultados**
De observación de los datos:

- La disminución en MNF y MDF indica fatiga.  
- Valores muy elevados de RMS indican descontrol.  
- Valores fuera de rango (40–90 %) en la señal relativa a MVC indican carga desequilibrada.

Del entrenamiento:

- a  
- b  
- c  
- d  
- e  
- Precisión de 73.91 %.  
- Margen de error de 6 muestras.

Los resultados obtenidos indican que las características EMG elegidas son efectivas para capturar patrones de activación y fatiga relevantes para evaluar la técnica en ejercicios de fuerza. La disminución sistemática de MNF y MDF coincide con estudios previos sobre fatiga muscular [3], mientras que las variaciones anómalas en RMS reflejan momentos de descontrol o compensación, coherentes con lo descrito en [4].

El modelo Random Forest demostró ser capaz de diferenciar ejecuciones correctas e incorrectas con un desempeño aceptable para una primera aproximación. Sin embargo, el rendimiento puede mejorar incorporando señales de mayor resolución, calibraciones individuales del MVC y técnicas de extracción de características más avanzadas.

---

## **7. Conclusiones**
- Se logró desarrollar un sistema capaz de clasificar ejecuciones correctas e incorrectas durante el levantamiento de pesas utilizando características extraídas de señales EMG.  
- La metodología implementada permite monitorear la fatiga muscular y la técnica en tiempo real.  
- Este sistema tiene potencial para aplicaciones en entrenamiento personalizado, rehabilitación y prevención de lesiones en adultos.  
- La precisión alcanzada demuestra la viabilidad del enfoque, aunque existe margen para optimizar el modelo y ampliar la base de datos.

---

## **8. Limitaciones**
- El dataset proviene de ensayos controlados, por lo cual el modelo debe validarse en usuarios reales con variaciones de técnica.  
- Las señales EMG pueden verse afectadas por sudor, desplazamiento de electrodos y ruido por movimiento.  
- Se recomienda ampliar la cantidad de sujetos, incluir protocolos estandarizados de MVC y explorar modelos adicionales como SVM o redes neuronales ligeras.

---

## **9. Referencias**
[1] M. J. Y. Tung, G. A. Lantz, A. D. Lopes, and L. Berglund, “Injuries in weightlifting and powerlifting: an updated systematic review,” BMJ Open Sport & Exercise Medicine, vol. 10, no. 4, 2024, doi: 10.1136/bmjsem-2023-001884.

[2] S. M. Cerqueira, R. Vilas Boas, J. Figueiredo, and C. P. Santos, “A comprehensive dataset of surface electromyography and self-perceived fatigue levels for muscle fatigue analysis,” Sensors, vol. 24, no. 24, p. 8081, 2024.

[3] J. Sun et al., “Application of Surface Electromyography in Exercise Fatigue,” Frontiers in Systems Neuroscience, 2022.

[4] H. M. Qassim et al., “Proposed Fatigue Index for the Objective Detection of Muscle Fatigue Using Surface Electromyography,” Sensors, vol. 22, no. 5, p. 1900, 2022.

---

## **10. Biografías de autores**
Andrés Nicolás Landeo Cruzado – Estudiante de Ingeniería Biomédica, con interés en Ingeniería Clínica, Biomecánica y procesamiento de señales e imágenes biomédicas. Busca aplicar estas técnicas en entornos clínicos y profesionales.  
Correo: andres.landeo@upch.pe

Nicolás Alejandro Vásquez Carrillo – Estudiante de Ingeniería Biomédica, interesado en áreas vinculadas al análisis de señales biomédicas y su aplicación en la atención al paciente. Motivado por comprender la complejidad de los sistemas fisiológicos y su impacto en la salud.  
Correo: nicolas.vasquez@upch.pe

Luis Fernando Galván Núñez – Estudiante de Ingeniería Biomédica, con interés en procesos de diseño, modelamiento fisiológico y tecnologías biomédicas. Enfocado en integrar conceptos teóricos con aplicaciones prácticas en ingeniería clínica.  
Correo: luis.galvan@upch.pe

Diego Fabrizio Munayco Saravia – Estudiante de Ingeniería Biomédica, con interés en biomecánica, ingeniería clínica y procesamiento de señales para aplicaciones en salud. Posee experiencia en modelado 3D y busca ampliar su dominio en análisis de señales fisiológicas.  
Correo: diego.munayco@upch.pe
