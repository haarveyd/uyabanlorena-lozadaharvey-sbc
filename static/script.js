/* ════════════════════════════════════════════════════════════
   LUMIS — Sistema Experto de Skincare
   Lógica de interfaz: wizard, llamadas API, renderizado
   ════════════════════════════════════════════════════════════ */

// ── Estado global ────────────────────────────────────────────
let state = {
  currentStep: 1,
  tipoPiel: null,
  objetivos: [],
  edad: null,
  lastResult: null   // guarda la última respuesta del servidor
};

// ════════════════════════════════════════════════════════════
// NAVEGACIÓN DEL WIZARD
// ════════════════════════════════════════════════════════════

function scrollToForm() {
  document.getElementById('form-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function goToStep(n) {
  if (n < 1 || n > 3) return;

  // Ocultar todos los pasos
  [1, 2, 3].forEach(i => {
    const el = document.getElementById(`step-${i}`);
    if (el) el.classList.add('hidden');
  });

  // Mostrar el paso objetivo
  const target = document.getElementById(`step-${n}`);
  if (target) {
    target.classList.remove('hidden');
    target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  state.currentStep = n;
  updateProgressUI(n);
}

function updateProgressUI(active) {
  [1, 2, 3].forEach(i => {
    const el = document.getElementById(`ps-${i}`);
    if (!el) return;
    el.classList.remove('active', 'done');
    if (i < active)  el.classList.add('done');
    if (i === active) el.classList.add('active');
  });
}

// ════════════════════════════════════════════════════════════
// LISTENERS DE SELECCIÓN
// ════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

  // ── Tipo de piel ────────────────────────────────────────────
  document.querySelectorAll('input[name="tipo_piel"]').forEach(radio => {
    radio.addEventListener('change', () => {
      state.tipoPiel = radio.value;
      document.getElementById('btn-next-1').disabled = false;
    });
  });

  // ── Objetivos (máx 3) ──────────────────────────────────────
  document.querySelectorAll('input[name="objetivos"]').forEach(cb => {
    cb.addEventListener('change', () => {
      const checked = [...document.querySelectorAll('input[name="objetivos"]:checked')];
      state.objetivos = checked.map(c => c.value);

      // Limite de 3
      if (state.objetivos.length >= 3) {
        document.querySelectorAll('input[name="objetivos"]:not(:checked)').forEach(other => {
          other.closest('.goal-card').classList.add('disabled-card');
        });
      } else {
        document.querySelectorAll('.goal-card').forEach(card => {
          card.classList.remove('disabled-card');
        });
      }

      document.getElementById('btn-next-2').disabled = state.objetivos.length === 0;
    });
  });

  // ── Edad ────────────────────────────────────────────────────
  document.querySelectorAll('input[name="edad"]').forEach(radio => {
    radio.addEventListener('change', () => {
      state.edad = radio.value;
      document.getElementById('btn-analizar').disabled = false;
    });
  });

});

// ════════════════════════════════════════════════════════════
// ANÁLISIS — LLAMADA AL BACKEND
// ════════════════════════════════════════════════════════════

async function analizar() {
  // Validación final
  if (!state.tipoPiel && state.objetivos.length === 0) {
    showError('Selecciona al menos tu tipo de piel y un objetivo.');
    return;
  }

  // Estado de carga
  setLoading(true);
  hideError();

  const payload = {
    tipo_piel: state.tipoPiel,
    objetivos:  state.objetivos,
    edad:       state.edad
  };

  try {
    const res = await fetch('/diagnosticar', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok || data.error) {
      showError(data.error || 'Error al conectar con el servidor.');
      return;
    }

    if (data.sin_conclusion) {
      showError(data.mensaje);
      return;
    }

    state.lastResult = data;
    renderResults(data);

  } catch (err) {
    showError('No se pudo conectar con el servidor. Asegúrate de que Flask esté corriendo.');
  } finally {
    setLoading(false);
  }
}

function setLoading(on) {
  const btn = document.getElementById('btn-analizar');
  const txt = document.getElementById('btn-text');
  const sp  = document.getElementById('btn-spinner');
  const ic  = document.getElementById('btn-icon');

  btn.disabled = on;
  txt.textContent = on ? 'Analizando...' : 'Analizar mi piel';
  sp.classList.toggle('hidden', !on);
  ic.classList.toggle('hidden', on);
}

// ════════════════════════════════════════════════════════════
// RENDERIZADO DE RESULTADOS
// ════════════════════════════════════════════════════════════

function renderResults(data) {
  const { recomendaciones, reglas_aplicadas, certeza_promedio, hechos_iniciales } = data;

  // Ocultar formulario, mostrar resultados
  document.getElementById('form-section').classList.add('hidden');
  const sec = document.getElementById('results-section');
  sec.classList.remove('hidden');
  sec.scrollIntoView({ behavior: 'smooth', block: 'start' });

  // ── Resumen ──────────────────────────────────────────────────
  const pieles = {
    piel_grasa: 'grasa', piel_seca: 'seca', piel_mixta: 'mixta',
    piel_normal: 'normal', piel_sensible: 'sensible'
  };
  const tipoDetectado = Object.keys(pieles).find(k => hechos_iniciales[k]) || '';
  const tipoPiel = tipoDetectado ? `piel ${pieles[tipoDetectado]}` : '';
  const nReg = reglas_aplicadas.length;
  const nProd = recomendaciones.todos_los_productos.length;

  document.getElementById('results-summary').textContent =
    `${nReg} regla${nReg !== 1 ? 's' : ''} aplicada${nReg !== 1 ? 's' : ''} · ` +
    `${nProd} producto${nProd !== 1 ? 's' : ''} recomendado${nProd !== 1 ? 's' : ''}` +
    (tipoPiel ? ` · Perfil: ${tipoPiel}` : '');

  // ── Certeza ─────────────────────────────────────────────────
  const pct = Math.round(certeza_promedio * 100);
  document.getElementById('certeza-pct').textContent = `${pct}%`;
  setTimeout(() => {
    document.getElementById('certeza-fill').style.width = `${pct}%`;
  }, 200);

  // ── Advertencias ────────────────────────────────────────────
  const advWrap = document.getElementById('advertencias-wrap');
  advWrap.innerHTML = '';
  (recomendaciones.advertencias || []).forEach(adv => {
    const div = document.createElement('div');
    div.className = `adv-item ${adv.tipo}`;
    div.innerHTML = `<span>${adv.tipo === 'warning' ? '⚠️' : '💡'}</span><span>${adv.texto}</span>`;
    advWrap.appendChild(div);
  });

  // ── Rutinas ─────────────────────────────────────────────────
  renderProductList('rutina-manana', recomendaciones.rutina_manana, reglas_aplicadas, hechos_iniciales);
  renderProductList('rutina-noche',  recomendaciones.rutina_noche,  reglas_aplicadas, hechos_iniciales);

  // Extras
  const extrasWrap = document.getElementById('extras-wrap');
  if (recomendaciones.extras && recomendaciones.extras.length > 0) {
    renderProductList('rutina-extras', recomendaciones.extras, reglas_aplicadas, hechos_iniciales);
    extrasWrap.classList.remove('hidden');
  } else {
    extrasWrap.classList.add('hidden');
  }

  // ── Reglas aplicadas ────────────────────────────────────────
  renderRulesApplied(reglas_aplicadas);

  // ── Explicación completa ─────────────────────────────────────
  document.getElementById('expl-pre').textContent = data.explicacion_texto;
}

function renderProductList(containerId, products, reglas, hechos) {
  const container = document.getElementById(containerId);
  container.innerHTML = '';

  if (!products || products.length === 0) {
    container.innerHTML = '<p style="font-size:13px;color:var(--gray);text-align:center;padding:12px 0;">No aplica para tu perfil</p>';
    return;
  }

  products.forEach((prod, idx) => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <div class="pc-top">
        <div class="pc-left">
          <span class="pc-icon">${prod.icono || '✦'}</span>
          <span class="pc-step-badge">Paso ${prod.paso}</span>
        </div>
        <button class="btn-porque" onclick='openPorque("${prod.predicado}", ${JSON.stringify(reglas).replace(/'/g, "\\'")}, ${JSON.stringify(hechos).replace(/'/g, "\\'")})'>¿Por qué?</button>
      </div>
      <div class="pc-name">${prod.nombre}</div>
      <div class="pc-desc">${prod.descripcion}</div>
      <div class="pc-examples"><span>Ejemplos:</span> ${prod.ejemplos.join(' · ')}</div>
    `;
    container.appendChild(card);
  });
}

function renderRulesApplied(reglas) {
  const container = document.getElementById('rules-applied');
  container.innerHTML = '';

  reglas.forEach(r => {
    const certPct = Math.round(r.certeza * 100);
    const div = document.createElement('div');
    div.className = 'rule-item';
    div.innerHTML = `
      <div class="ri-header">
        <span class="ri-badge">${r.nombre}</span>
        <span class="ri-cat">${r.categoria}</span>
        <span class="ri-certeza">${certPct}% certeza</span>
      </div>
      <div class="ri-desc">${r.descripcion}</div>
      <div class="ri-formula">${r.si_entonces}</div>
    `;
    container.appendChild(div);
  });
}

// ════════════════════════════════════════════════════════════
// MODAL ¿POR QUÉ?
// ════════════════════════════════════════════════════════════

async function openPorque(conclusion, reglas, hechos) {
  document.getElementById('modal-title').textContent = `¿Por qué: ${conclusion.replace(/_/g, ' ')}?`;
  document.getElementById('modal-body').textContent = 'Consultando al motor de inferencia…';
  document.getElementById('modal-overlay').classList.remove('hidden');

  try {
    const res = await fetch(`/porque/${encodeURIComponent(conclusion)}`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hechos_iniciales: hechos, reglas_aplicadas: reglas })
    });
    const data = await res.json();
    document.getElementById('modal-body').textContent =
      data.explicacion || data.error || 'Sin información disponible.';
  } catch {
    document.getElementById('modal-body').textContent = 'Error al obtener la explicación.';
  }
}

function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
}

// Cerrar modal con ESC
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ════════════════════════════════════════════════════════════
// EXPLICACIÓN TOGGLE
// ════════════════════════════════════════════════════════════

function toggleExplanation() {
  const body   = document.getElementById('expl-body');
  const toggle = document.getElementById('expl-toggle');
  const hidden = body.classList.toggle('hidden');
  toggle.textContent = hidden ? 'Ver detalle ↓' : 'Ocultar ↑';
}

// ════════════════════════════════════════════════════════════
// RESET
// ════════════════════════════════════════════════════════════

function resetForm() {
  // Limpiar estado
  state = { currentStep: 1, tipoPiel: null, objetivos: [], edad: null, lastResult: null };

  // Limpiar selecciones
  document.querySelectorAll('input[name="tipo_piel"], input[name="objetivos"], input[name="edad"]')
    .forEach(el => { el.checked = false; });

  // Restaurar botones disabled
  document.getElementById('btn-next-1').disabled = true;
  document.getElementById('btn-next-2').disabled = true;
  document.getElementById('btn-analizar').disabled = true;

  // Limpiar límite de objetivos
  document.querySelectorAll('.goal-card').forEach(c => c.classList.remove('disabled-card'));

  // Ocultar resultados, mostrar formulario
  document.getElementById('results-section').classList.add('hidden');
  document.getElementById('form-section').classList.remove('hidden');

  // Volver al paso 1
  goToStep(1);
  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Ocultar explicación
  document.getElementById('expl-body').classList.add('hidden');
  document.getElementById('expl-toggle').textContent = 'Ver detalle ↓';

  hideError();
}

// ════════════════════════════════════════════════════════════
// UTILIDADES
// ════════════════════════════════════════════════════════════

function showError(msg) {
  const banner = document.getElementById('error-banner');
  document.getElementById('error-msg').textContent = msg;
  banner.classList.remove('hidden');
}

function hideError() {
  document.getElementById('error-banner').classList.add('hidden');
}
