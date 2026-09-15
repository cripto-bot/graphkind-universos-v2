# Estrategia de visibilidad (sin arXiv)

**laboratorio GraphKind · 2026-09-14 · estado verificado y plan concreto**

> Objetivo: que el trabajo sea **encontrable y citable** por buscadores
> académicos y generales sin pasar por la burocracia de arXiv.

---

## 1. Estado actual (verificado)

| canal | estado | evidencia |
|---|---|---|
| **OpenAlex** | **indexado** ✓ | `api.openalex.org/works/https://doi.org/10.5281/zenodo.22747350` → tipo *software*, 2026 |
| **Zenodo (DataCite)** | publicado ✓ | concept DOI `10.5281/zenodo.22747350`; alimenta DataCite Commons, OpenAIRE, BASE |
| **GitHub Pages** | **live** ✓ | `cripto-bot.github.io/graphkind-universos-v2` con `citation_*`, Open Graph, JSON-LD (`ScholarlyArticle` + `Dataset`), `robots.txt`, `sitemap.xml` |
| **Paper PDF** | ✓ | `paper/graphkind-v2.pdf` (A4, 15 páginas, figuras incluidas) |
| **HuggingFace** | ✓ | Space con tags + OG; dataset con tags + DOI + thumbnail |
| **Semantic Scholar** | **no indexado** ✗ | la API responde *not found* → pedir indexación |
| **Google Scholar** | pendiente de rastreo | requiere PDF + `citation_*` (ya están) y tiempo de crawleo |

**Conclusión**: la base técnica está. Falta **difusión** (depósitos espejo,
comunidad, backlinks) y **pedir indexación** donde no es automática.

---

## 2. Palancas, por costo/beneficio

### A. Preprint servers sin burocracia (alternativas a arXiv)

| servidor | costo | qué aporta |
|---|---|---|
| **HAL** (hal.science) | cuenta + depósito (10 min) | archivo nacional francés, DOI propio, cosechado por Scholar/OpenAIRE |
| **OSF Preprints** (osf.io/preprints) | cuenta + depósito | DOI, moderación liviana, Scholar |
| **Preprints.org** (MDPI) | cuenta + depósito | rápido, DOI, Scholar |
| **TechRxiv** (IEEE) | cuenta + depósito | marco de ingeniería/CS |
| **ResearchGate** | subida directa | audiencia académica, descubrimiento |

Recomendado: **HAL + OSF** con el mismo PDF (dos espejos independientes).

### B. Pedir indexación (5 minutos cada una)

- **Semantic Scholar**: formulario de sugerencia (FAQ → *How can I add my paper?*).
- **Google Search Console**: verificar `cripto-bot.github.io` + enviar
  `sitemap.xml`.
- **Bing Webmaster Tools**: ídem.

### C. Comunidad (tráfico + backlinks)

- **Show HN** con el Space (el demo interactivo es el gancho, no el paper).
- **Lobsters** (tags `math`, `cs`), **Reddit** (`r/math`, `r/computerscience`;
  respetar reglas de autopromoción), **Mathstodon/Bluesky** (`#math`
  `#graphtheory`).
- **MathOverflow/StackExchange**: respuestas genuinas sobre WL/complemento
  citando el resultado (sin spam).

### D. Software

- **PyPI**: publicar el kernel (`wl`/`k-FWL`/kinds) como paquete → audiencia
  de desarrolladores + cita de software.
- **JOSS** (*Journal of Open Source Software*): publicación revisada del
  software, sin arXiv.

### E. Backlinks de alto valor

- **Wikipedia**: citar el DOI en *Weisfeiler–Leman* o *Graph isomorphism*
  **si es pertinente** (cuidado con conflicto de interés: aportar la cifra
  exacta, no promocionar).
- **Wikidata**: ítem del trabajo (si cumple notabilidad).
- **Listas `awesome-*`** de teoría de grafos / refinamiento.

### F. Contenido

- **Blog post accesible** (*el mapa y no la respuesta*) en dev.to / Hashnode /
  Medium, enlazando paper, Space y dataset.
- Video corto (opcional): 3 minutos mostrando la Demo 2 (Rook/Shrikhande).

---

## 3. Plan de 7 días

1. **Día 1** — PDF + `citation_*` + Zenodo con el PDF (hecho); Search Console
   + Bing (sitemap).
2. **Día 2** — HAL + OSF (subir el PDF).
3. **Día 3** — Show HN + Lobsters + Mastodon/Bluesky.
4. **Día 4** — Reddit + blog post.
5. **Día 5** — Semantic Scholar (pedido) + Wikipedia/Wikidata (si aplica).
6. **Día 6** — PyPI del kernel.
7. **Día 7** — medir y ajustar.

## 4. Métricas a seguir

OpenAlex (trabajos citados, vistas) · Zenodo (vistas/descargas) ·
HuggingFace (downloads/likes del dataset y del Space) · GitHub
(clones/visitas) · Search Console (impresiones/clics) · referrers del blog.

---

## 5. Lo que NO hacemos

- No compramos visibilidad ni usamos granjas de citas.
- No spameamos foros: cada aparición aporta contenido (la cifra, el demo).
- No prometemos el invariante completo: el mensaje es *el mapa*, y eso es
  también lo que hace creíble la difusión.
