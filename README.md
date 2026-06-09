# LUMIS — Sistema Experto de Skincare
# Uyaban Lorena, Lozada Harvey

Sistema basado en conocimiento que recomienda rutinas de cuidado facial personalizadas usando encadenamiento hacia adelante.

---

## ¿Por qué elegimos este proyecto?

El cuidado de la piel es un tema que afecta a millones de personas, pero la mayoría no sabe por dónde empezar: hay cientos de productos en el mercado, ingredientes con nombres difíciles y consejos contradictorios en redes sociales. Una consulta con un dermatólogo puede ser costosa o difícil de acceder.

Elegimos este dominio porque es un problema real y cotidiano, con reglas claras basadas en evidencia científica que se pueden formalizar perfectamente en un sistema experto. Además, permite demostrar el encadenamiento hacia adelante de forma muy visual: el sistema toma datos simples (tipo de piel + objetivo) y deriva recomendaciones concretas y justificadas paso a paso.

---

## Interfaz web: ¿qué es Flask y por qué lo elegimos?

**Flask** es un framework de Python para crear aplicaciones web. Un framework es como un "kit de herramientas" que ya tiene resuelto lo difícil (recibir solicitudes del navegador, enviar respuestas, manejar rutas) para que el desarrollador se concentre en la lógica del sistema.

**¿Por qué Flask y no Streamlit?**  
Elegimos Flask sobre Streamlit porque nos da control total sobre el diseño de la interfaz. Con Streamlit, la apariencia es genérica y difícil de personalizar. Flask permite crear una interfaz completamente a medida con HTML, CSS y JavaScript propio, lo que nos permitió diseñar la experiencia visual minimalista y profesional que tiene LUMIS.

---

## Instalación

```bash
# 1. Entrar a la carpeta del proyecto
cd skincare_expert

# 2. (Opcional) Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
python app.py
```

Luego abrir en el navegador: **http://localhost:5000**

---

## Estructura del proyecto

```
skincare_expert/
├── app.py                    # Servidor Flask (punto de entrada)
├── requirements.txt
├── README.md
│
├── src/
│   ├── base_conocimiento.py  # Predicados + 15 reglas de producción
│   └── motor_inferencia.py   # Motor de inferencia (encadenamiento hacia adelante)
│
├── templates/
│   └── index.html            # Interfaz web
│
├── static/
│   ├── style.css             # Estilos visuales
│   └── script.js             # Lógica del wizard y llamadas al servidor
│
├── tests/
│   └── casos_prueba.md       # 6 casos de prueba documentados
│
└── docs/
    └── documentacion.docx    # Documentación técnica y manual de usuario
```

---

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Interfaz web principal |
| POST | `/diagnosticar` | Ejecuta el motor de inferencia |
| POST | `/porque/<conclusion>` | Explica una conclusión específica |
| GET | `/predicados` | Lista todos los predicados del dominio |
| GET | `/reglas` | Lista todas las reglas de producción |

---
# Motor de Inferencia

El motor de inferencia es el cerebro del sistema. Es el componente encargado de razonar: toma los datos que el usuario ingresó (tipo de piel, objetivos, edad) y, aplicando las reglas de conocimiento, llega a conclusiones concretas sobre qué productos recomendar.

# Encadenamiento hacia adelante
La técnica que usa el motor se llama encadenamiento hacia adelante (forward chaining). El nombre describe exactamente lo que hace: parte de los hechos conocidos (lo que el usuario dijo de su piel) y avanza hacia adelante, aplicando reglas una por una, hasta derivar todas las conclusiones posibles.
El proceso funciona así:

Se cargan los hechos iniciales — por ejemplo: piel_grasa = verdadero, objetivo_anti_acne = verdadero.
Se recorren las 15 reglas — para cada regla, el motor verifica si todas sus condiciones están presentes en los hechos conocidos.
Si una regla se cumple, se dispara — sus conclusiones se agregan a los hechos conocidos. Por ejemplo, la regla R1 derivaría: usar_limpiador_acido_salicilico = verdadero, usar_niacinamida = verdadero.
Se repite el proceso — ahora con los hechos nuevos, puede que otras reglas que antes no se cumplían ahora sí se cumplan. El motor sigue iterando hasta que no haya ningún cambio nuevo (a esto se le llama punto fijo).

La diferencia con el encadenamiento hacia atrás es que ese parte de una conclusión y busca si hay hechos que la justifiquen. El encadenamiento hacia adelante es más adecuado para sistemas de recomendación, donde el objetivo es descubrir todo lo que se puede concluir a partir de lo que el usuario informa.


---

## Glosario de términos

Este glosario explica los ingredientes y conceptos que el sistema recomienda, en palabras sencillas.

| Término | ¿Qué es? |
|---------|----------|
| **Ácido hialurónico** | Molécula que la piel produce naturalmente y que retiene la humedad como una esponja. En productos, se usa en sueros para dar hidratación profunda. |
| **Ácido salicílico** | Ingrediente que penetra dentro del poro y lo limpia por dentro, reduciendo granos, espinillas y puntos negros. Ideal para piel grasa. |
| **Niacinamida** | Vitamina B3 que regula el exceso de grasa, minimiza los poros y pareja el tono de la piel. Es uno de los ingredientes más seguros y bien tolerados. |
| **Ceramidas** | Grasas naturales que forman la capa protectora de la piel. Cuando esa capa está dañada (piel seca o sensible), las ceramidas la reparan. |
| **Retinol** | Forma de vitamina A que acelera la renovación de las células de la piel, reduciendo arrugas, manchas y mejorando la textura. El activo anti-edad más estudiado. |
| **Péptidos** | Proteínas pequeñas que le "avisan" a la piel que produzca más colágeno, la proteína que da firmeza y elasticidad. Son suaves y no irritan. |
| **Vitamina C** | Antioxidante que protege la piel del daño ambiental, ilumina el tono y ayuda a borrar manchas. Se usa en las mañanas. |
| **Centella asiática** | Planta medicinal con propiedades calmantes. Reduce el enrojecimiento y la inflamación. Ideal para pieles sensibles o con acné. |
| **Colágeno** | Proteína natural de la piel que la mantiene firme y elástica. Con la edad, la piel produce menos colágeno y aparecen las arrugas. |
| **Bloqueador solar** | Producto que protege la piel de los rayos ultravioleta del sol, responsables del 80% del envejecimiento prematuro y las manchas. |
| **Exfoliante químico** | Producto que elimina células muertas usando ingredientes ácidos suaves, sin frotar. |
| **Sebo** | Grasa natural que produce la piel. En exceso causa brillo y tapa poros; en déficit, la piel se reseca. |
| **Barrera cutánea** | Capa protectora exterior de la piel. Cuando está dañada, la piel pierde humedad y se irrita fácilmente. |
| **Suero** | Producto de textura ligera con alta concentración de ingredientes activos. Va después del limpiador y antes de la crema. |
