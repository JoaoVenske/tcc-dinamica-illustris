import yt
import numpy as np
import matplotlib.pyplot as plt

# 1. Carregar os dados
snapshot_path = 'snap_100.hdf5'
ds = yt.load(snapshot_path)

# 2. centralizar
_, centro_pos = ds.find_max(("gas", "density"))
raio_max = 50.0
esfera = ds.sphere(centro_pos, (raio_max, "kpc"))

pos_brutas = esfera[("PartType4", "Coordinates")].in_units("kpc").v
centro_kpc = centro_pos.in_units("kpc").v
massas = esfera[("PartType4", "Masses")].in_units("Msun").v

# 3. Calcular raios relativos
pos_relativas = pos_brutas - centro_kpc
raios = np.linalg.norm(pos_relativas, axis=1)

# 4. Construir o perfil: Massa contida em cada anel 
num_bins = 50
bins_raio = np.linspace(0.1, raio_max, num_bins + 1)
centro_bins = (bins_raio[:-1] + bins_raio[1:]) / 2.0

# Massa em cada casca (o histograma faz a soma das massas dentro do intervalo)
massa_por_casca, _ = np.histogram(raios, bins=bins_raio, weights=massas)

# 5. Plotar
plt.figure(figsize=(8, 6))
plt.plot(centro_bins, massa_por_casca, color='darkblue', lw=2, marker='o', markersize=4)


plt.yscale('log')

plt.xlabel('Raio $r$ [kpc]', fontsize=12)
plt.ylabel(r'Massa Estelar por Intervalo $\Delta M$ [$M_\odot$]', fontsize=12)
plt.title('Perfil Radial de Massa Estelar', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('perfil_massa_radial.png', dpi=300)
plt.show()