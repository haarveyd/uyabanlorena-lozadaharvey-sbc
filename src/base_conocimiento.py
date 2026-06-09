# =============================================================================
# base_conocimiento.py
# Sistema Experto de Recomendación de Rutinas de Skincare
# Inteligencia Artificial II - Proyecto Final
# Uyaban Lorena, Lozada Harvey
# =============================================================================

# =============================================================================
# PREDICADOS DEL DOMINIO
# Definición formal: nombre → {descripcion, tipo, dominio, rango, notacion_logica}
# Tipos: 'entrada' (usuario), 'derivado' (motor de inferencia)
# =============================================================================

PREDICADOS = {
    # ─── Tipo de piel (entrada) ────────────────────────────────────────────
    "piel_grasa": {
        "descripcion": "La piel produce exceso de sebo, luce brillante y tiene tendencia al acné",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ piel_grasa(x) → exceso_sebo(x) ∧ brillo_facial(x) ]"
    },
    "piel_seca": {
        "descripcion": "La piel produce poco sebo, se siente tirante y puede descamarse",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ piel_seca(x) → bajo_sebo(x) ∧ tension_facial(x) ]"
    },
    "piel_mixta": {
        "descripcion": "Zona T (frente/nariz/mentón) grasa; mejillas normales o secas",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ piel_mixta(x) → piel_grasa(zona_T(x)) ∧ ¬piel_grasa(mejillas(x)) ]"
    },
    "piel_normal": {
        "descripcion": "Piel equilibrada: sin exceso de grasa ni sequedad notable",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ piel_normal(x) → ¬piel_grasa(x) ∧ ¬piel_seca(x) ∧ ¬piel_sensible(x) ]"
    },
    "piel_sensible": {
        "descripcion": "La piel reacciona fácilmente: rojeces, picores o irritación ante productos",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ piel_sensible(x) → reaccion_adversa(x, ingredientes_activos) ]"
    },
    # ─── Objetivos de cuidado (entrada) ────────────────────────────────────
    "objetivo_hidratacion": {
        "descripcion": "El usuario busca mejorar la hidratación y suavidad de su piel",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ objetivo_hidratacion(x) → busca(x, mejorar_hidratacion_cutanea) ]"
    },
    "objetivo_anti_acne": {
        "descripcion": "El usuario busca reducir o eliminar acné y espinillas",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ objetivo_anti_acne(x) → busca(x, reducir_acne) ]"
    },
    "objetivo_anti_envejecimiento": {
        "descripcion": "El usuario busca prevenir o reducir líneas de expresión y signos de envejecimiento",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ objetivo_anti_envejecimiento(x) → busca(x, prevenir_envejecimiento) ]"
    },
    "objetivo_iluminacion": {
        "descripcion": "El usuario busca un tono de piel más luminoso y uniforme",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ objetivo_iluminacion(x) → busca(x, luminosidad_cutanea) ]"
    },
    "objetivo_poros": {
        "descripcion": "El usuario busca minimizar la apariencia de poros dilatados",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ objetivo_poros(x) → busca(x, minimizar_poros_dilatados) ]"
    },
    "objetivo_manchas": {
        "descripcion": "El usuario busca reducir manchas e hiperpigmentación",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ objetivo_manchas(x) → busca(x, reducir_hiperpigmentacion) ]"
    },
    # ─── Rango de edad (entrada) ────────────────────────────────────────────
    "edad_joven": {
        "descripcion": "El usuario tiene entre 15 y 25 años",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ edad_joven(x) ↔ 15 ≤ edad(x) ≤ 25 ]"
    },
    "edad_adulto": {
        "descripcion": "El usuario tiene entre 26 y 40 años",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ edad_adulto(x) ↔ 26 ≤ edad(x) ≤ 40 ]"
    },
    "edad_maduro": {
        "descripcion": "El usuario tiene más de 40 años",
        "tipo": "entrada",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x [ edad_maduro(x) ↔ edad(x) > 40 ]"
    },
    # ─── Predicados derivados (conclusiones del motor) ──────────────────────
    "usar_limpiador_suave": {
        "descripcion": "Usar limpiador facial suave sin sulfatos, pH neutro (4.5–6.5)",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_limpiador_suave(x) ← piel_normal(x) ∨ piel_mixta(x) ∨ piel_sensible(x)"
    },
    "usar_limpiador_salicilico": {
        "descripcion": "Usar limpiador con ácido salicílico (BHA) al 0.5–2% para desobstruir poros",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_limpiador_salicilico(x) ← piel_grasa(x) ∧ objetivo_anti_acne(x)"
    },
    "usar_hidratante_ligero": {
        "descripcion": "Usar hidratante de textura ligera: gel o loción oil-free",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_hidratante_ligero(x) ← piel_grasa(x) ∨ piel_mixta(x)"
    },
    "usar_hidratante_rico": {
        "descripcion": "Usar hidratante de textura rica: crema nutritiva emoliente",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_hidratante_rico(x) ← piel_seca(x) ∨ (piel_sensible(x) ∧ objetivo_hidratacion(x))"
    },
    "usar_protector_solar": {
        "descripcion": "Usar protector solar SPF 30+ diariamente (regla universal)",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "∀x usar_protector_solar(x)"
    },
    "usar_niacinamida": {
        "descripcion": "Usar sérum o tónico con niacinamida (vitamina B3) al 5–10%",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_niacinamida(x) ← piel_grasa(x) ∨ objetivo_poros(x) ∨ objetivo_manchas(x)"
    },
    "usar_acido_hialuronico": {
        "descripcion": "Usar sérum de ácido hialurónico para atracción de agua a la piel",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_acido_hialuronico(x) ← piel_seca(x) ∨ objetivo_hidratacion(x)"
    },
    "usar_vitamina_c": {
        "descripcion": "Usar sérum vitamina C (10–20%) por la mañana como antioxidante",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_vitamina_c(x) ← objetivo_iluminacion(x) ∨ objetivo_manchas(x) ∨ objetivo_anti_envejecimiento(x)"
    },
    "usar_retinol": {
        "descripcion": "Usar retinol (0.025–0.1%) por la noche, comenzando 2 veces/semana",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_retinol(x) ← objetivo_anti_envejecimiento(x) ∧ (edad_adulto(x) ∨ edad_maduro(x)) ∧ ¬piel_sensible(x)"
    },
    "usar_acido_salicilico": {
        "descripcion": "Usar tónico/sérum con ácido salicílico para exfoliación química de poros",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_acido_salicilico(x) ← objetivo_anti_acne(x) ∨ (piel_grasa(x) ∧ objetivo_poros(x))"
    },
    "usar_centella_asiatica": {
        "descripcion": "Usar productos con centella asiática (Cica) para calmar inflamación",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_centella_asiatica(x) ← piel_sensible(x)"
    },
    "usar_ceramidas": {
        "descripcion": "Usar crema con ceramidas para restaurar la barrera lipídica cutánea",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_ceramidas(x) ← piel_seca(x) ∨ piel_sensible(x)"
    },
    "usar_peptidos": {
        "descripcion": "Usar sérum con péptidos para mejorar firmeza y estimular colágeno",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_peptidos(x) ← objetivo_anti_envejecimiento(x) ∧ (edad_adulto(x) ∨ edad_maduro(x))"
    },
    "evitar_retinol": {
        "descripcion": "Contraindicación: evitar retinol en piel sensible (riesgo de irritación severa)",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "evitar_retinol(x) ← piel_sensible(x)"
    },
    "rutina_minimalista": {
        "descripcion": "Aplicar rutina de solo 3 pasos: limpieza → hidratación → protección solar",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "rutina_minimalista(x) ← piel_sensible(x) ∨ piel_normal(x)"
    },
    "doble_limpieza": {
        "descripcion": "Realizar doble limpieza nocturna: aceite desmaquillante + limpiador acuoso",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "doble_limpieza(x) ← piel_grasa(x) ∧ objetivo_poros(x)"
    },
    "usar_mascarilla_arcilla": {
        "descripcion": "Aplicar mascarilla de arcilla 1–2 veces/semana para absorber exceso de sebo",
        "tipo": "derivado",
        "dominio": "Persona",
        "rango": "Boolean",
        "notacion": "usar_mascarilla_arcilla(x) ← piel_grasa(x) ∧ (objetivo_poros(x) ∨ objetivo_anti_acne(x))"
    }
}


# =============================================================================
# REGLAS DE PRODUCCIÓN
# 15 reglas formalizadas en lógica de predicados con formato SI-ENTONCES
# Campo 'condiciones': lista de (predicado, valor_esperado)
# Campo 'conclusiones': lista de (predicado, valor_derivado)
# =============================================================================

REGLAS = [
    {
        "nombre": "R1",
        "categoria": "Control de Acné",
        "descripcion": "Piel grasa con acné: limpieza con BHA y regulación de sebo",
        "condiciones": [
            ("piel_grasa", True),
            ("objetivo_anti_acne", True)
        ],
        "conclusiones": [
            ("usar_limpiador_salicilico", True),
            ("usar_niacinamida", True),
            ("usar_hidratante_ligero", True),
            ("usar_mascarilla_arcilla", True)
        ],
        "certeza": 0.95,
        "si_entonces": (
            "SI piel_grasa(x) ∧ objetivo_anti_acne(x) "
            "ENTONCES usar_limpiador_salicilico(x) ∧ usar_niacinamida(x) "
            "∧ usar_hidratante_ligero(x) ∧ usar_mascarilla_arcilla(x)"
        ),
        "justificacion": (
            "El ácido salicílico (BHA) es liposoluble: penetra el poro y disuelve el "
            "tapón de sebo que causa el acné. La niacinamida regula la sebosidad sin "
            "irritar. Incluso la piel grasa necesita hidratación ligera para no "
            "compensar produciendo más sebo."
        )
    },
    {
        "nombre": "R2",
        "categoria": "Hidratación Intensa",
        "descripcion": "Piel seca que busca hidratación: activos humectantes y oclusivos",
        "condiciones": [
            ("piel_seca", True),
            ("objetivo_hidratacion", True)
        ],
        "conclusiones": [
            ("usar_acido_hialuronico", True),
            ("usar_ceramidas", True),
            ("usar_hidratante_rico", True)
        ],
        "certeza": 0.97,
        "si_entonces": (
            "SI piel_seca(x) ∧ objetivo_hidratacion(x) "
            "ENTONCES usar_acido_hialuronico(x) ∧ usar_ceramidas(x) ∧ usar_hidratante_rico(x)"
        ),
        "justificacion": (
            "El ácido hialurónico es humectante: atrae hasta 1000 veces su peso en agua. "
            "Las ceramidas son lípidos que conforman la barrera cutánea; en piel seca esta "
            "barrera está comprometida. La crema rica actúa como oclusivo para retener la humedad."
        )
    },
    {
        "nombre": "R3",
        "categoria": "Equilibrio Piel Mixta",
        "descripcion": "Piel mixta: limpieza suave con niacinamida para equilibrar zonas",
        "condiciones": [
            ("piel_mixta", True)
        ],
        "conclusiones": [
            ("usar_limpiador_suave", True),
            ("usar_hidratante_ligero", True),
            ("usar_niacinamida", True)
        ],
        "certeza": 0.90,
        "si_entonces": (
            "SI piel_mixta(x) "
            "ENTONCES usar_limpiador_suave(x) ∧ usar_hidratante_ligero(x) ∧ usar_niacinamida(x)"
        ),
        "justificacion": (
            "La piel mixta exige equilibrio. Un limpiador suave no altera las zonas secas "
            "mientras limpia la zona T. La niacinamida regula el sebo de forma selectiva "
            "sin resecar las mejillas."
        )
    },
    {
        "nombre": "R4",
        "categoria": "Protocolo Piel Sensible",
        "descripcion": "Piel sensible: rutina calmante y minimalista con ingredientes seguros",
        "condiciones": [
            ("piel_sensible", True)
        ],
        "conclusiones": [
            ("usar_centella_asiatica", True),
            ("usar_ceramidas", True),
            ("evitar_retinol", True),
            ("rutina_minimalista", True)
        ],
        "certeza": 0.95,
        "si_entonces": (
            "SI piel_sensible(x) "
            "ENTONCES usar_centella_asiatica(x) ∧ usar_ceramidas(x) "
            "∧ evitar_retinol(x) ∧ rutina_minimalista(x)"
        ),
        "justificacion": (
            "La centella asiática (Cica) tiene propiedades antiinflamatorias clínicamente "
            "probadas. Las ceramidas reparan la barrera comprometida en pieles sensibles. "
            "El retinol está contraindicado por su potencial irritante. "
            "Menos productos = menos riesgo de reacción adversa."
        )
    },
    {
        "nombre": "R5",
        "categoria": "Hidratación Piel Sensible",
        "descripcion": "Piel sensible con objetivo hidratación: activos suaves y reparadores",
        "condiciones": [
            ("piel_sensible", True),
            ("objetivo_hidratacion", True)
        ],
        "conclusiones": [
            ("usar_acido_hialuronico", True),
            ("usar_ceramidas", True),
            ("usar_hidratante_rico", True)
        ],
        "certeza": 0.93,
        "si_entonces": (
            "SI piel_sensible(x) ∧ objetivo_hidratacion(x) "
            "ENTONCES usar_acido_hialuronico(x) ∧ usar_ceramidas(x) ∧ usar_hidratante_rico(x)"
        ),
        "justificacion": (
            "Para piel sensible-seca, el ácido hialurónico y las ceramidas son activos de "
            "alta tolerabilidad: no contienen fragancias ni retinoides. Restauran la hidratación "
            "sin desencadenar reacciones inflamatorias."
        )
    },
    {
        "nombre": "R6",
        "categoria": "Anti-envejecimiento Avanzado",
        "descripcion": "Anti-envejecimiento en piel madura: retinol + péptidos + vitamina C",
        "condiciones": [
            ("objetivo_anti_envejecimiento", True),
            ("edad_maduro", True)
        ],
        "conclusiones": [
            ("usar_retinol", True),
            ("usar_peptidos", True),
            ("usar_vitamina_c", True),
            ("usar_protector_solar", True)
        ],
        "certeza": 0.96,
        "si_entonces": (
            "SI objetivo_anti_envejecimiento(x) ∧ edad_maduro(x) "
            "ENTONCES usar_retinol(x) ∧ usar_peptidos(x) ∧ usar_vitamina_c(x) ∧ usar_protector_solar(x)"
        ),
        "justificacion": (
            "El retinol (vitamina A) es el activo anti-aging con mayor evidencia clínica: "
            "acelera el recambio celular y estimula colágeno. Los péptidos tienen acción "
            "complementaria. La vitamina C es antioxidante de mañana. "
            "El SPF es obligatorio para no revertir los beneficios."
        )
    },
    {
        "nombre": "R7",
        "categoria": "Anti-envejecimiento Preventivo",
        "descripcion": "Anti-envejecimiento en adultos (26-40): vitamina C y péptidos como prevención",
        "condiciones": [
            ("objetivo_anti_envejecimiento", True),
            ("edad_adulto", True)
        ],
        "conclusiones": [
            ("usar_vitamina_c", True),
            ("usar_peptidos", True),
            ("usar_acido_hialuronico", True),
            ("usar_protector_solar", True)
        ],
        "certeza": 0.92,
        "si_entonces": (
            "SI objetivo_anti_envejecimiento(x) ∧ edad_adulto(x) "
            "ENTONCES usar_vitamina_c(x) ∧ usar_peptidos(x) ∧ usar_acido_hialuronico(x) ∧ usar_protector_solar(x)"
        ),
        "justificacion": (
            "En la etapa 26-40 el colágeno comienza a disminuir (~1%/año). Los péptidos "
            "y la vitamina C son opciones preventivas más seguras que el retinol, que puede "
            "reservarse para signos más avanzados. El ácido hialurónico mantiene volumen."
        )
    },
    {
        "nombre": "R8",
        "categoria": "Prevención Temprana",
        "descripcion": "Anti-envejecimiento en jóvenes (15-25): vitamina C y SPF como prevención básica",
        "condiciones": [
            ("objetivo_anti_envejecimiento", True),
            ("edad_joven", True)
        ],
        "conclusiones": [
            ("usar_vitamina_c", True),
            ("usar_protector_solar", True),
            ("usar_hidratante_ligero", True)
        ],
        "certeza": 0.88,
        "si_entonces": (
            "SI objetivo_anti_envejecimiento(x) ∧ edad_joven(x) "
            "ENTONCES usar_vitamina_c(x) ∧ usar_protector_solar(x) ∧ usar_hidratante_ligero(x)"
        ),
        "justificacion": (
            "El 80% del envejecimiento cutáneo visible es causado por exposición solar (fotoenvejecimiento). "
            "Para jóvenes, la mejor anti-edad es prevención: SPF diario y antioxidantes. "
            "El retinol no es necesario aún en esta etapa."
        )
    },
    {
        "nombre": "R9",
        "categoria": "Luminosidad y Uniformidad",
        "descripcion": "Objetivo luminosidad: vitamina C + niacinamida para tono uniforme",
        "condiciones": [
            ("objetivo_iluminacion", True)
        ],
        "conclusiones": [
            ("usar_vitamina_c", True),
            ("usar_protector_solar", True),
            ("usar_niacinamida", True)
        ],
        "certeza": 0.93,
        "si_entonces": (
            "SI objetivo_iluminacion(x) "
            "ENTONCES usar_vitamina_c(x) ∧ usar_protector_solar(x) ∧ usar_niacinamida(x)"
        ),
        "justificacion": (
            "La vitamina C inhibe la tirosinasa, enzima clave en la síntesis de melanina, "
            "aclarando el tono. La niacinamida bloquea la transferencia de melanosomas a "
            "los queratinocitos. Ambas acción requieren SPF para no generar nuevas manchas."
        )
    },
    {
        "nombre": "R10",
        "categoria": "Reducción de Manchas",
        "descripcion": "Objetivo manchas: activos despigmentantes + protección solar obligatoria",
        "condiciones": [
            ("objetivo_manchas", True)
        ],
        "conclusiones": [
            ("usar_vitamina_c", True),
            ("usar_niacinamida", True),
            ("usar_protector_solar", True)
        ],
        "certeza": 0.94,
        "si_entonces": (
            "SI objetivo_manchas(x) "
            "ENTONCES usar_vitamina_c(x) ∧ usar_niacinamida(x) ∧ usar_protector_solar(x)"
        ),
        "justificacion": (
            "La vitamina C y niacinamida son los activos despigmentantes de mayor seguridad y "
            "evidencia. Sin protector solar, la radiación UV activa la melanogénesis y las "
            "manchas reaparecen. El SPF es insustituible en este objetivo."
        )
    },
    {
        "nombre": "R11",
        "categoria": "Poros Dilatados",
        "descripcion": "Piel grasa con poros dilatados: BHA + niacinamida + doble limpieza",
        "condiciones": [
            ("piel_grasa", True),
            ("objetivo_poros", True)
        ],
        "conclusiones": [
            ("usar_niacinamida", True),
            ("usar_acido_salicilico", True),
            ("doble_limpieza", True),
            ("usar_mascarilla_arcilla", True)
        ],
        "certeza": 0.91,
        "si_entonces": (
            "SI piel_grasa(x) ∧ objetivo_poros(x) "
            "ENTONCES usar_niacinamida(x) ∧ usar_acido_salicilico(x) "
            "∧ doble_limpieza(x) ∧ usar_mascarilla_arcilla(x)"
        ),
        "justificacion": (
            "Los poros dilatados en piel grasa se deben al exceso de sebo que los agranda. "
            "La niacinamida los minimiza visualmente reduciendo el sebo. "
            "El ácido salicílico penetra y desobstruye el contenido del poro. "
            "La doble limpieza asegura que no queden residuos que los tapen."
        )
    },
    {
        "nombre": "R12",
        "categoria": "Acné en Piel Sensible",
        "descripcion": "Acné en piel sensible: tratamiento suave para evitar irritación adicional",
        "condiciones": [
            ("objetivo_anti_acne", True),
            ("piel_sensible", True)
        ],
        "conclusiones": [
            ("usar_acido_salicilico", True),
            ("usar_centella_asiatica", True),
            ("usar_limpiador_suave", True)
        ],
        "certeza": 0.89,
        "si_entonces": (
            "SI objetivo_anti_acne(x) ∧ piel_sensible(x) "
            "ENTONCES usar_acido_salicilico(x) ∧ usar_centella_asiatica(x) ∧ usar_limpiador_suave(x)"
        ),
        "justificacion": (
            "La piel sensible con acné necesita tratar sin agravar la barrera. "
            "Ácido salicílico a baja concentración (0.5%) es efectivo y mejor tolerado. "
            "La centella asiática calma la inflamación post-acné. "
            "Se evita el limpiador salicílico fuerte por riesgo de irritación."
        )
    },
    {
        "nombre": "R13",
        "categoria": "Nutrición Piel Madura Seca",
        "descripcion": "Piel seca en edad madura: nutrición profunda con ceramidas y retinol",
        "condiciones": [
            ("piel_seca", True),
            ("edad_maduro", True)
        ],
        "conclusiones": [
            ("usar_ceramidas", True),
            ("usar_retinol", True),
            ("usar_acido_hialuronico", True),
            ("usar_hidratante_rico", True)
        ],
        "certeza": 0.94,
        "si_entonces": (
            "SI piel_seca(x) ∧ edad_maduro(x) "
            "ENTONCES usar_ceramidas(x) ∧ usar_retinol(x) "
            "∧ usar_acido_hialuronico(x) ∧ usar_hidratante_rico(x)"
        ),
        "justificacion": (
            "La piel madura pierde ceramidas y ácido hialurónico endógeno naturalmente. "
            "El retinol es esencial para la renovación celular; en piel seca se aplica "
            "sobre una capa de hidratante para minimizar la irritación (técnica sandwich). "
            "La crema rica proporciona los lípidos que la piel ya no sintetiza eficientemente."
        )
    },
    {
        "nombre": "R14",
        "categoria": "Mantenimiento Piel Normal",
        "descripcion": "Piel normal: rutina básica de mantenimiento para preservar el equilibrio",
        "condiciones": [
            ("piel_normal", True)
        ],
        "conclusiones": [
            ("usar_limpiador_suave", True),
            ("usar_hidratante_ligero", True),
            ("usar_protector_solar", True),
            ("rutina_minimalista", True)
        ],
        "certeza": 0.95,
        "si_entonces": (
            "SI piel_normal(x) "
            "ENTONCES usar_limpiador_suave(x) ∧ usar_hidratante_ligero(x) "
            "∧ usar_protector_solar(x) ∧ rutina_minimalista(x)"
        ),
        "justificacion": (
            "La piel normal está en equilibrio: el objetivo es mantenerlo, no transformarla. "
            "Una rutina simple de 3 pasos es suficiente y preferible a sobrecargar la piel "
            "con activos innecesarios que podrían alterar ese equilibrio."
        )
    },
    {
        "nombre": "R15",
        "categoria": "Protección Solar Universal",
        "descripcion": "Regla universal: toda persona debe aplicar protector solar SPF 30+ diariamente",
        "condiciones": [],  # Sin condiciones: se aplica siempre
        "conclusiones": [
            ("usar_protector_solar", True)
        ],
        "certeza": 1.0,
        "si_entonces": "∀x ENTONCES usar_protector_solar(x)",
        "justificacion": (
            "El protector solar SPF 30+ es el producto con mayor evidencia científica en "
            "prevención del envejecimiento prematuro y el melanoma. La OMS y AAD lo "
            "recomiendan para toda persona sin excepción, independientemente del tipo de "
            "piel, objetivo o edad."
        )
    }
]
