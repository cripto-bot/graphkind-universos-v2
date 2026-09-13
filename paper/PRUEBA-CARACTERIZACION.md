# La caracterización Sₙ·K — prueba estructural y estado

> Fabrica: GraphKind · 2026-09-10 · EXP-110/111

## El enunciado

Con WL simétrico (cuenta `in` y `out` por color, grados crudos):

    T4(ι, f) vive ⟺ ι ∈ Sₙ·K  y  (ι cambia el par ⟹ f(1) ≠ f(2))
    K = {id, comp_dir, transp, comp_transp} ≅ Z₂×Z₂

donde "vive" = la partición WL se preserva para todo digrafo.

## (⇐) Lo que está demostrado

Sea ι = σ∘s∘c con σ∈Sₙ, s∈{0,1} (swap global in/out), c∈{0,1}
(complementación uniforme de todos los pares).

1. **σ (relabel)**: el WL es invariante por isomorfismo: la coloración
   se transporta biyectivamente; la partición (multiset de tamaños) es
   idéntica. Vale para toda f.
2. **s (swap in/out)**: intercambia los conteos de cada nodo,
   (in_D, out_D) → (out_D, in_D); el perfil se transforma por el swap
   (f(a),f(b)) → (f(b),f(a)), que es una biyección de perfiles. La
   partición se preserva. Vale para toda f.
3. **c (complemento uniforme)**: para cada clase D, el conteo de
   vecinos se transforma m → |D| − m (o |D|−1−m en la clase propia, sin
   self-loops): una biyección de conteos. La partición se preserva
   **siempre que f distinga 1 de 2** — condición mínima verificada
   (con f(1)=f(2) el contraejemplo existe: EXP-102, n=6).

Por lo tanto Sₙ·K ⊆ supervivientes. La suficiencia de `f(1)≠f(2)` para
**toda** f (no solo las del catálogo) queda como parte del teorema
candidato (verificado en 102/102 + 87/87 + 94/94 + 528/528).

## (⇒) Lo verificado

| cámara | resultado |
|---|---|
| n=3 afín exhaustiva (110) | 140 viven (el WL chico es ciego: rango) |
| **n=4 inducidas exhaustiva (111-B)** | viven **96** (f=id) y **48** (const1), **todas uniformes, 0 fuera** |
| **n=5 inducidas dirigida (111-C)** | **7680 con testigo**; 480 sin testigo = uniformes (104 involuciones válidas + 376 relabels no involutivos) |
| fuera del espacio (111-D) | 10000 iotas afines aleatorias: **10000 con testigo** |
| real (108/109) | moléculas: 100/100; CST: comp_dir dual + T4 94/94 |

## Lo que queda abierto (declarado)

1. (⇒) para todo n: verificado en n≤4 exhaustivo y n=5 dirigido
   (existencia de testigo válido por iota: 6424/6424). **Receta
   universal: no hallada** — la mejor de la familia probada es `ciclo`
   (99.63%); el intento "defecto + aislado" quedó **retirado** (medía
   la iota extendida, no la de n: EXP-113 fase 3, control 52/104).
2. (⇐) con c=1 y f arbitraria con f(1)≠f(2): verificado en los
   catálogos; falta la demostración para f arbitraria.

## Rigor registrado

- **Rango**: n=3 es ciego (140 > 96): la caracterización fina requiere
  n≥4. El testigo de n=5 incluye 200 grafos aleatorios + ciclos k≥2 +
  estrellas: **el ciclo k=1 era un self-loop y daba falsos positivos**
  (bug corregido: la identidad "fallaba").
