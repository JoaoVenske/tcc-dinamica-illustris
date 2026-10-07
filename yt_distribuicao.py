import yt
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

# 1. Dados
snapshot_path = 'snap_100.hdf5'
ds = yt.load(snapshot_path)
_, centro = ds.find_max(("gas", "density"))

# 2. Coordenadas
esfera = ds.sphere(centro, (50, "kpc"))
coords = esfera[("PartType4", "Coordinates")].in_units("kpc").v
centro_kpc = centro.in_units("kpc").v

x = coords[:, 0] - centro_kpc[0]
y = coords[:, 1] - centro_kpc[1]

# 3. Plotagem
plt.style.use('default') 
fig, ax = plt.subplots(figsize=(10, 8))

# vmin e vmax ajustam o contraste para que os dados apareçam claramente
# hist2d - algoritmo de deposição (histograma bidimensional)
h = ax.hist2d(
    x, y, 
    bins=600, 
    range=[[-50, 50], [-50, 50]], 
    cmap='magma', 
    norm=colors.LogNorm(vmin=1, vmax=800) 
)

# Adicionar barra de cores
cbar = plt.colorbar(h[3], ax=ax)
cbar.set_label('Densidade de Partículas Estelares', rotation=270, labelpad=15)

ax.set_xlabel("X [kpc]")
ax.set_ylabel("Y [kpc]")
ax.set_title("Distribuição Estelar (Vista Face-on)")
ax.set_aspect('equal')
ax.set_facecolor('white')

plt.savefig('galaxia_estrelas.png', dpi=600, bbox_inches='tight', facecolor='white')
print(" Imagem salva como 'galaxia_estrelas.png' ")
