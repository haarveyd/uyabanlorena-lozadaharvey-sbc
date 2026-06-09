# =============================================================================
# app.py — Servidor Flask
# Sistema Experto de Skincare | Inteligencia Artificial II
# Ejecutar: python app.py  (desde la carpeta skincare_expert/)
# Acceder:  http://localhost:5000
# =============================================================================

import os
import sys
import logging

from flask import Flask, render_template, request, jsonify

# Añadir src/ al path de módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from base_conocimiento import PREDICADOS, REGLAS
from motor_inferencia import (
    encadenamiento_adelante,
    explicar_razonamiento,
    porque,
    obtener_recomendaciones
)

# ─── Configuración Flask ───────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)
app.config["JSON_ENSURE_ASCII"] = False  # Permite caracteres UTF-8 en JSON

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# RUTAS
# =============================================================================

@app.route("/")
def index():
    """Página principal: formulario interactivo de skincare"""
    return render_template("index.html")


@app.route("/diagnosticar", methods=["POST"])
def diagnosticar():
    """
    Endpoint principal del sistema experto.
    Recibe hechos del usuario y devuelve rutina + explicación.

    Body JSON esperado:
        {
            "tipo_piel": "grasa" | "seca" | "mixta" | "normal" | "sensible",
            "objetivos": ["anti_acne", "hidratacion", ...],
            "edad":      "joven" | "adulto" | "maduro"
        }
    """
    try:
        datos = request.get_json(force=True)

        if not datos:
            return jsonify({"error": "No se recibieron datos en la solicitud."}), 400

        # ── Construir hechos iniciales ────────────────────────────────────────
        hechos_iniciales = {}

        tipo_piel = datos.get("tipo_piel", "").strip()
        if tipo_piel:
            hechos_iniciales[f"piel_{tipo_piel}"] = True

        objetivos = datos.get("objetivos", [])
        for obj in objetivos:
            hechos_iniciales[f"objetivo_{obj}"] = True

        edad = datos.get("edad", "").strip()
        if edad:
            hechos_iniciales[f"edad_{edad}"] = True

        # Validación mínima
        if not tipo_piel and not objetivos:
            return jsonify({
                "error": "Selecciona al menos el tipo de piel o un objetivo."
            }), 400

        logger.info(f"Hechos iniciales recibidos: {hechos_iniciales}")

        # ── Ejecutar motor de inferencia ──────────────────────────────────────
        hechos_finales, reglas_aplicadas = encadenamiento_adelante(REGLAS, hechos_iniciales)

        # ── Generar salidas ───────────────────────────────────────────────────
        recomendaciones = obtener_recomendaciones(hechos_finales, hechos_iniciales)
        explicacion = explicar_razonamiento(reglas_aplicadas)

        # Caso sin conclusión
        if not reglas_aplicadas and not recomendaciones["todos_los_productos"]:
            return jsonify({
                "sin_conclusion": True,
                "mensaje": (
                    "El sistema no pudo derivar recomendaciones con los datos ingresados. "
                    "Intenta seleccionar un tipo de piel y al menos un objetivo."
                )
            })

        certeza_promedio = (
            sum(r["certeza"] for r in reglas_aplicadas) / len(reglas_aplicadas)
            if reglas_aplicadas else 0.0
        )

        # ── Serializar respuesta ──────────────────────────────────────────────
        respuesta = {
            "exito": True,
            "hechos_iniciales": {k: v for k, v in hechos_iniciales.items() if v},
            "certeza_promedio": round(certeza_promedio, 4),
            "reglas_aplicadas": [
                {
                    "nombre": r["nombre"],
                    "descripcion": r["descripcion"],
                    "categoria": r["categoria"],
                    "certeza": r["certeza"],
                    "si_entonces": r["si_entonces"],
                    "justificacion": r["justificacion"],
                    "condiciones": r["condiciones_activadas"],
                    "conclusiones": r["conclusiones_derivadas"],
                    "iteracion": r["iteracion"]
                }
                for r in reglas_aplicadas
            ],
            "recomendaciones": recomendaciones,
            "explicacion_texto": explicacion
        }

        return jsonify(respuesta)

    except Exception as exc:
        logger.exception("Error durante el diagnóstico")
        return jsonify({"error": f"Error interno: {str(exc)}"}), 500


@app.route("/porque/<conclusion>", methods=["POST"])
def explicar_porque(conclusion):
    """
    Endpoint de explicación para una conclusión específica (botón '¿Por qué?').

    Body JSON esperado:
        {
            "hechos_iniciales": {...},
            "reglas_aplicadas": [...]
        }
    """
    try:
        datos = request.get_json(force=True)
        hechos_iniciales = datos.get("hechos_iniciales", {})
        reglas_aplicadas = datos.get("reglas_aplicadas", [])

        # Reconstruir estructura esperada por porque()
        reglas_reconstruidas = []
        for r in reglas_aplicadas:
            reglas_reconstruidas.append({
                **r,
                "condiciones_activadas": r.get("condiciones", []),
                "conclusiones_derivadas": r.get("conclusiones", [])
            })

        texto = porque(conclusion, hechos_iniciales, reglas_reconstruidas)
        return jsonify({"conclusion": conclusion, "explicacion": texto})

    except Exception as exc:
        logger.exception("Error en /porque")
        return jsonify({"error": str(exc)}), 500


@app.route("/predicados")
def ver_predicados():
    """Devuelve la definición formal de todos los predicados (utilidad de documentación)."""
    return jsonify(PREDICADOS)


@app.route("/reglas")
def ver_reglas():
    """Devuelve todas las reglas de la base de conocimiento."""
    reglas_serializables = [
        {
            "nombre": r["nombre"],
            "categoria": r["categoria"],
            "descripcion": r["descripcion"],
            "condiciones": r["condiciones"],
            "conclusiones": r["conclusiones"],
            "certeza": r["certeza"],
            "si_entonces": r["si_entonces"],
            "justificacion": r["justificacion"]
        }
        for r in REGLAS
    ]
    return jsonify(reglas_serializables)


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  Sistema Experto de Skincare — IA II")
    print("  Servidor corriendo en http://localhost:5000")
    print("=" * 55 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
