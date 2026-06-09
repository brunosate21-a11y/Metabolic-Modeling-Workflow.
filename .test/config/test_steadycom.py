from micom.data import test_taxonomy
from micom import Community
import pandas as pd

# Carregar modelos de exemplo
tax = test_taxonomy()
com = Community(tax)

# Correr SteadyCom
sol = com.cooperative_tradeoff(fraction=0.5)
print(sol.members)

# Guardar resultados
sol.members.to_csv(".test/config/steadycom_results.tsv", sep="\t")
print("Guardado em steadycom_results.tsv")