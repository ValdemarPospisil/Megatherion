import megatherion

df = megatherion.DataFrame.read_json("data.json")
print(df)
sort_df = df.sort('numbers')
print(sort_df)