from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from treinar_modelo import treinar

ROOT = Path(__file__).parent
st.set_page_config(page_title="Sinal — Monitor de consumo", page_icon="◉", layout="wide")

@st.cache_resource
def carregar():
    path = ROOT / "artefatos" / "dbscan.joblib"
    if not path.exists():
        treinar()
    return joblib.load(path)

m = carregar()
st.markdown("""<style>
.stApp {background: #f6f8fb;} .block-container {max-width: 1150px; padding-top: 2rem;}
.hero {background:linear-gradient(120deg,#10283f,#155e75);padding:2.1rem 2.5rem;border-radius:20px;color:white;margin-bottom:1.2rem}
.hero h1 {font-size:2.5rem;margin:0}.hero p {opacity:.82;margin:.55rem 0 0}
div[data-testid="stForm"] {background:white;padding:1.2rem;border:1px solid #e3e9ef;border-radius:16px}
</style><div class="hero"><h1>◉ Sinal</h1><p>Monitor inteligente de consumo · Identifique leituras fora do comportamento esperado</p></div>""", unsafe_allow_html=True)

left, right = st.columns([.9, 1.1], gap="large")
with left:
    st.subheader("Analisar uma leitura")
    with st.form("leitura"):
        consumo = st.number_input("Consumo (kWh)", min_value=0.0, max_value=1000.0, value=3.2, step=.1)
        a, b = st.columns(2)
        hora = a.slider("Hora do dia", 0, 23, 14)
        temp = b.number_input("Temperatura (°C)", min_value=-30.0, max_value=60.0, value=22.0, step=.5)
        ocup = st.selectbox("Local ocupado?", ["Sim", "Não"])
        submitted = st.form_submit_button("Verificar leitura", type="primary", use_container_width=True)
    st.caption("Informe uma leitura por vez. Os limites evitam entradas inválidas.")
    if submitted:
        x = pd.DataFrame([[consumo, hora, temp, ocup == "Sim"]], columns=m["features"])
        z = m["scaler"].transform(x)
        dist = np.linalg.norm(m["core"] - z, axis=1)
        idx = int(np.argmin(dist)) if len(dist) else -1
        anomalia = idx < 0 or dist[idx] > m["eps"]
        st.session_state["resultado"] = (anomalia, float(dist[idx]) if idx >= 0 else None)
    if "resultado" in st.session_state:
        flag, d = st.session_state["resultado"]
        if flag:
            st.error("⚠️ Leitura fora do padrão esperado")
            st.write("O DBSCAN não encontrou uma região densa de leituras semelhantes. Vale investigar o equipamento ou o contexto.")
        else:
            st.success("✓ Leitura compatível com um padrão conhecido")
            st.write("Esta leitura está próxima de um grupo observado nos dados de referência.")
        if d is not None:
            st.caption(f"Distância ao ponto de referência mais próximo (espaço padronizado): {d:.2f} · limite ε = {m['eps']}")
        st.caption("Isto é um alerta exploratório, não um diagnóstico nem uma decisão automática.")

with right:
    st.subheader("Panorama dos dados de referência")
    dados = pd.read_csv(ROOT / "dados" / "leituras_consumo.csv")
    fig = px.scatter(dados, x="hora", y="consumo_kwh", color="temperatura_c", color_continuous_scale="Teal", opacity=.55,
                     labels={"hora":"Hora do dia", "consumo_kwh":"Consumo (kWh)", "temperatura_c":"Temperatura (°C)"})
    fig.update_layout(template="plotly_white", height=340, margin=dict(l=10,r=10,t=20,b=10), coloraxis_colorbar=dict(title="°C"))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Amostra sintética de consumo; cor indica temperatura. O gráfico mostra contexto, não a saída do modelo.")

with st.expander("Como funciona"):
    st.markdown(f"""**Técnica:** DBSCAN (agrupamento por densidade), com ε = **{m['eps']}** e mínimo de **{m['min_samples']} vizinhos**.

**Dados:** simulados por `gerar_dados.py` — {len(dados):,} leituras: consumo, hora, temperatura e ocupação. O gerador combina ciclo diário, temperatura, ocupação e ruído; injeta também leituras extremas para testar o detector. Não representam medições reais.

**Preparação:** valores ausentes são preenchidos pela mediana e variáveis são padronizadas. DBSCAN considera ruído os pontos sem vizinhos suficientes.

**Avaliação:** a taxa de pontos classificados como ruído foi **{100*m['ruidos_detectados']/m['registros']:.1f}%**; silhouette dos clusters (sem ruído): **{m['silhouette_sem_ruido']:.3f}**. Referência sintética: ARI **{m['ari_referencia_sintetica']:.3f}**. Métricas neste contexto artificial não garantem desempenho em consumo real.

**Limitações:** sem dados reais, a definição de anomalia depende dos padrões simulados; uma novidade pode ser normal. Distância e ε dependem da padronização e dos parâmetros. DBSCAN não oferece probabilidade calibrada.""")

st.divider()
st.caption("Projeto acadêmico de mineração de dados · Gustavo Muniz dos Anjos e Alex Gabriel Alves dos Santos")
