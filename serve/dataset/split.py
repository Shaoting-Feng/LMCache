import pandas as pd

input_file = "samsum_processed.csv"

df = pd.read_csv(input_file)
print(f"Original dataset size: {df.shape}")

## Split 1, df.length < 3000
df1 = df[df['length'] < 3000]
print(f"Dataset size with length < 3000: {df1.shape}")
df1.to_csv("samsum_processed_lt_3000.csv", index=False)

## Split 2, 3000 < df.length < 10000    
df2 = df[(df['length'] >= 3000) & (df['length'] < 10000)]
print(f"Dataset size with 1000 < length < 10000: {df2.shape}")
df2.to_csv("samsum_processed_bw_3000_10000.csv", index=False)

## Split 3, 10000 < df.length < 100000
df3 = df[(df['length'] >= 10000) & (df['length'] < 100000)]
print(f"Dataset size with 10000 < length < 100000: {df3.shape}")
df3.to_csv("samsum_processed_bw_10000_100000.csv", index=False)