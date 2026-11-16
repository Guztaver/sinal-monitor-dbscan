"""Gera leituras sintéticas de consumo com padrões diários e anomalias."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N_NORMAL = 1100
N_ANOMALIAS = 100


def gerar(seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    hora = rng.integers(0, 24, N_NORMAL)
    temperatura = np.clip(rng.normal(22, 7, N_NORMAL), 3, 40)
    ocupacao = rng.binomial(1, 0.62, N_NORMAL)
    ciclo = 1.8 + 1.2 * np.sin((hora - 7) * np.pi / 12) ** 2
    consumo = 0.6 + ciclo + 0.075 * np.maximum(temperatura - 18, 0) + 1.15 * ocupacao + rng.normal(0, 0.35, N_NORMAL)
    consumo = np.clip(consumo, 0.15, None)
    normal = pd.DataFrame({"consumo_kwh": consumo, "hora": hora, "temperatura_c": temperatura, "ocupacao": ocupacao, "tipo_gerado": "normal"})

    hora_a = rng.integers(0, 24, N_ANOMALIAS)
    temp_a = rng.uniform(3, 40, N_ANOMALIAS)
    ocup_a = rng.binomial(1, .5, N_ANOMALIAS)
    consumo_a = rng.choice([1, -1], N_ANOMALIAS) * rng.uniform(1.5, 4.5, N_ANOMALIAS) + 4.2
    anom = pd.DataFrame({"consumo_kwh": consumo_a, "hora": hora_a, "temperatura_c": temp_a, "ocupacao": ocup_a, "tipo_gerado": "anomalia_injetada"})
    return pd.concat([normal, anom], ignore_index=True).sample(frac=1, random_state=seed).reset_index(drop=True)

if __name__ == "__main__":
    out = Path(__file__).parent / "dados" / "leituras_consumo.csv"
    out.parent.mkdir(exist_ok=True)
    gerar().to_csv(out, index=False)
    print(f"Salvo: {out} ({N_NORMAL + N_ANOMALIAS} linhas)")
