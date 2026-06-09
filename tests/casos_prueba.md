# Casos de Prueba — Sistema Experto LUMIS

## Tabla de casos

| Caso | Descripción | Hechos iniciales | Reglas esperadas | Conclusión esperada | Resultado obtenido | Estado |
|------|-------------|-----------------|-----------------|--------------------|--------------------|--------|
| 1 | Joven con piel grasa y acné | piel_grasa, objetivo_anti_acne, edad_joven | R1, R15 | usar_limpiador_salicilico, usar_niacinamida, usar_mascarilla_arcilla, usar_protector_solar | ✓ Todas derivadas | ✓ |
| 2 | Adulta piel seca busca hidratación | piel_seca, objetivo_hidratacion, edad_adulto | R2, R15 | usar_acido_hialuronico, usar_ceramidas, usar_hidratante_rico, usar_protector_solar | ✓ Todas derivadas | ✓ |
| 3 | Piel sensible con acné (sin retinol) | piel_sensible, objetivo_anti_acne, edad_joven | R4, R12, R15 | usar_centella_asiatica, usar_ceramidas, evitar_retinol, usar_acido_salicilico, usar_limpiador_suave, usar_protector_solar | ✓ Incluye evitar_retinol | ✓ |
| 4 | Madura anti-edad avanzado | objetivo_anti_envejecimiento, edad_maduro, piel_normal | R6, R14, R15 | usar_retinol, usar_peptidos, usar_vitamina_c, usar_limpiador_suave, rutina_minimalista, usar_protector_solar | ✓ Todas derivadas | ✓ |
| 5 | Piel grasa con poros dilatados | piel_grasa, objetivo_poros | R11, R15 | usar_niacinamida, usar_acido_salicilico, doble_limpieza, usar_mascarilla_arcilla, usar_protector_solar | ✓ Todas derivadas | ✓ |
| 6 | Caso sin conclusión útil (solo edad, sin tipo de piel) | edad_adulto | R15 | Solo usar_protector_solar (regla universal) | ✓ Sistema responde con SPF universal | ✓ |

---

## Detalle de cada caso

### Caso 1 — Piel grasa + acné (joven)
- **Hechos iniciales:** `piel_grasa=True`, `objetivo_anti_acne=True`, `edad_joven=True`
- **Reglas activadas:** R1, R15
- **Conclusiones derivadas:** `usar_limpiador_salicilico`, `usar_niacinamida`, `usar_hidratante_ligero`, `usar_mascarilla_arcilla`, `usar_protector_solar`
- **Justificación:** R1 se activa porque ambas condiciones (piel_grasa ∧ objetivo_anti_acne) son verdaderas. R15 aplica universalmente.
- **Certeza promedio:** 97.5%

### Caso 2 — Piel seca + hidratación (adulta)
- **Hechos iniciales:** `piel_seca=True`, `objetivo_hidratacion=True`, `edad_adulto=True`
- **Reglas activadas:** R2, R15
- **Conclusiones derivadas:** `usar_acido_hialuronico`, `usar_ceramidas`, `usar_hidratante_rico`, `usar_protector_solar`
- **Certeza promedio:** 98.5%

### Caso 3 — Piel sensible con acné (sin retinol)
- **Hechos iniciales:** `piel_sensible=True`, `objetivo_anti_acne=True`, `edad_joven=True`
- **Reglas activadas:** R4, R12, R15
- **Conclusiones derivadas:** `usar_centella_asiatica`, `usar_ceramidas`, `evitar_retinol`, `rutina_minimalista`, `usar_acido_salicilico`, `usar_limpiador_suave`, `usar_protector_solar`
- **Caso de borde:** Acné sin poder usar limpiador salicílico fuerte. R12 es más conservadora que R1.
- **Certeza promedio:** 94.3%

### Caso 4 — Madura, anti-edad avanzado
- **Hechos iniciales:** `objetivo_anti_envejecimiento=True`, `edad_maduro=True`, `piel_normal=True`
- **Reglas activadas:** R6, R14, R15
- **Conclusiones derivadas:** `usar_retinol`, `usar_peptidos`, `usar_vitamina_c`, `usar_limpiador_suave`, `usar_hidratante_ligero`, `rutina_minimalista`, `usar_protector_solar`
- **Certeza promedio:** 95.3%

### Caso 5 — Poros dilatados (piel grasa)
- **Hechos iniciales:** `piel_grasa=True`, `objetivo_poros=True`
- **Reglas activadas:** R11, R15
- **Conclusiones derivadas:** `usar_niacinamida`, `usar_acido_salicilico`, `doble_limpieza`, `usar_mascarilla_arcilla`, `usar_protector_solar`
- **Certeza promedio:** 95.5%

### Caso 6 — Sin conclusión (solo edad)
- **Hechos iniciales:** `edad_adulto=True`
- **Reglas activadas:** R15 únicamente (universal)
- **Conclusiones:** `usar_protector_solar` solamente
- **Comportamiento esperado:** El sistema responde con el mínimo (SPF universal) e indica que se necesitan más datos.
- **Certeza:** 100%

---

## Análisis de cobertura

| Categoría de regla | Reglas | Casos que la ejercitan |
|--------------------|--------|----------------------|
| Control de Acné | R1 | Casos 1, 3 |
| Hidratación Intensa | R2 | Caso 2 |
| Piel Mixta | R3 | — |
| Piel Sensible | R4 | Caso 3 |
| Hidratación Sensible | R5 | — |
| Anti-aging Avanzado | R6 | Caso 4 |
| Anti-aging Preventivo | R7 | — |
| Prevención Temprana | R8 | — |
| Luminosidad | R9 | — |
| Manchas | R10 | — |
| Poros Dilatados | R11 | Caso 5 |
| Acné Sensible | R12 | Caso 3 |
| Piel Madura Seca | R13 | — |
| Piel Normal | R14 | Caso 4 |
| SPF Universal | R15 | Todos |
