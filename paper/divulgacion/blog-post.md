# El mapa y no la respuesta: dónde se vuelve incompleto el invariante de isomorfismo

*Un laboratorio mide la frontera de la completitud, ordena los observadores
y demuestra que la incompletitud es del par (universo, observador).*

Hay una pregunta que la matemática arrastra desde hace cincuenta años:

> ¿Existe un invariante **completo** para el isomorfismo de grafos — una
> huella que distinga todo par de grafos no isomorfos — y que se calcule
> en tiempo polinómico?

Nadie la respondió. Lo que hicimos en el laboratorio **GraphKind** fue otra
cosa: **darle coordenadas**.

## Lo que medimos

- **La frontera**: sobre *todos* los grafos hasta n=8 (76 205 685 pares), la
  familia `{WL, 2-WL, 3-WL}` da **cero colisiones**. En n=10 (12 005 168
  grafos, barrido exhaustivo) también: la primera incompletitud **no está
  ahí**. La primera falla conocida sigue en **n=16**, con el par
  **Rook/Shrikhande** — dos grafos cospectrales que 3-WL no separa.
- **El retículo de observadores**: WL = 2-WL en n≤9; `IR₁` falla donde falla
  3-WL; `IR₂` se comporta como 3-FWL ≡ 4-WL; la forma normal de Smith del
  Laplaciano separa Rook/Shrikhande. El orden entre observadores, medido
  lado a lado, no estaba tabulado así.
- **La incompletitud es del par**: no del objeto. Cambiá el universo
  (estándar, dinámico, aleatorio, multicapa, hipergrafo) y la respuesta
  cambia.
- **El precio de la simetría**: imponer invariancia bajo complemento (el
  teorema T4) fusiona exactamente **6 168 pares** en n≤8. Y hay una tensión
  estructural: **un invariante completo no puede ser complemento-invariante**.
- **Una ley de composición**: en objetos multicapa, T4 vive si y solo si el
  complemento actúa uniformemente sobre las capas (grupo `ℤ₂^L ⋊ S_L`).
- **Un reparo**: en hipergrafos de aridad mezclada, el dual por aridad
  restaura la invariancia (261 000 casos, cero testigos de fallo).

## Lo que NO hicimos

No encontramos el invariante completo universal. No probamos que sea
imposible. No resolvimos P vs NP. No medimos la frontera exacta entre n=11
y n=15 (es inabordable por barrido). La dirección difícil de la
caracterización multicapa sigue abierta.

Eso también es el resultado: **un mapa, no una respuesta**. Y los mapas, en
matemática, redirigen la pregunta.

## Probalo vos mismo

El demo es interactivo y corre el mismo refinamiento que el motor, en tu
navegador:

- **T4 ronda a ronda**: movés la ronda k y ves que la *partición* de G y su
  complemento coincide, mientras las etiquetas de color difieren (son
  hashes arbitrarios).
- **¿Lo separa?**: elegís un par (C₆/2·C₃, Petersen/prisma,
  Rook/Shrikhande) y un observador (WL, k=2, k=3), y el navegador computa.

👉 **[Demo: GraphKind — El mapa y no la respuesta](https://huggingface.co/spaces/Jose-dev/graphlab-discoveries-demo)**

## Todo abierto

- **Paper (PDF, 15 páginas)**: <https://cripto-bot.github.io/graphkind-universos-v2/paper/graphkind-v2.pdf>
- **DOI (datos y código, CC-BY-4.0)**: <https://doi.org/10.5281/zenodo.22747350>
- **Código**: <https://github.com/cripto-bot/graphkind-universos-v2>
- **Dataset**: <https://huggingface.co/datasets/Jose-dev/graphkind-universos>
- **Kernel en Python** (`pip install graphkind-wl`): <https://pypi.org/project/graphkind-wl/>

Cada cifra de este post sale de un *freeze* del laboratorio: un resultado
congelado antes de interpretarlo, con control negativo. Nada está
redondeado a favor de la historia.
