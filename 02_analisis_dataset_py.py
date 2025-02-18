import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración de directorios
output_dir = "graficos_indicadores"
os.makedirs(output_dir, exist_ok=True)

# Eliminar imágenes existentes en la carpeta
for archivo in os.listdir(output_dir):
    ruta_archivo = os.path.join(output_dir, archivo)
    if os.path.isfile(ruta_archivo):
        os.remove(ruta_archivo)

# Nombre del archivo
archivo_excel = "DB_compensacion_py.xlsx"

# Verificar si el archivo existe
if not os.path.exists(archivo_excel):
    print(f"El archivo '{archivo_excel}' no existe. Asegúrate de generar el dataset primero.")
    exit()

# Cargar el dataset
df = pd.read_excel(archivo_excel)

# Convertir fechas
df["Fecha Ingreso"] = pd.to_datetime(df["Fecha Ingreso"])
df["Año Ingreso"] = df["Fecha Ingreso"].dt.year

# Función para guardar gráficos
def guardar_grafico(fig, nombre):
    ruta = os.path.join(output_dir, nombre)
    fig.savefig(ruta)
    print(f"📊 Gráfico guardado: {ruta}")

### **Indicadores Clave**

# 1️⃣ Total de empleados
total_empleados = df.shape[0]
print(f"Total de empleados: {total_empleados}")

# 2️⃣ Distribución de género
genero_counts = df["Género"].value_counts()
fig, ax = plt.subplots()
ax.pie(genero_counts, labels=genero_counts.index, autopct="%.1f%%", colors=["blue", "pink"], startangle=90)
ax.set_title("Distribución de Género")
guardar_grafico(fig, "distribucion_genero.png")

# 1️⃣ Costo laboral por área
costo_laboral_area = df.groupby("Área")["Salario"].sum().sort_values(ascending=False)
fig, ax = plt.subplots()
costo_laboral_area.plot(kind="bar", ax=ax, color='skyblue')
ax.set_title("Costo Laboral por Área")
ax.set_ylabel("Salario Total ($)")
ax.set_xlabel("Área")
plt.xticks(rotation=45)
guardar_grafico(fig, "costo_laboral_area.png")

# 2️⃣ Distribución salarial por género
salario_genero = df.groupby("Género")["Salario"].describe()
fig, ax = plt.subplots()
salario_genero["mean"].plot(kind="bar", ax=ax, color=['pink', 'blue'])
ax.set_title("Distribución Salarial por Género")
ax.set_ylabel("Salario Promedio ($)")
guardar_grafico(fig, "salario_genero.png")

# 3️⃣ Rotación salarial
rotacion_salarial = df.groupby("Estado")["Salario"].mean()
fig, ax = plt.subplots()
rotacion_salarial.plot(kind="bar", ax=ax, color=['green', 'red'])
ax.set_title("Rotación Salarial")
ax.set_ylabel("Salario Promedio ($)")
guardar_grafico(fig, "rotacion_salarial.png")

# 4️⃣ Indicador de crecimiento
empleados_ultimos_5_anios = df[df["Año Ingreso"] >= (df["Año Ingreso"].max() - 5)].shape[0]
total_empleados = df.shape[0]
indicador_crecimiento = empleados_ultimos_5_anios / total_empleados * 100

fig, ax = plt.subplots()
ax.pie([indicador_crecimiento, 100 - indicador_crecimiento], labels=["Últimos 5 años", "Anteriores"], autopct="%.1f%%", colors=["blue", "gray"])
ax.set_title("Indicador de Crecimiento")
guardar_grafico(fig, "indicador_crecimiento.png")

### **Indicadores Calculados**

# 5️⃣ Promedio de salario por cargo
salario_por_cargo = df.groupby("Cargo")["Salario"].mean().sort_values()
fig, ax = plt.subplots()
salario_por_cargo.plot(kind="barh", ax=ax, color='purple')
ax.set_title("Salario Promedio por Cargo")
ax.set_xlabel("Salario Promedio ($)")
guardar_grafico(fig, "salario_por_cargo.png")

# 6️⃣ Distribución de salario en las áreas
distribucion_salario_area = df.groupby("Área")["Salario"].describe()

# 7️⃣ Análisis de equidad interna
equidad_interna = df.groupby(["Área", "Cargo"])["Salario"].mean()

# 8️⃣ Equidad salarial entre hombres y mujeres
brecha_salarial = df.groupby("Género")["Salario"].mean()

fig, ax = plt.subplots()
colors = ['blue', 'pink']
brecha_salarial.plot(kind="bar", ax=ax, color=colors)

# Anotaciones para mostrar los valores exactos
for i, salario in enumerate(brecha_salarial):
    ax.text(i, salario + (salario * 0.02), f"${salario:,.0f}", ha='center', fontsize=10, fontweight="bold")

# Diferencia salarial
diff = brecha_salarial.max() - brecha_salarial.min()
ax.annotate(f"Diferencia: ${diff:,.0f}", 
            xy=(0.5, brecha_salarial.max()), 
            xytext=(0.5, brecha_salarial.max() + (brecha_salarial.max() * 0.05)), 
            arrowprops=dict(facecolor='red', arrowstyle="->"),
            ha='center', fontsize=10, fontweight="bold", color='red')

ax.set_title("Brecha Salarial entre Géneros")
ax.set_ylabel("Salario Promedio ($)")

guardar_grafico(fig, "brecha_salarial.png")


### **Indicadores Sugeridos**

# 9️⃣ Nivel educativo por género
nivel_educativo_genero = df.groupby(["Género", "Nivel Educativo"]).size().unstack()
fig, ax = plt.subplots()
nivel_educativo_genero.plot(kind="bar", ax=ax)
ax.set_title("Nivel Educativo por Género")
ax.set_ylabel("Cantidad de Empleados")
guardar_grafico(fig, "nivel_educativo_genero.png")

# 🔟 Relación entre edad y salario
relacion_edad_salario = df.groupby("Edad")["Salario"].mean()
fig, ax = plt.subplots()
ax.scatter(relacion_edad_salario.index, relacion_edad_salario.values, color='orange')
ax.set_title("Relación entre Edad y Salario")
ax.set_xlabel("Edad")
ax.set_ylabel("Salario Promedio ($)")
guardar_grafico(fig, "relacion_edad_salario.png")

# 1️⃣1️⃣ Tipos de contrato con años de experiencia
contrato_experiencia = df.groupby("Tipo de Contrato")["Años de Experiencia"].mean()
fig, ax = plt.subplots()
contrato_experiencia.plot(kind="bar", ax=ax, color='brown')
ax.set_title("Años de Experiencia por Tipo de Contrato")
ax.set_ylabel("Experiencia Promedio (años)")
guardar_grafico(fig, "contrato_experiencia.png")

# 1️⃣2️⃣ Distribución de empleados por fondo
empleados_por_fondo = df["Fondo de Pensión"].value_counts()
fig, ax = plt.subplots()
empleados_por_fondo.plot(kind="bar", ax=ax, color='gray')
ax.set_title("Distribución de Empleados por Fondo Pensiones")
ax.set_ylabel("Edad")
guardar_grafico(fig, "empleados_por_fondo.png")

print("✅ Análisis completado y gráficos generados en la carpeta 'graficos_indicadores'.")
