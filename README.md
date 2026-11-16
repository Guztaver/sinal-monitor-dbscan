# Sinal — Monitor de anomalias de consumo

Aplicação web acadêmica que recebe uma leitura de energia e sinaliza se ela parece compatível com padrões conhecidos. Técnica: **DBSCAN**. Integrantes: **Gustavo Muniz dos Anjos** e **Alex Gabriel Alves dos Santos**.

> Os dados são inteiramente simulados para fins didáticos; não são medições nem aconselhamento técnico.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python gerar_dados.py
python treinar_modelo.py
streamlit run app.py
```

Acesse o endereço local informado pelo Streamlit. O aplicativo também cria o artefato treinado automaticamente se ele estiver ausente. Para reproduzir os dados, use `python gerar_dados.py` (semente fixa 42).

## Dados e método

`gerar_dados.py` gera 1.100 leituras normais e 100 anomalias artificiais (1.200 linhas). O consumo normal depende de ciclo horário, temperatura, ocupação e ruído gaussiano; os casos artificiais são extremos de consumo. A mistura serve para demonstrar e testar, não reproduz uma população real. A avaliação é feita no conjunto sintético completo; não deve ser interpretada como validação independente para produção.

`treinar_modelo.py` substitui infinitos por ausentes, preenche ausentes pela mediana, padroniza quatro atributos e ajusta DBSCAN (`eps=0.72`, `min_samples=12`). Salva `artefatos/dbscan.joblib` e `artefatos/metricas.json`. Para uma nova leitura, o app mede a distância ao ponto central (core) mais próximo no espaço padronizado: além de ε é sinalizada como fora do padrão. É uma aproximação prática para inferência de DBSCAN em dados não vistos, não uma probabilidade.

Métricas calculadas: fração de ruído, silhouette excluindo ruído e ARI/contagem contra os rótulos conhecidos somente por se tratar de simulação. Parâmetros dependem da escala e do domínio; DBSCAN não produz probabilidade calibrada. A validação real exige dados reais rotulados e revisão humana.

## Arquivos

- `app.py`: site Streamlit responsivo.
- `gerar_dados.py`: gerador reprodutível.
- `treinar_modelo.py`: pré-processamento, treino e métricas.
- `dados/leituras_consumo.csv`: conjunto gerado (recriado pelo script).
- `artefatos/`: modelo e métricas serializados.
- `apresentacao.html`: slides para apresentar (setas ou espaço para navegar).
- `guia_estudo.md`: roteiro de estudo e perguntas de revisão.
- `relatorio.md`: relatório conciso para entrega.

## Uso de IA

Foi usada IA generativa (OpenAI/ChatGPT via pi) para apoiar estruturação, implementação, documentação e revisão do projeto. Os integrantes devem revisar o código, executar os testes e compreender/explicar as escolhas; uso declarado conforme as instruções da atividade.

## Integridade e limitações

Não há dados pessoais. O projeto é uma demonstração didática e não deve ser usado para decisões operacionais ou de segurança.
