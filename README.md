
# BIAS - Behavioral Intelligence Analysis System

## Descripción

BIAS (Behavioral Intelligence Analysis System) es un sistema diseñado para la evaluación de perfiles de riesgo de radicalización, con el objetivo de prevenir situaciones extremistas y violentas a través de un análisis detallado de factores conductuales, sociales, psicológicos y contextuales.

## Cómo ejecutar la aplicación

1. **Clona el repositorio**:
    ```
    git clone https://github.com/CristinaVano/behavioral-intelligence.git
    ```

2. **Instalar dependencias**:
    Ejecuta el siguiente comando en tu terminal para instalar las librerías necesarias:
    ```
    pip install -r requirements.txt
    ```

3. **Ejecutar la aplicación**:
    Para correr la app localmente:
    ```
    streamlit run app.py
    ```

4. **Acceder a la app**:
    - Al ejecutar la app, accede con el usuario **`demo_bias`** para ver el informe genérico.
    - Si eres **`JuanCarlos_bias`** o **`Cristina_bias`**, podrás acceder al **informe detallado** con puntuaciones.

## Usuarios de prueba

- **Usuario:** `demo_bias`  
  **Contraseña:** `biasdemo2025`  
  *Este usuario solo puede generar el informe básico.*
  
- **Usuario:** `JuanCarlos_bias`  
  **Contraseña:** `admin_bias`  
  *Este usuario puede generar el informe detallado y el básico.*

- **Usuario:** `Cristina_bias`  
  **Contraseña:** `admin_bias`  
  *Este usuario puede generar el informe detallado y el básico.*

## Requisitos

- Python 3.x
- Streamlit
- FPDF
- Pandas
- NumPy
- Scikit-learn

## Licencia

MIT License.
