"""Treina DBSCAN e registra artefatos e métricas de avaliação."""
from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import adjusted_rand_score, confusion_matrix, silhouette_score
from sklearn.preprocessing import StandardScaler
from gerar_dados import gerar

ROOT = Path(__file__).parent
FEATURES = ["consumo_kwh", "hora", "temperatura_c", "ocupacao"]
EPS = 0.72
MIN_SAMPLES = 12


def treinar():
    df = gerar()
    X = df[FEATURES].replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    scaler = StandardScaler()
    Z = scaler.fit_transform(X)
    modelo = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(Z)
    rotulos = modelo.labels_
    clusters = set(rotulos) - {-1}
    mask = rotulos != -1
    sil = float(silhouette_score(Z[mask], rotulos[mask])) if len(clusters) > 1 and mask.sum() > len(clusters) else None
    real = (df.tipo_gerado == "anomalia_injetada").astype(int)
    pred = (rotulos == -1).astype(int)
    tn, fp, fn, tp = confusion_matrix(real, pred, labels=[0, 1]).ravel()
    resultado = {
        "registros": int(len(df)), "clusters": len(clusters), "ruidos_detectados": int(pred.sum()),
        "silhouette_sem_ruido": sil, "ari_referencia_sintetica": float(adjusted_rand_score(real, pred)),
        "matriz_confusao": {"verdadeiros_normais": int(tn), "falsos_alertas": int(fp), "anomalias_perdidas": int(fn), "anomalias_detectadas": int(tp)},
        "eps": EPS, "min_samples": MIN_SAMPLES,
    }
    (ROOT / "artefatos").mkdir(exist_ok=True)
    joblib.dump({"scaler": scaler, "core": modelo.components_, "core_labels": modelo.labels_[modelo.core_sample_indices_], "features": FEATURES, "eps": EPS, "min_samples": MIN_SAMPLES}, ROOT / "artefatos" / "dbscan.joblib")
    (ROOT / "artefatos" / "metricas.json").write_text(json.dumps(resultado, indent=2, ensure_ascii=False))
    (ROOT / "dados").mkdir(exist_ok=True)
    df.drop(columns="tipo_gerado").to_csv(ROOT / "dados" / "leituras_consumo.csv", index=False)
    return resultado

if __name__ == "__main__":
    print(json.dumps(treinar(), indent=2, ensure_ascii=False))
