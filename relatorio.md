# Monitor de anomalias de consumo — relatório

**Integrantes:** Gustavo Muniz dos Anjos e Alex Gabriel Alves dos Santos  
**Problema.** Leituras incomuns de consumo podem ajudar a identificar erros de medição ou situações que merecem investigação. O projeto demonstra um serviço que recebe consumo, horário, temperatura e ocupação e aponta se a leitura se distancia de regiões densas conhecidas. O alerta não é diagnóstico.

**Dados.** Dataset simulado reprodutível de 1.200 linhas: 1.100 padrões normais e 100 anomalias artificiais. O consumo normal incorpora ciclo horário, temperatura, ocupação e ruído gaussiano; as anomalias são valores extremos de consumo. Não são dados reais. A semente é 42. O conjunto sintético completo é usado no ajuste e na análise descritiva; portanto, métricas não equivalem a avaliação em dados independentes.

**Técnica e preparação.** DBSCAN agrupa observações em regiões densas conforme o raio ε e o mínimo de vizinhos (`min_samples`). Os pontos sem densidade suficiente recebem rótulo de ruído (`-1`). Ausentes são preenchidos pela mediana e quatro variáveis são padronizadas com `StandardScaler`, importante porque hora, temperatura e consumo têm escalas distintas. O modelo ajustado e os pontos centrais são salvos em joblib. Para uma entrada nova, comparamos a distância padronizada ao ponto central mais próximo com ε; exceder o limite gera alerta.

**Métricas e limitações.** Com `eps=0.72` e `min_samples=12`, o modelo encontrou 2 grupos e 99/1.200 pontos como ruído (8,25%); silhouette sem ruído = 0,376; ARI sintético = 0,817. Na referência criada pelo gerador: 85 das 100 anomalias foram detectadas, 15 não; houve 14 falsos alertas entre 1.100 casos normais. Silhouette não mede diretamente detecção de anomalias. A referência foi construída artificialmente e não existe teste independente real. DBSCAN é sensível a ε, à escala e a densidades variáveis; não estima probabilidade e a inferência por proximidade a pontos centrais é uma aproximação para dados novos. Os resultados não devem orientar decisões reais.

**Divisão de tarefas sugerida (confirmar entre integrantes).** Gustavo: gerador, preparação e avaliação do DBSCAN. Alex: interface, testes de uso e material de apresentação. Ambos: revisão do código, interpretação das métricas e apresentação. Ajustem esta divisão para refletir o trabalho efetivamente realizado.
