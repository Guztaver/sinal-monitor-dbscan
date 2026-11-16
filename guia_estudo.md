# Guia de estudo — apresentação do Sinal

## Explicação em 60 segundos

“Criamos o Sinal, um protótipo que analisa leituras simuladas de consumo. Usamos DBSCAN, um algoritmo não supervisionado que encontra regiões densas e marca pontos isolados como ruído. Padronizamos consumo, hora, temperatura e ocupação para que escalas diferentes não dominem a distância. Para uma leitura nova, medimos sua distância aos pontos centrais do modelo e comparamos com ε. É uma demonstração: os dados foram simulados, então os resultados não garantem desempenho no mundo real.”

## Conceitos para dominar

- **Mineração de dados:** encontrar estruturas úteis em dados, além de apenas armazená-los.
- **Não supervisionado:** o algoritmo não recebe rótulos de normal/anomalia para formar grupos. No nosso gerador, rótulos existem apenas para comparar resultados simulados.
- **DBSCAN:** agrupamento por densidade; não exige informar previamente o número de grupos.
- **ε (eps):** raio de vizinhança. Menor ε tende a deixar mais pontos isolados; maior ε pode juntar regiões.
- **min_samples:** quantidade mínima de pontos na vizinhança para definir um núcleo. Aumentar tende a exigir maior densidade.
- **Ruído:** observação que não pertence a uma região densa. Pode ser anomalia, mas também um padrão legítimo raro.
- **Padronização:** transforma atributos em escalas comparáveis (média 0, desvio padrão 1). Necessária antes de uma distância multivariada.
- **Silhouette:** mede coesão/separação dos clusters, não acurácia de detecção. Calculamos somente para pontos agrupados.
- **ARI:** compara partições preditas com rótulos de referência, corrigindo concordância ao acaso. Aqui a referência é sintética.
- **Limite de inferência:** DBSCAN não tem `predict` nativo. Nossa distância ao core mais próximo é uma regra aproximada; não é probabilidade nem garantia de pertencer ao cluster.

## Como a simulação funciona

O gerador cria 1.100 padrões com hora, temperatura e ocupação. O consumo cresce/varia conforme um ciclo horário, aumenta com calor e ocupação, e recebe ruído aleatório. Acrescenta 100 leituras extremas como anomalias didáticas. Essa estrutura permite demonstrar agrupamento; o modelo vê também os extremos no treino. Não alegue que dados aleatórios ou sintéticos representam clientes reais.

## Demonstração sugerida (3–5 min)

1. Apresente o problema e diga claramente que os dados são simulados.
2. Abra o site, explique os quatro campos e faça uma leitura compatível (por exemplo consumo 3,2 kWh, hora 14, temperatura 22 °C, ocupado).
3. Faça um caso extremo (por exemplo 15 kWh) e mostre o alerta e a distância/ε.
4. Mostre gráfico: hora e consumo; cor é temperatura. O gráfico é panorama, não classificação do modelo.
5. Abra “Como funciona”: explique padronização, ε, `min_samples`, métricas e limitações.
6. Se pedirem alteração: ajuste `EPS` em `treinar_modelo.py`, execute `python treinar_modelo.py` e reinicie o app; explique que o valor exige nova avaliação, não é “melhor” por definição.

## Perguntas prováveis

**Por que DBSCAN?** O tema sorteado é monitor de anomalias/DBSCAN; densidade permite marcar observações isoladas sem definir previamente quantos grupos existem.

**Por que padronizar?** Sem ela, uma variável com números maiores pode dominar a distância euclidiana.

**O que muda com ε?** Altera quem conta como vizinho: baixo pode fragmentar grupos e gerar falsos alertas; alto pode unir grupos e esconder casos isolados.

**O que é min_samples?** Mínimo de vizinhos na região ε para o ponto ser núcleo. Os parâmetros foram escolhidos empiricamente para a simulação, não validados em campo.

**A taxa de ruído é taxa de erro?** Não. É a proporção que o modelo marca como ruído. Para erro, é preciso comparar a rótulos confiáveis; mesmo ARI/contagens aqui refletem apenas os rótulos criados pelo gerador.

**O modelo pode prever qualquer caso novo?** Não exatamente: o DBSCAN clássico não oferece `predict`. Usamos aproximação por distância ao core mais próximo, declarada no README e no app.

**O que faria para produção?** Obter dados reais representativos e rotulados/revisados, testar em período separado, investigar falsos positivos/negativos, calibrar parâmetros, monitorar mudanças de padrão e manter decisão humana.

## Checklist antes de apresentar

- [ ] Cada integrante consegue explicar geração dos dados, DBSCAN, escala e limitações.
- [ ] Rodar comandos do README do zero e testar os dois exemplos no formulário.
- [ ] Conferir métricas no `artefatos/metricas.json` e jamais inventar resultados.
- [ ] Divisão de tarefas do relatório corresponde ao que realmente foi feito.
- [ ] Mostrar que os dados são simulados; não prometer precisão no mundo real.
