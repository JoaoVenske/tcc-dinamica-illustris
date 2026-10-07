import yt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# 1. Carregar os dados
snapshot_path = 'snap_100.hdf5'
ds = yt.load(snapshot_path)

# 2. Localizar o centro espacial
_, centro_pos = ds.find_max(("gas", "density"))

esfera = ds.sphere(centro_pos, (50, "kpc"))

# 3. Extrair posições e calcular o Raio (r)

pos_brutas = esfera[("PartType4", "Coordinates")].in_units("kpc").v
centro_kpc = centro_pos.in_units("kpc").v

# Posições relativas ao centro
pos_relativas = pos_brutas - centro_kpc

# Módulo do raio: r = sqrt(x^2 + y^2 + z^2)
raios = np.linalg.norm(pos_relativas, axis=1)

# 4. Tratar as Velocidades e calcular |v|
vel_brutas = esfera[("PartType4", "Velocities")].in_units("km/s").v

# Aqui vamos descobrir a velocidade de translação da galáxia (Bulk Velocity)
# Vamos calcular a velocidade média das estrelas no núcleo (raio < 5 kpc)
# para referenciar quem dita o movimento central.
mascara_nucleo = raios < 5.0
vel_nucleo_x = np.mean(vel_brutas[mascara_nucleo, 0])
vel_nucleo_y = np.mean(vel_brutas[mascara_nucleo, 1])
vel_nucleo_z = np.mean(vel_brutas[mascara_nucleo, 2])
vel_sistemica = np.array([vel_nucleo_x, vel_nucleo_y, vel_nucleo_z])

# Subtrair a velocidade sistêmica para ter a velocidade das estrelas em relação à galáxia
vel_relativas = vel_brutas - vel_sistemica

# Módulo da velocidade: |v| = sqrt(vx^2 + vy^2 + vz^2)
vel_mag = np.linalg.norm(vel_relativas, axis=1)

# 5. Gerar o Mapa de Fase

plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 7))


h = ax.hist2d(
    raios, vel_mag, 
    bins=[600, 600], 
    range=[[0, 50], [0, 1500]], 
    cmap='inferno', 
    norm=colors.LogNorm(vmin=1) # LogNorm para não ofuscar as regiões de baixa densidade
)


cbar = plt.colorbar(h[3], ax=ax)
cbar.set_label('Densidade de Estrelas (Contagem)', rotation=270, labelpad=15)

ax.set_xlabel("Raio $r$ [kpc]", fontsize=12)
ax.set_ylabel("Magnitude da Velocidade $|v|$ [km/s]", fontsize=12)
ax.set_title("Espaço de Fase Estelar: $|v|$ vs $r$", fontsize=14)


ax.grid(True, linestyle='--', alpha=0.3, color='white')

plt.tight_layout()
plt.savefig('mapa_fase_v_r.png', dpi=300)
print("--- Sucesso! Imagem salva como 'mapa_fase_v_r.png' ---")