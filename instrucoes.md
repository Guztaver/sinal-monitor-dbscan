# Trabalho — Mineração de Dados

Em dupla, vocês constroem um site que funciona como um serviço real. O usuário informa dados comuns e recebe uma resposta útil, e a mineração de dados roda por trás. A professora vai testar o site com dados novos durante a apresentação.

O uso de IA é permitido, com as regras da seção 7.

---

## 1. O site de cada dupla

Cada dupla constrói um destes oito sites, sorteado em sala. Se houver mais de oito duplas, alguns temas se repetem com datasets diferentes.

| #   | Site                          | Técnica                        | O usuário informa                  | O site responde                                                         |
| :-- | :---------------------------- | :----------------------------- | :--------------------------------- | :---------------------------------------------------------------------- |
| 1   | Previsão de temperatura       | Regressão Linear               | Mês, umidade, pressão e vento      | Temperatura prevista e erro típico (MAE)                                |
| 2   | Carrinho inteligente          | Regras de associação (Apriori) | Produtos no carrinho               | Até 5 sugestões, com confiança e lift                                   |
| 3   | Recomendador de filmes        | KNN                            | 3 a 5 filmes de que gosta          | 5 filmes parecidos                                                      |
| 4   | Estimador de preço de imóvel  | Árvore de Regressão            | Área, quartos e bairro             | Preço estimado e faixa de erro                                          |
| 5   | Risco de evasão               | Árvore de Decisão              | Perfil do aluno                    | Risco de evadir e o caminho da árvore que levou a ele                   |
| 6   | Aprovação de crédito simulada | Random Forest                  | Dados do solicitante               | Aprovado ou negado, com a probabilidade e os 3 fatores mais importantes |
| 7   | Segmentação de clientes       | K-means                        | Idade, renda e pontuação de gastos | Segmento do cliente, descrição do perfil e gráfico                      |
| 8   | Monitor de anomalias          | DBSCAN                         | Leituras de consumo                | Normal ou fora do padrão, com gráfico                                   |

---

## 2. Os dados

Os dados devem ter **pelo menos 300 linhas**. A dupla escolhe entre:

- **Dataset público**, de fonte citada (Kaggle, UCI, INMET, MovieLens e outras), ou
- **Dataset simulado**, gerado pela própria dupla.

Se for **simulado**, a dupla deve:

- Gerar os dados por um script (por exemplo, em Python com `numpy` e `pandas`) e guardá-lo no repositório.
- Dar estrutura aos dados: as colunas devem se relacionar de forma realista com a resposta, com um pouco de ruído. Dados totalmente aleatórios não servem, porque o modelo não aprende nada.
- Explicar no README e no relatório como os dados foram gerados: regras, intervalos e ruído.
- Informar na seção "Como funciona" do site que os dados são simulados.

---

## 3. O que o site precisa ter

- Tela de entrada simples: formulário (ou upload de CSV) com os campos do tema.
- Resposta clara, que não exija que o usuário saiba mineração.
- Seção "Como funciona", com a técnica, o dataset (e se é simulado) e a métrica obtida.
- Preparação dos dados feita no código (ausentes e transformações) e divisão treino e teste, quando a técnica permitir.
- Modelo salvo (por exemplo, com `joblib`), para o site não treinar a cada acesso.
- Validação das entradas, para o site não quebrar com valores inválidos.

**Sugestão de ferramentas:** Python, `scikit-learn` (`mlxtend` para as regras) e Streamlit. A hospedagem no Streamlit Community Cloud ou no Hugging Face Spaces é gratuita. Outras opções, como Flask ou Gradio, também valem.

---

## 4. Entrega final

Enviem à professora:

- Link público do site, funcionando.
- Repositório no GitHub, com:
  - o código do site;
  - o notebook de treino e o script de simulação, se houver;
  - o arquivo de dados ou o script que o gera;
  - o `requirements.txt`;
  - um README que explica como rodar e declara o uso de IA.
- Relatório de 1 a 2 páginas, com problema, dados, técnica, métrica, limitações e divisão de tarefas.

---

## 5. Datas

| Etapa                                    | Data  |
| :--------------------------------------- | :---- |
| Formação das duplas                      | 28/10 |
| OAT em sala: primeira versão funcionando | 18/11 |
| Entrega final                            | 01/12 |
| Apresentação                             | 02/12 |

---

## 6. Uso de IA

- Declarem no README quais ferramentas usaram e para quê.
- Os dois integrantes precisam explicar o código e as escolhas. Na apresentação, a professora pode peder uma alteração ao vivo, como mudar um parâmetro ou uma entrada.
- Não coloquem senhas, chaves ou dados pessoais sensíveis no repositório.
