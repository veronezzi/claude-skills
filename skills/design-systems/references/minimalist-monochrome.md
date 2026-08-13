# Design System: Minimalist Monochrome

Paleta estritamente preto e branco, tipografia serifada oversized, zero border-radius, sem sombras, linhas e inversão de cor no lugar de cor de destaque, transições instantâneas. Estética editorial, luxuosa e austera — ver `SKILL.md` pra saber quando usar este sistema em vez de outro.

## Filosofia de design

### Princípio central

**Redução à essência.** Minimalist Monochrome reduz o design aos elementos mais fundamentais: preto, branco e tipografia. Não há cores de destaque pra se esconder atrás, sem gradientes pra suavizar bordas, sem sombras pra criar falsa profundidade. Toda decisão de design precisa se sustentar sozinha. Isso é design como disciplina, onde a contenção se torna a forma máxima de expressão.

### Vibe visual

**Palavras-chave emocionais**: Austero, autoritário, atemporal, editorial, intelectual, dramático, refinado, cru, confiante, inegociável.

Esta é a linguagem visual de:
- Editoriais de moda de alto padrão (capas da Vogue, Harper's Bazaar)
- Monografias de arquitetura e catálogos de museu
- Identidades de marcas de luxo (Chanel, Celine, Bottega Veneta)
- Design de livro premiado e tipografia fina
- Materiais de exposição de galeria

O design comanda respeito através da sua confiança. Não precisa de cor pra ser interessante — usa escala, contraste, ritmo e espaço negativo pra criar drama visual.

### O que este design NÃO é

- Colorido ou lúdico
- Suave, arredondado ou amigável
- Baseado em gradiente ou com cores de destaque
- Pesado em sombra ou "elevado"
- Genérico ou parecido com template
- Poluído ou apinhado
- Parecido com "Minimalist Modern" (sem destaque azul, sem gradientes, sem cantos arredondados)

### O DNA do Minimalist Monochrome

**1. Paleta puramente preto e branco.** Sem cinzas pra elementos primários — use preto verdadeiro (`#000000`) e branco verdadeiro (`#FFFFFF`). Cinza é reservado só pra texto secundário e bordas. O contraste cru cria impacto visual imediato e força decisões deliberadas de hierarquia.

**2. Tipografia serifada como protagonista.** Diferente do minimalismo sans-serif moderno, este estilo abraça tipos clássicos serifados. A serifa adiciona sofisticação, peso editorial e elegância atemporal. Tipografia não é só conteúdo — é o elemento visual primário.

**3. Escala tipográfica oversized.** Títulos não só informam — dominam. Espere tamanhos 8xl, 9xl e maiores. Palavras viram elementos gráficos. Uma única palavra ou frase curta pode preencher a largura inteira do viewport.

**4. Sistema visual baseado em linhas.** Em vez de formas preenchidas, sombras ou fundos, este design usa linhas: hairlines, regras grossas, bordas, sublinhados, riscados. Linhas criam estrutura sem massa.

**5. Precisão geométrica cortante.** Zero border-radius em tudo. Cantos perfeitos de 90 graus. Alinhamentos precisos. A geometria é arquitetônica — pense Bauhaus encontrando design editorial de impresso.

**6. Espaço negativo dramático.** Espaço em branco não é vazio — é ativo. Margens e paddings generosos criam respiro que torna os elementos pretos mais impactantes. A página respira.

**7. Inversão para ênfase.** Em vez de cores de destaque, use inversão de cor (fundo preto, texto branco) pra destacar elementos importantes. Isso cria drama sem quebrar a regra do monocromático.

### Diferenciação do Minimalist Modern

| Aspecto | Minimalist Modern | Minimalist Monochrome |
|---|---|---|
| Cores | Destaque azul + gradientes | Só preto e branco |
| Tipografia | Sans-serif (Inter) | Serifada (Playfair Display) |
| Cantos | Arredondados (lg, xl, 2xl) | Cortantes (0px em tudo) |
| Profundidade | Sombras, glows, elevação | Plano, 2D, sem sombras |
| Elementos visuais | Preenchimento gradiente, ícones coloridos | Linhas, bordas, tipografia |
| Vibe | Tech contemporânea | Luxo editorial |
| Personalidade | Confiante e acessível | Austera e imponente |

---

## Sistema de design tokens

### Cores (estritamente monocromático)

```
background:       #FFFFFF (branco puro)
foreground:        #000000 (preto puro)
muted:              #F5F5F5 (quase-branco pra fundos sutis)
mutedForeground:    #525252 (cinza escuro pra texto secundário)
accent:             #000000 (o preto É o destaque)
accentForeground:   #FFFFFF (branco sobre preto)
border:             #000000 (bordas pretas)
borderLight:        #E5E5E5 (cinza claro pra divisores sutis)
card:               #FFFFFF (cards brancos)
cardForeground:     #000000 (texto preto)
ring:               #000000 (focus ring preto)
```

**Regra**: nenhuma outra cor. Nunca. A paleta é absoluta.

### Tipografia

**Stack de fontes**:
- **Display/títulos**: `"Playfair Display", Georgia, serif` — serifada elegante, alto contraste, itálicos bonitos.
- **Corpo**: `"Source Serif 4", Georgia, serif` — serifada altamente legível pra texto longo.
- **Mono/labels**: `"JetBrains Mono", monospace` — pra datas, metadados, detalhes técnicos.

**Escala tipográfica** (faixa dramática):
```
xs:   0.75rem  (12px) — rodapé fino, metadados
sm:   0.875rem (14px) — legendas, labels
base: 1rem     (16px) — texto de corpo mínimo
lg:   1.125rem (18px) — texto de corpo preferido
xl:   1.25rem  (20px) — parágrafo de abertura
2xl:  1.5rem   (24px) — introdução de seção
3xl:  2rem     (32px) — subtítulos
4xl:  2.5rem   (40px) — títulos de seção
5xl:  3.5rem   (56px) — títulos de página
6xl:  4.5rem   (72px) — subtítulos de hero
7xl:  6rem     (96px) — títulos de hero
8xl:  8rem     (128px) — títulos de display
9xl:  10rem    (160px) — declarações oversized
```

**Tracking e leading**:
- Títulos: `tracking-tight` (-0.025em) ou `tracking-tighter` (-0.05em)
- Corpo: `tracking-normal` (0)
- Small caps/labels: `tracking-widest` (0.1em)
- Line-height: `leading-none` (1) pra display, `leading-relaxed` (1.625) pra corpo

### Border radius

```
TODOS OS VALORES: 0px
```

Sem exceções. Todo elemento tem cantos cortantes de 90 graus. Isso não é negociável e define o caráter arquitetônico do estilo.

### Bordas e linhas

```
hairline: 1px solid #E5E5E5  (divisores sutis)
thin:     1px solid #000000  (bordas padrão)
medium:   2px solid #000000  (bordas de ênfase)
thick:    4px solid #000000  (regras pesadas, divisores de seção)
ultra:    8px solid #000000  (impacto máximo)
```

**Uso**:
- Regras horizontais entre seções (thick ou ultra)
- Divisores verticais entre colunas (thin)
- Bordas de card (thin ou medium)
- Sublinhado de link (thin, no hover)

### Sombras

```
NENHUMA
```

Este design tem zero drop shadow. Profundidade é criada através de:
- Inversão de cor (troca preto/branco)
- Variação de peso de borda
- Contraste de escala
- Espaço negativo

### Texturas e padrões

**CRÍTICO**: estas texturas são OBRIGATÓRIAS pra evitar design chapado. Aplique estrategicamente por seção.

**Padrão primário: linhas horizontais (global)**
```css
background-image: repeating-linear-gradient(
  0deg,
  transparent,
  transparent 1px,
  #000 1px,
  #000 2px
);
background-size: 100% 4px;
opacity: 0.015;
```

**Padrão secundário: grid (pra seções editoriais como detalhe de produto)**
```css
background-image:
  linear-gradient(#00000008 1px, transparent 1px),
  linear-gradient(90deg, #00000008 1px, transparent 1px);
background-size: 40px 40px;
opacity: 0.015;
```

**Linhas diagonais (pra seções de processo/timeline)**
```css
background-image: repeating-linear-gradient(
  45deg,
  transparent,
  transparent 40px,
  #00000008 40px,
  #00000008 42px
);
opacity: 0.01;
```

**Textura de ruído (global, pra qualidade tipo papel)**
```css
background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
opacity: 0.02;
```

**Texturas de seção invertida**

Pra fundos escuros (Stats, CTA final), use texturas baseadas em branco:

```css
/* linhas verticais pra Stats */
background-image: repeating-linear-gradient(
  90deg,
  transparent,
  transparent 1px,
  #fff 1px,
  #fff 2px
);
background-size: 4px 100%;
opacity: 0.03;

/* gradiente radial pro CTA final */
background-image: radial-gradient(
  circle at top center,
  #ffffff,
  transparent 70%
);
opacity: 0.05;
```

---

## Estilização de componentes

### Botões

**Botão primário**:
```
- Fundo: #000000 (preto)
- Texto: #FFFFFF (branco)
- Borda: nenhuma
- Padding: px-8 py-4 (generoso)
- Fonte: uppercase, tracking-widest, font-medium, text-sm
- Hover: inverte pra fundo branco, texto preto, borda preta
- Transição: instantânea (0ms ou no máximo 100ms)
```

**Botão secundário/outline**:
```
- Fundo: transparente
- Texto: #000000
- Borda: 2px solid #000000
- Hover: preenche de preto, texto branco
```

**Botão ghost**:
```
- Fundo: transparente
- Texto: #000000
- Borda: nenhuma
- Decoração de texto: sublinhado no hover
- Estilo: parece um link de texto
```

**Formato de botão**: sempre retangular, nunca arredondado. Considere adicionar uma seta pequena (→) pra CTAs.

### Cards/containers

**Card padrão**:
```
- Fundo: #FFFFFF
- Borda: 1px solid #000000
- Padding: p-6 ou p-8
- Sem sombra, sem raio
```

**Card invertido** (pra ênfase):
```
- Fundo: #000000
- Texto: #FFFFFF
- Borda: nenhuma
- Use com moderação, só pra conteúdo destacado
```

**Card sem borda**:
```
- Sem borda, sem fundo
- Conteúdo separado por espaço em branco generoso
- Use regras horizontais acima/abaixo se necessário
```

### Inputs

**Text input**:
```
- Fundo: #FFFFFF
- Borda: 2px solid #000000 (só embaixo, ou completa)
- Sem raio
- Placeholder: #525252 itálico
- Focus: borda engrossa pra 3px ou 4px
- Sem focus ring colorido — só mudança de borda
```

**Textarea**: mesmo padrão do input, com alça de resize visível.

---

## Estratégia de layout

### Container
```
max-width: max-w-6xl (72rem / 1152px)
padding: px-6 md:px-8 lg:px-12
```

### Espaçamento de seção
```
Padding vertical: py-24 md:py-32 lg:py-40
Entre seções: regra horizontal grossa (4px ou 8px preto)
```

### Sistema de grid

- Use CSS Grid pra controle preciso
- Grid base de 12 colunas pra flexibilidade
- Alinhamento forte ao ritmo vertical

---

## Efeitos e animação

**Filosofia de movimento**: **mínima e instantânea**

Este design favorece quietude e mudanças de estado instantâneas. Quando existe animação, ela é:
- **Instantânea**: transições de 0-100ms no máximo
- **Binária**: estados nítidos de on/off, não graduais
- **Proposital**: só pra mudanças de estado (hover, focus)

**Efeitos de hover (aplicados)**:
- **Cards/features**: inversão completa de cor (fundo, texto, bordas) com transição de 100ms
- **Botões**: inversão de cor com `transition-none` pra feedback instantâneo
- **Imagens de blog**: borda engrossa (2px → 4px), imagem escala 105% e remove grayscale (300ms)
- **Links**: aparecimento de sublinhado (instantâneo)
- **Depoimentos**: opacidade da aspas aumenta, borda inferior engrossa

**Estados de focus (obrigatórios pra acessibilidade)**:
- **Botões**: outline sólido de 3px com offset de 3px
- **Inputs**: borda engrossa de 2px pra 4px (só embaixo)
- **Links**: borda aparece/engrossa
- **Elementos interativos**: outline sólido de 3px com offset de 2px
- Todos os outlines usam `focus-visible` pra evitar outline em clique de mouse

**Implementações específicas**:
```tsx
// Hover de feature card
className="group bg-[var(--background)] p-8 transition-colors duration-100 hover:bg-[var(--foreground)] hover:text-[var(--background)]"

// Hover de imagem de blog
className="border-2 transition-all duration-100 group-hover:border-[4px]"
className="grayscale transition-all duration-300 group-hover:scale-105 group-hover:grayscale-0"

// Hover de depoimento
className="group-hover:opacity-20 transition-opacity duration-100" // aspas
className="transition-all duration-100 group-hover:border-t-[3px]" // borda
```

**Não**:
- Animações bouncy
- Elementos flutuantes
- Parallax scrolling
- Funções de easing lentas
- Animações de gradiente

---

## Iconografia

**Estilo**: contornado, traço fino (`strokeWidth`: 1 ou 1.5)

**Uso**:
- Ícones dentro de círculos com traço preto, preenchimento branco
- Ou standalone sem container
- Tamanho: consistente, 20px ou 24px
- Cor: sempre preto (`#000000`)

**Configuração Lucide Icons**:
```tsx
<Icon size={20} strokeWidth={1.5} className="text-black" />
```

---

## Estratégia responsiva

**Adaptações mobile**:
- Manter cantos cortantes e paleta preto/branco
- Reduzir títulos oversized (9xl → 5xl no mobile)
- Empilhar colunas verticalmente
- Bordas viram regras horizontais full-width
- Espaçamento vertical generoso mantido

**Princípio-chave**: o drama monocromático precisa sobreviver no mobile. Não caia em padrões mobile genéricos por padrão.

---

## Acessibilidade

**Contraste**: preto puro sobre branco excede os requisitos WCAG AAA (razão 21:1).

**Estados de focus (OBRIGATÓRIOS em todo elemento interativo)**:
```
Botões e elementos interativos primários:
- Outline: 3px solid #000000
- Outline-offset: 3px
- Use focus-visible pra evitar outline em clique de mouse

Text inputs:
- Borda engrossa de 2px pra 4px no focus
- Só borda inferior
- Sem outline (mudança de borda já é suficiente)

Links de navegação:
- Borda aparece/engrossa no focus-visible
- Consistente com o estado de hover

Elementos interativos secundários (ícones sociais, botões de FAQ):
- Outline: 3px solid #000000
- Outline-offset: 2px
```

**Implementação**:
```tsx
// Focus de botão
focus-visible:outline focus-visible:outline-3 focus-visible:outline-[var(--foreground)] focus-visible:outline-offset-3

// Focus de input
focus:border-b-[4px] focus:outline-none focus-visible:border-b-[4px]

// Focus de link
focus-visible:border-[var(--foreground)] focus-visible:outline-none
```

**Skip links**: botão preto visível no topo da página.

**Alvo de toque**: mínimo de 44px×44px pra todo elemento interativo no mobile.

---

## Escolhas ousadas (inegociáveis)

1. **Tipografia hero oversized**: pelo menos uma palavra em 8xl ou maior (9xl no desktop)
2. **Elementos decorativos de hero**: regra grossa com um quadrado pequeno bordado pra pontuação visual
3. **Seção de stats invertida**: fundo preto, texto branco, com textura sutil de linha vertical
4. **Sem cores de destaque**: resista à tentação — o preto É o destaque
5. **Regras horizontais pesadas**: linhas pretas de 4px entre TODAS as seções principais
6. **Pull quotes editoriais**: depoimentos como serifa itálica grande com aspas oversized
7. **Tudo cortante**: zero border-radius em todos os elementos
8. **Interações instantâneas**: no máximo 100ms de transição, majoritariamente instantâneo
9. **Tipografia como gráfico**: títulos que funcionam como elemento visual, não só texto
10. **Texturas em camada**: múltiplos padrões sutis pra profundidade (design NÃO chapado)
11. **Drop cap em caixa**: primeiro parágrafo do detalhe de produto tem drop cap com caixa bordada
12. **Tier de preço elevado**: o tier destacado se estende verticalmente no desktop
13. **Inversões no hover**: feature cards e tiers de preço invertem no hover
14. **Bordas de imagem engrossam**: borda de imagem de blog aumenta de peso no hover com efeito de escala

---

## Como é o sucesso

Uma implementação bem-sucedida do Minimalist Monochrome deve parecer:
- Abrir uma revista de moda de alto padrão
- Caminhar por uma galeria de arte moderna
- Ler uma monografia de arquitetura premiada
- Navegar pelo site de uma marca de luxo

NÃO deve parecer:
- Um template de site genérico
- Uma landing page de startup de tecnologia
- Algo que "precisa de uma pontinha de cor"
- Minimalist Modern com as cores removidas
