1 import yt
2 import numpy as np
3 import agama
4 import matplotlib . pyplot as plt
5
6 # 1. Configurar o AGAMA
7 agama . setUnits ( length =1 , velocity =1 , mass =1)
8
9 # 2. Carregar e Filtrar os Dados
10 ds = yt . load ( ’ snap_100 . hdf5 ’)
11 _ , centro = ds . find_max (( " gas " , " density " ) )
12 esfera = ds . sphere ( centro , (50 , " kpc " ) )
13
14 posicoes_yt = esfera [( " PartType4 " , " Coordinates " ) ]. in_units ( " kpc " ) .
v
15 posicoes_centralizadas = posicoes_yt - centro . in_units ( " kpc " ) . v
16 massas = esfera [( " PartType4 " , " Masses " ) ]. in_units ( " Msun " ) . v
17
18
19 # 3. R e c o n s t r u o do Potencial
20 potencial_estrelas = agama . Potential (
21 type = ’ Multipole ’ ,
22 particles =( posicoes_centralizadas , massas ) ,
23 symmetry = ’a ’ ,
24 gridSizeR =20 ,
25 lmax =20
26 )
27
28
29 # 4. C l c u l o do Perfil Radial
30 raios = np . linspace (0.1 , 50 , 100)
31 pontos_radiais = np . zeros (( len ( raios ) , 3) )
32 pontos_radiais [: , 0] = raios
33
39
34 potenciais = potencial_estrelas . potential ( pontos_radiais )
35
36 # 5. Plotagem do Potencial
37 plt . figure ( figsize =(8 , 6) )
38
39 plt . plot ( raios , potenciais , color = ’ blue ’ , lw =2 , label = ’ Potencial ␣
Estelar ␣ ( AGAMA ) ’)
40 plt . xlabel ( ’ Raio ␣ $R$ ␣ ( kpc ) ’ , fontsize =12)
41 plt . ylabel ( ’ Potencial ␣ $ \ Phi ( R ) $ ’ , fontsize =12)
42 plt . title ( ’ Perfil ␣ do ␣ Potencial ␣ Gravitacional ’ , fontsize =14)
43 plt . legend ()
44 plt . grid ( True , alpha =0.3)
45
46 plt . tight_layout ()
47 plt . savefig ( ’ potencial_estrelas_simples . png ’ , dpi =300)
48 plt . show ()