# persiapan module yang akan digunakan
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import networkx as nx
from networkx.algorithms import bipartite
# tahap 1
# memanggil file txt dan memasukkan ke dalam variable data
data = pd.read_csv('Employee_Movie_Choices.txt', sep="\t")
# menampilkan data 
print(data)


# tahap 2
# menampilkan list dari data memamfaatkan module networkx
B = nx.from_pandas_edgelist(data, '#Employee', 'Movie')
B.edges()
print(B.edges())

#tahap 3
#membuat node (titik/simpul)  untuk setiap type dengan data['#Employee'] sebagai employee dan data['Movie'] sebagai movie
#intinya melakukan list pengelompokan sesuia type ya
for employee in data['#Employee']:
    nx.set_node_attributes(B, {employee: {'type':'employee'}})
for movie in data['Movie']:
    nx.set_node_attributes(B, {movie: {'type':'movie'}})

print(nx.get_node_attributes(B, 'type'))


#tahap 4
# cara menemukan bobot proyeksi yang memberikan informasi jumlah film yang dimiliki oleh tiap pasangan pegawai
G = bipartite.weighted_projected_graph(B, data['#Employee'])

#tahap 5
# melakukan plot GRAPH 
plt.figure(figsize=(12, 6))
pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G,'weight')
print(nx.draw_networkx(G, pos))
print(nx.draw_networkx_edge_labels(G, pos, edge_labels=labels))
plt.show()

#tahap 6
#mencari korelasi antara skor hubungan karyawan dengan jumlah film yang mereka miliki.
#jika ada 2 karyawan yang tidak memiliki film/movie maka berikan index nol, jangan dibuang datanya namun masukkan dalam perhitungan korelasi

#tahap 7
#panggil data_1 yang berisi hubungan antar pegawai
data_1 = pd.read_csv('Employee_Relationships.txt', sep="\t", header=None)
print(data_1)

data_2 = data_1.set_index([0, 1])
print(data_2)

weights = nx.get_edge_attributes(G,'weight')
print(weights)

for index, weight in weights.items():
    if index in list(data_2.index):
        data_2.loc[index, 'weight'] = weight
    else:
        data_2.loc[(index[1], index[0]), 'weight'] = weight
print(data_2)

employee_relationships = data_2.fillna(0)
corr = employee_relationships.corr()
print(corr)


# inilah hasil dari korelasi nilai hubungan pegawai terhadap jumlah movie yang mereka miliki
print(corr.iloc[0,1])
