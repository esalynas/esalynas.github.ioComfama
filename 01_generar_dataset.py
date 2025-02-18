import os
import pandas as pd
import random
from faker import Faker
import subprocess

# Configurar Faker para datos en español
fake = Faker('es_CO')

# Definir listas de valores posibles
generos = ["Masculino", "Femenino"]
cargos = ["Analista", "Gerente", "Coordinador", "Asistente", "Director"]
departamentos = ["Recursos Humanos", "Finanzas", "IT", "Ventas", "Operaciones"]
areas = ["Administrativa", "Técnica", "Comercial"]
niveles_educativos = ["Bachillerato", "Técnico", "Tecnólogo", "Universitario", "Postgrado"]
tipos_contrato = ["Indefinido", "Fijo", "Prestación de servicios", "Aprendizaje"]
eps = ["Sanitas", "Sura", "Nueva EPS", "Salud Total", "Compensar"]
cajas_compensacion = ["Cafam", "Colsubsidio", "Compensar", "Comfama", "Comfenalco"]
fondos_pension = ["Porvenir", "Protección", "Colfondos", "Skandia", "Colpensiones"]

# Nombre del archivo
archivo_excel = "DB_compensacion_py.xlsx"

# Verificar si el archivo ya existe
if os.path.exists(archivo_excel):
    print(f"El archivo '{archivo_excel}' ya existe. No se generará uno nuevo.")
else:
    # Generar datos ficticios
    def generar_datos(n=5000):
        data = []
        for _ in range(n):
            cedula = fake.unique.random_int(min=10000000, max=99999999)
            nombre = fake.name()
            genero = random.choices(["Masculino", "Femenino"], weights=[0.55, 0.45])[0]  # Más hombres
            edad = random.randint(18, 65)
            residencia = fake.city()
            fecha_ingreso = fake.date_between(start_date="-20y", end_date="today")
            estado = random.choice(["Activo", "Inactivo"])
            
            # Salario desigual
            if genero == "Femenino":
                salario = round(random.uniform(1200000, 8000000), -3)  # Menor salario
            else:
                salario = round(random.uniform(2000000, 15000000), -3)
            
            cargo = random.choice(cargos)
            departamento = random.choice(departamentos)
            area = random.choices(["Administrativa", "Técnica", "Comercial"], weights=[0.3, 0.3, 0.4])[0]
            
            # Salario más alto en cargos gerenciales y en ventas
            if cargo in ["Gerente", "Director"] or area == "Comercial":
                salario = max(salario, round(random.uniform(8000000, 15000000), -3))
            
            nivel_educativo = random.choice(niveles_educativos)
            experiencia = random.randint(0, 40)
            
            # Tipos de contrato sesgados
            if cargo == "Asistente":
                tipo_contrato = random.choices(tipos_contrato, weights=[0.1, 0.2, 0.6, 0.1])[0]  # Más prestación de servicios
            elif edad <= 22:
                tipo_contrato = "Aprendizaje"  # Más contratos de aprendizaje en jóvenes
            else:
                tipo_contrato = random.choice(tipos_contrato)
            
            eps_seleccionada = random.choice(eps)
            caja_compensacion = random.choice(cajas_compensacion)
            
            # Mayores afiliados a Colpensiones
            if edad > 50:
                fondo_pension = "Colpensiones"
            else:
                fondo_pension = random.choice(fondos_pension[:-1])  # Excluye Colpensiones

            data.append([
                cedula, nombre, genero, edad, residencia, fecha_ingreso, estado, salario, 
                cargo, departamento, area, nivel_educativo, experiencia, tipo_contrato, 
                eps_seleccionada, caja_compensacion, fondo_pension
            ])

        return pd.DataFrame(data, columns=[
            "Cédula", "Nombre", "Género", "Edad", "Residencia", "Fecha Ingreso", "Estado", "Salario",
            "Cargo", "Departamento", "Área", "Nivel Educativo", "Años de Experiencia", "Tipo de Contrato",
            "EPS", "Caja de Compensación", "Fondo de Pensión"
        ])

    # Crear y guardar el dataset
    df = generar_datos()
    df.to_excel(archivo_excel, index=False)

    print(f"Dataset generado y guardado como '{archivo_excel}'.")

    # Ejecutar el siguiente script
script_analisis = "02_analisis_dataset_py.py"
if os.path.exists(script_analisis):
    print(f"Ejecutando '{script_analisis}'...")
    subprocess.run(["python", script_analisis], check=True)
else:
    print(f"El archivo '{script_analisis}' no se encuentra en el directorio.")
