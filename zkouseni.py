import megatherion

data1 = {'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']}
data2 = {'id': [1, 5, 3], 'age': [25, 30, 35]}

df1 = megatherion.DataFrame(data1)
df2 = megatherion.DataFrame(data2)

joined_df = df1.inner_join(df2, 'id', 'id')



df3 = megatherion.DataFrame.read_json("data.json")
df4 = megatherion.DataFrame.read_json("data copy.json")

joined_df2 = df3.inner_join(df4, 'numbers', 'numbers')

df5 = df2.product(axis=1)
print(df2)
df6 = df2.replace([1,5,30,35,25],9)
print(df6)
df7 = df1.melt(id_vars=['id'],value_vars=['name'])
print(df7)

#print("Joinutá tabulka číslo 1")
#print(joined_df)
#print("------------------------------")
#print("Joinutá tabulka číslo 2")
#print(joined_df2)

#print("------------------------------")
#print("Setříděná tabulka číslo 2 od největšího po nejmenší")
#sorted_df = df3.sort("numbers", ascending=False)
#print(sorted_df)

#print("------------------------------")
#print("Filtrovaná tabulka číslo 2 podle čísel která jsou větší nebo rovno než 5")
#filtered_df = df3.filter('numbers', lambda x: x >= 5)
#print(filtered_df)