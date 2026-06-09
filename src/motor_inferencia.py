# =============================================================================
# motor_inferencia.py
# Motor de Inferencia — Encadenamiento Hacia Adelante
# Sistema Experto de Skincare | Inteligencia Artificial II
# Uyaban Lorena, Lozada Harvey
# =============================================================================

import logging
from copy import deepcopy

# ─── Configuración de logging ─────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# =============================================================================
# MAPEO DE PREDICADOS DERIVADOS → PRODUCTOS CONCRETOS
# =============================================================================

PRODUCTOS_MAPEADOS = {
    "usar_limpiador_suave": {
        "nombre": "Limpiador Facial Suave",
        "descripcion": "Jabón o gel suave para lavar la cara, sin ingredientes que irriten. Úsalo mañana y noche.",
        "ejemplos": ["CeraVe Hydrating Cleanser", "La Roche-Posay Toleriane Hydrating", "Simple Kind to Skin"],
        "momento": ["AM", "PM"],
        "paso": 1,
        "icono": "🧴"
    },
    "usar_limpiador_salicilico": {
        "nombre": "Limpiador con Ácido Salicílico",
        "descripcion": "Jabón especial para piel grasa y con acné. El ácido salicílico entra al poro y lo limpia por dentro, reduciendo granos y espinillas.",
        "ejemplos": ["Neutrogena Oil-Free Acne Wash", "The Inkey List Salicylic Acid Cleanser", "Paula's Choice BHA Cleanser"],
        "momento": ["AM", "PM"],
        "paso": 1,
        "icono": "🧴"
    },
    "doble_limpieza": {
        "nombre": "Doble Limpieza Nocturna",
        "descripcion": "Limpiar la cara en dos pasos por la noche: primero con un aceite o bálsamo para quitar el maquillaje y el bloqueador solar, luego con un jabón normal.",
        "ejemplos": ["Banila Co Clean It Zero (aceite)", "DHC Deep Cleansing Oil", "Farmacy Green Clean Balm"],
        "momento": ["PM"],
        "paso": 0,
        "icono": "✨"
    },
    "usar_acido_hialuronico": {
        "nombre": "Suero de Ácido Hialurónico",
        "descripcion": "Suero que atrae y retiene la humedad en la piel, como una esponja de agua. Se aplica después de lavar la cara, con la piel todavía un poco húmeda, para mejores resultados.",
        "ejemplos": ["The Ordinary Hyaluronic Acid 2% + B5", "Neutrogena Hydro Boost Serum", "L'Oréal Revitalift Suero HA"],
        "momento": ["AM", "PM"],
        "paso": 2,
        "icono": "💧"
    },
    "usar_vitamina_c": {
        "nombre": "Suero de Vitamina C",
        "descripcion": "Suero que ilumina el tono de la piel, borra manchas y la protege de los daños del ambiente. Se usa en las mañanas, antes del bloqueador solar.",
        "ejemplos": ["TruSkin Vitamin C Serum", "The Ordinary Ascorbyl Glucoside 12%", "Timeless 20% Vitamin C + E"],
        "momento": ["AM"],
        "paso": 2,
        "icono": "🍊"
    },
    "usar_niacinamida": {
        "nombre": "Suero de Niacinamida (Vitamina B3)",
        "descripcion": "Suero con vitamina B3. Controla el brillo y el exceso de grasa, reduce la apariencia de los poros y pareja el tono de la piel. Muy suave, lo toleran casi todos los tipos de piel.",
        "ejemplos": ["The Ordinary Niacinamide 10% + Zinc 1%", "Paula's Choice 10% Niacinamide Booster", "Good Molecules Niacinamide Serum"],
        "momento": ["AM", "PM"],
        "paso": 2,
        "icono": "⚗️"
    },
    "usar_peptidos": {
        "nombre": "Suero con Péptidos",
        "descripcion": "Suero con proteínas pequeñas que le dicen a la piel que produzca más colágeno (la proteína que le da firmeza y elasticidad). Ideal para reducir arrugas sin irritar.",
        "ejemplos": ["The Ordinary Buffet + Copper Peptides", "Olay Regenerist Micro-Sculpting Serum", "NIOD CAIL Copper Amino"],
        "momento": ["AM", "PM"],
        "paso": 2,
        "icono": "🔬"
    },
    "usar_centella_asiatica": {
        "nombre": "Producto con Centella Asiática",
        "descripcion": "Crema o suero con una planta medicinal llamada centella asiática. Calma el enrojecimiento, la irritación y la picazón de forma natural. Ideal para pieles reactivas.",
        "ejemplos": ["COSRX Centella Blemish Cream", "Dr.Jart+ Cicapair Tiger Grass Cream", "Purito Centella Green Level Serum"],
        "momento": ["AM", "PM"],
        "paso": 2,
        "icono": "🌿"
    },
    "usar_acido_salicilico": {
        "nombre": "Tónico/Suero con Ácido Salicílico",
        "descripcion": "Líquido exfoliante que limpia el interior de los poros sin necesidad de frotar. Reduce los puntos negros y los granos. Se aplica por las noches.",
        "ejemplos": ["Paula's Choice 2% BHA Liquid Exfoliant", "The Ordinary Salicylic Acid 2% Anhydrous", "COSRX BHA Blackhead Power Liquid"],
        "momento": ["PM"],
        "paso": 2,
        "icono": "⚗️"
    },
    "usar_retinol": {
        "nombre": "Retinol (Vitamina A) — Uso Nocturno",
        "descripcion": "Vitamina A en crema o suero que renueva las células de la piel mientras duermes, reduciendo arrugas y mejorando la textura. Empezar usándolo 2 noches por semana. Siempre aplicar primero una crema hidratante para reducir la sensibilidad.",
        "ejemplos": ["The Ordinary Granactive Retinoid 2% Emulsion", "CeraVe Skin Renewing Retinol Serum", "RoC Retinol Correxion Line Smoothing"],
        "momento": ["PM"],
        "paso": 3,
        "icono": "🌙"
    },
    "usar_ceramidas": {
        "nombre": "Crema con Ceramidas",
        "descripcion": "Crema que repara la capa protectora de la piel. Las ceramidas son grasas naturales que la piel necesita para no perder humedad ni dejarse irritar fácilmente.",
        "ejemplos": ["CeraVe Moisturizing Cream", "Elizabeth Arden Advanced Ceramide Capsules", "Eucerin Original Healing Cream"],
        "momento": ["AM", "PM"],
        "paso": 3,
        "icono": "🛡️"
    },
    "usar_hidratante_ligero": {
        "nombre": "Crema Hidratante Ligera (sin aceite)",
        "descripcion": "Crema o gel de textura suave y ligera, sin aceite. Hidrata la piel sin dejarla grasosa ni tapar los poros. Perfecta para piel grasa o mixta.",
        "ejemplos": ["Neutrogena Hydro Boost Water Gel", "La Roche-Posay Effaclar Mat", "Clinique Dramatically Different Moisturizing Gel"],
        "momento": ["AM", "PM"],
        "paso": 3,
        "icono": "💦"
    },
    "usar_hidratante_rico": {
        "nombre": "Crema Hidratante Nutritiva",
        "descripcion": "Crema espesa y nutritiva que cubre bien la piel seca. Ideal para quienes sienten la piel tirante, áspera o con tendencia a descamarse.",
        "ejemplos": ["CeraVe Moisturizing Cream", "First Aid Beauty Ultra Repair Cream", "Eucerin Advanced Repair Cream"],
        "momento": ["AM", "PM"],
        "paso": 3,
        "icono": "🧈"
    },
    "usar_protector_solar": {
        "nombre": "Bloqueador Solar (Factor 30 o más)",
        "descripcion": "Protege la piel de los rayos del sol, que son la causa principal del envejecimiento prematuro y las manchas. Es el último paso de la rutina de la mañana. Reaplicar cada 2 horas si pasas tiempo al sol.",
        "ejemplos": ["La Roche-Posay Anthelios Invisible Fluid", "EltaMD UV Clear", "Supergoop! Unseen Sunscreen"],
        "momento": ["AM"],
        "paso": 4,
        "icono": "☀️"
    },
    "usar_mascarilla_arcilla": {
        "nombre": "Mascarilla de Arcilla",
        "descripcion": "Mascarilla para usar 1 o 2 veces por semana. Absorbe el exceso de grasa y limpia los poros en profundidad. Se deja actuar 10-15 minutos y se retira con agua.",
        "ejemplos": ["Aztec Secret Indian Healing Clay", "L'Oréal Pure Clay Mask", "Innisfree Super Volcanic Pore Clay Mask"],
        "momento": ["Semanal"],
        "paso": 5,
        "icono": "🏺"
    }
}


# =============================================================================
# FUNCIÓN PRINCIPAL: ENCADENAMIENTO HACIA ADELANTE
# =============================================================================

def encadenamiento_adelante(reglas, hechos_iniciales):
    """
    Aplica encadenamiento hacia adelante (forward chaining) sobre la base de conocimiento.

    Algoritmo:
        1. Copiar hechos iniciales del usuario a la memoria de trabajo.
        2. Iterar sobre todas las reglas.
        3. Para cada regla, verificar si TODAS sus condiciones son verdaderas en la memoria.
        4. Si se cumple y genera hechos nuevos → agregar conclusiones y marcar cambio.
        5. Repetir hasta punto fijo (sin nuevos hechos) o límite de iteraciones.

    Args:
        reglas (list): Lista de reglas de producción desde base_conocimiento.py
        hechos_iniciales (dict): Hechos aportados por el usuario {predicado: bool}

    Returns:
        tuple: (hechos_finales dict, reglas_aplicadas list)
    """
    hechos = deepcopy(dict(hechos_iniciales))
    reglas_aplicadas = []
    nombres_aplicadas = set()
    MAX_ITERACIONES = 50  # Salvaguarda contra ciclos infinitos

    logger.info("=" * 60)
    logger.info("INICIO ENCADENAMIENTO HACIA ADELANTE")
    logger.info(f"Hechos iniciales: {[k for k, v in hechos.items() if v]}")
    logger.info("=" * 60)

    cambio = True
    iteracion = 0

    while cambio and iteracion < MAX_ITERACIONES:
        cambio = False
        iteracion += 1
        logger.info(f"── Iteración {iteracion} ──")

        for regla in reglas:
            nombre = regla["nombre"]

            # Omitir reglas ya aplicadas
            if nombre in nombres_aplicadas:
                continue

            # ── Evaluar condiciones ──────────────────────────────────────────
            condiciones = regla.get("condiciones", [])

            if len(condiciones) == 0:
                # Regla universal (R15): siempre se aplica
                aplica = True
            else:
                aplica = all(
                    hechos.get(pred, False) == val_esperado
                    for pred, val_esperado in condiciones
                )

            if not aplica:
                continue

            # ── Verificar si produce hechos nuevos ───────────────────────────
            conclusiones = regla.get("conclusiones", [])
            nuevos = [(pred, val) for pred, val in conclusiones if hechos.get(pred) != val]

            if not nuevos and len(condiciones) > 0:
                # Todas las conclusiones ya existen; no aporta nada nuevo
                continue

            # ── Aplicar regla ────────────────────────────────────────────────
            for pred, val in conclusiones:
                hechos[pred] = val

            entrada_log = {
                "nombre": nombre,
                "descripcion": regla["descripcion"],
                "categoria": regla["categoria"],
                "condiciones_activadas": condiciones,
                "conclusiones_derivadas": conclusiones,
                "certeza": regla["certeza"],
                "si_entonces": regla["si_entonces"],
                "justificacion": regla["justificacion"],
                "iteracion": iteracion
            }

            reglas_aplicadas.append(entrada_log)
            nombres_aplicadas.add(nombre)
            cambio = True

            logger.info(
                f"  ✓ {nombre} aplicada → "
                f"{[c[0] for c in conclusiones]}"
            )

    if iteracion >= MAX_ITERACIONES:
        logger.warning("⚠ Límite de iteraciones alcanzado. Posible ciclo detectado.")

    logger.info(f"Proceso terminado en {iteracion} iteración(es).")
    logger.info(f"Reglas aplicadas: {[r['nombre'] for r in reglas_aplicadas]}")
    logger.info("=" * 60)

    return hechos, reglas_aplicadas


# =============================================================================
# FUNCIÓN: EXPLICAR RAZONAMIENTO COMPLETO
# =============================================================================

def explicar_razonamiento(reglas_aplicadas):
    """
    Genera una explicación legible del proceso completo de razonamiento.

    Args:
        reglas_aplicadas (list): Lista de reglas que se aplicaron.

    Returns:
        str: Texto explicativo estructurado.
    """
    if not reglas_aplicadas:
        return (
            "No se pudieron derivar conclusiones con los hechos proporcionados. "
            "Intenta seleccionar más opciones de tipo de piel u objetivos."
        )

    lineas = [
        f"El motor de inferencia aplicó {len(reglas_aplicadas)} regla(s) "
        f"mediante encadenamiento hacia adelante:\n"
    ]

    for i, r in enumerate(reglas_aplicadas, 1):
        certeza_pct = int(r["certeza"] * 100)
        lineas.append(f"{'─'*55}")
        lineas.append(f"Paso {i} → [{r['nombre']}] {r['descripcion']}")
        lineas.append(f"Categoría : {r['categoria']}")
        lineas.append(f"Certeza   : {certeza_pct}%")

        if r["condiciones_activadas"]:
            conds = " ∧ ".join(f"{c[0]}" for c in r["condiciones_activadas"])
            lineas.append(f"Condición : {conds}")
        else:
            lineas.append("Condición : (regla universal — aplica siempre)")

        concls = ", ".join(c[0] for c in r["conclusiones_derivadas"])
        lineas.append(f"Derivó    : {concls}")
        lineas.append(f"Por qué   : {r['justificacion']}")
        lineas.append("")

    return "\n".join(lineas)


# =============================================================================
# FUNCIÓN: PORQUE (explicación de una conclusión específica)
# =============================================================================

def porque(conclusion, hechos_iniciales, reglas_aplicadas):
    """
    Explica por qué el sistema llegó a una conclusión específica.

    Args:
        conclusion (str): Predicado cuya justificación se quiere conocer.
        hechos_iniciales (dict): Hechos aportados por el usuario.
        reglas_aplicadas (list): Reglas que se aplicaron durante la inferencia.

    Returns:
        str: Cadena explicando la cadena de razonamiento hacia esa conclusión.
    """
    # ── Si es un hecho inicial ───────────────────────────────────────────────
    if hechos_iniciales.get(conclusion):
        return (
            f"'{conclusion}' fue proporcionado directamente por el usuario "
            f"como hecho inicial, no fue derivado por el motor."
        )

    # ── Buscar qué reglas derivaron esta conclusión ──────────────────────────
    fuentes = [
        r for r in reglas_aplicadas
        if any(c == conclusion and v for c, v in r["conclusiones_derivadas"])
    ]

    if not fuentes:
        return f"La conclusión '{conclusion}' no fue derivada en esta sesión."

    partes = [f"La conclusión '{conclusion}' fue derivada porque:"]

    for r in fuentes:
        partes.append(f"\n  Regla {r['nombre']}: {r['descripcion']}")
        partes.append(f"  Fórmula lógica: {r['si_entonces']}")

        if r["condiciones_activadas"]:
            partes.append("  Se cumplieron las condiciones:")
            for cond, val in r["condiciones_activadas"]:
                origen = (
                    "hecho inicial del usuario"
                    if hechos_iniciales.get(cond) == val
                    else "derivado por otra regla"
                )
                partes.append(f"    ✓ {cond} = {val}  ({origen})")
        else:
            partes.append("  Es una regla universal (aplica siempre).")

        partes.append(f"  Base científica: {r['justificacion']}")

    return "\n".join(partes)


# =============================================================================
# FUNCIÓN: OBTENER RECOMENDACIONES ESTRUCTURADAS
# =============================================================================

def obtener_recomendaciones(hechos_finales, hechos_iniciales):
    """
    Extrae los productos y la rutina recomendada a partir de los hechos derivados.

    Args:
        hechos_finales (dict): Todos los hechos tras la inferencia.
        hechos_iniciales (dict): Hechos originales del usuario.

    Returns:
        dict: {
            'rutina_manana': [...],
            'rutina_noche': [...],
            'extras': [...],
            'advertencias': [...],
            'todos_los_productos': [...]
        }
    """
    productos = []
    advertencias = []

    for predicado, info in PRODUCTOS_MAPEADOS.items():
        # Solo incluir predicados derivados (no eran hechos del usuario)
        if hechos_finales.get(predicado) and not hechos_iniciales.get(predicado):
            productos.append({
                "predicado": predicado,
                "nombre": info["nombre"],
                "descripcion": info["descripcion"],
                "ejemplos": info["ejemplos"],
                "momento": info["momento"],
                "paso": info["paso"],
                "icono": info["icono"]
            })

    # Ordenar por paso en la rutina
    productos.sort(key=lambda x: x["paso"])

    # ── Advertencias contextuales ────────────────────────────────────────────
    if hechos_finales.get("evitar_retinol"):
        advertencias.append({
            "tipo": "warning",
            "texto": (
                "Tu tipo de piel sensible es incompatible con el retinol. "
                "Puede provocar enrojecimiento severo e irritación. "
                "Consulta a un dermatólogo antes de usarlo."
            )
        })

    if hechos_finales.get("rutina_minimalista"):
        advertencias.append({
            "tipo": "info",
            "texto": (
                "Para tu tipo de piel, una rutina de 3 pasos es más efectiva "
                "que una cargada de activos. Menos es más."
            )
        })

    if hechos_finales.get("usar_retinol"):
        advertencias.append({
            "tipo": "info",
            "texto": (
                "Si es tu primera vez con retinol, comienza 2 noches/semana "
                "durante el primer mes. Siempre aplica hidratante antes (técnica sandwich)."
            )
        })

    # ── Separar por momento del día ──────────────────────────────────────────
    rutina_manana = [p for p in productos if "AM" in p["momento"]]
    rutina_noche = [p for p in productos if "PM" in p["momento"]]
    extras = [p for p in productos if p["momento"] == ["Semanal"]]

    return {
        "rutina_manana": rutina_manana,
        "rutina_noche": rutina_noche,
        "extras": extras,
        "advertencias": advertencias,
        "todos_los_productos": productos
    }
