#%%

from apyori import apriori
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

all_items = set()  # Tüm ögeler
with open("TestDatas/All_Data.csv") as f:
    reader = csv.reader(f, delimiter=",")  # her bir tag virgülle ayrıldıgı için burada belirtiyorum
    for i, line in enumerate(reader):
        all_items.update(line)
# Her bir ögeden veriler içerisinde kaç tane oldugunun sayılması ve listenin buna göre güncellenmesi
counting = list()
with open("TestDatas/All_Data.csv") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        row = {item: 0 for item in all_items}
        row.update({item:1 for item in line})
        counting.append(row)
deneme = pd.DataFrame(counting)
print(deneme.head())  # ss al burayı
print(deneme.shape)

#%%

# 1. Tüm satır toplamlarının toplamının toplam öğe sayısını bulun
tot_item_count = sum(deneme.sum())
#print(tot_item_count)

# 2. İlk 20 öğeyi almak için satırları toplayın ve sıralama azalan düzendedir
item_sum = deneme.sum().sort_values(ascending=False).reset_index().head(n=20)
item_sum.rename(columns={item_sum.columns[0]:'Item_name',item_sum.columns[1]:'Item_count'}, inplace=True)
#print(item_sum)

# 3. Ne kadar katkıda bulunduğunu bilmemiz için yüzde değeri eklenir.
# X'in toplam yüzdesi, toplam yüzdede x ve üzeri öğelerin yüzdesini, yani kümülatif toplamı belirler.
item_sum['Item_percent'] = item_sum['Item_count']/tot_item_count
item_sum['Tot_percent'] = item_sum.Item_percent.cumsum()
item_sum.head(20) # Yüzdelerle birlikte ilk 20 öğe listesi


# sık geçen tagların cizimi
obj = (list(item_sum['Item_name'].head(n=20)))
y_pos = np.arange(len(obj))
performans = list(item_sum['Item_count'].head(n=20))
#print(performans)

plt.bar(y_pos,performans,align='center',alpha=0.9)
plt.xticks(y_pos,obj,rotation='vertical')
plt.ylabel('Frekans Sayısı')
plt.title('Analiz Sonucu')
plt.show(block=True)
plt.interactive(False)
plt.figure()
print("deneme: ")
print(deneme.shape)


#%%

#Dikkate alınacak öğe için Minimum Toplam Öge Yüzdesi -> Eşik değeri gibi
# transaction islem Dikkate alınacak minimum işlem uzunluğu (yani arka arkaya minimum öğe sayısı).

def prune_dataset(olddf,len_transaction, tot_item_percent):
    if 'tot_items' in olddf.columns:
        del(olddf['tot_items'])

    # Her öğe için item_count ve toplam öğe sayısını bulma.
    # 3.adım gibi
    Item_count = olddf.sum().sort_values(ascending=False).reset_index()
    tot_items = sum(olddf.sum().sort_values(ascending=False))
    Item_count.rename(columns={Item_count.columns[0]:'Item_name', Item_count.columns[1]:'Item_count'},inplace = True)

    # Öge yuzdesi ve toplam yuzdeyi bulmak icin 3 adıma benzer
    Item_count['Item_percent'] = Item_count['Item_count'] / tot_items
    Item_count['Tot_percent'] = Item_count.Item_percent.cumsum()

    # Toplam yüzde için koşul / minimum eşiğe uyan öğeleri almak.
    selected_items = list(Item_count[Item_count.Tot_percent < tot_item_percent].Item_name)
    olddf['tot_items'] = olddf[selected_items].sum(axis=1)

    # İşlemin uzunluğu veya bir satırdaki öğe sayısı için koşul / minimum eşiğe uyan öğeleri almak.
    olddf = olddf[olddf.tot_items >= len_transaction]
    del(olddf['tot_items'])

    # Temizlenmis / Kısaltılmıs veri seti

    return olddf[selected_items],Item_count[Item_count.Tot_percent < tot_item_percent]


#%%

#Apriori için uygun bir veri seti elde etmek üzere şimdi len_transaction ve tot_item_percent için farklı değerler gireceğiz
#Deneme 1

pruneddf ,Item_count= prune_dataset(deneme,3,0.7)

print(pruneddf.shape)
#print(list(pruneddf.columns))
# Çıktı (Sütun listesi aslında apriori için dikkate aldığımız öğelerdir.)


#%%

# DENEME 2
#pruneddf,Item_count = prune_dataset(deneme,4,0.4)
print(pruneddf.shape)
#print(list(pruneddf.columns))

#%%



#%%

#
# # deneme 3
#pruneddf, Item_count = prune_dataset(deneme,4,0.2)
#print(pruneddf.shape)
#print(list(pruneddf.columns)



#%%

# İlk olarak, veri çerçevemizi, orijinal veri kümemiz gibi görünecek, ancak boyutu küçültülmüş bir csv dosyasına dönüştürmemiz gerekir. ½½
# 1'leri uygun öğe adına dönüştürme (sütun adı)

y = list(pruneddf.columns)
#print("y",y)
for s in y:
    pruneddf.loc[(pruneddf[s] == 1),s] = s
print(pruneddf)
# Sıfırları Sil
lol = pruneddf.values.tolist()
#print(lol)

for a in lol:
    while(0 in a):
        a.remove(0)
#print("sıfırsız lol",lol)
# Yeni bir temizlnemiş veri kümesi csv dosyası oluşturma
with open("Results/PrunedCVSs/prunedAll.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(lol)

#%%

birliktelik_kurali = apriori(lol, min_support=0.004, min_confidence=0.3, min_lift=3, min_length=4)
birliktelik_sonuc = list(birliktelik_kurali)

print("Türetilen Birliktelik İlişkisi {}.".format(len(birliktelik_sonuc)))

print("Türetilen Kurallar: ")
for i in range(0, len(birliktelik_sonuc)):
    print(birliktelik_sonuc[i][0])


#%%

# Güven değerine göre sıralanması
#sirali = sorted(birliktelik_sonuc, key=lambda x: int(x[2][0][2]))

# Destek değerine göre sıralanması
#sirali = sorted(birliktelik_sonuc, key=lambda x: int(x[1]))

# Lift Değerine göre
#sirali = sorted(birliktelik_sonuc, key=lambda x: int(x[2][0][3]))

# for item in sirali:
#     # iç listenin ilk dizini
#     # Temel öğeyi içerir ve öğe ekler
#     pair = item[0]
#     items = [x for x in pair]
#     print("Kural: " + items[0] + " -> " + items[1])
#
#     # iç listenin ikinci dizini
#     print("Destek: " + str(item[1]))
#
#     # iç listenin üçüncü dizininin 0'ında bulunan listenin üçüncü dizini
#
#     print("Güven: " + str(item[2][0][2]))
#     print("Lift: " + str(item[2][0][3]))
#     print("=====================================")

# iç içe liste -> nested list
    # İç içe listenin ilk dizi kuralı, ikinci dizini destek (support) değerini, ucuncu diznde destek(confidence) ve lift değeri bulunur



#%%

for item in birliktelik_sonuc:
    # iç listenin ilk dizini
    # Temel öğeyi içerir ve öğe ekler

    pair = item[0]

    items = [x for x in pair]
    print("Kural: " + items[0] + " -> " + items[1])

    # iç listenin ikinci dizini -> support
    print("Destek: " + str(item[1]))

    # iç listenin üçüncü dizininin 0'ında bulunan listenin üçüncü dizini

    print("Güven: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")




#%%

# Sonucları csv dosyasına yazdırma
#df = pd.DataFrame([[i[0], i[1],str(i[2][0][2]),str(i[2][0][3])] for i in birliktelik_sonuc],
                  #columns=['taglar','destek','guven','lift'])



#df.to_csv('Results/All_DataResults.csv', index=False)

