import pandas as pd
# import llama tokenizer
from transformers import AutoTokenizer

input_file_1 = "samsum_processed.csv"
input_file_2 = "qmsum_processed.csv"

df = pd.read_csv(input_file_1)
print(f"Original dataset size: {df.shape}")
qdf = pd.read_csv(input_file_2)
print(f"QMSUM dataset size: {qdf.shape}")

## Split 1, 5500 < df.length < 6500
df1 = df[(df['length'] >= 5500) & (df['length'] < 6500)]
print(f"Dataset size with 5500 < length < 6500: {df1.shape}")
df1.to_csv("samsum_processed_bw_5500_6500.csv", index=False)

## Split 2, 9000 < df.length < 10000
df2 = df[(df['length'] >= 8500) & (df['length'] < 9500)]
print(f"Dataset size with 8500 < length < 9500: {df2.shape}")
df2.to_csv("samsum_processed_bw_8500_9500.csv", index=False)

## Split 3, 11500 < df.length < 12500
df3 = df[(df['length'] >= 11500) & (df['length'] < 12500)]
print(f"Dataset size with 11500 < length < 12500: {df3.shape}")
df3.to_csv("samsum_processed_bw_11500_12500.csv", index=False)

# for qdf, add the length column
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
qdf['length'] = qdf['context'].apply(lambda x: len(tokenizer(x)['input_ids']))
# add column for dataset
qdf['dataset'] = "qmsum"

## Split 1, 8500 < qdf.length < 9500
df2 = qdf[(qdf['length'] >= 8500) & (qdf['length'] < 9500)]
print(f"QMSUM dataset size with 8500 < length < 9500: {df2.shape}")
df2.to_csv("qmsum_processed_bw_8500_9500.csv", index=False)

## Split 2, 13000 < qdf.length < 14000
df3 = qdf[(qdf['length'] >= 13000) & (qdf['length'] < 14000)]
print(f"QMSUM dataset size with 13000 < length < 14000: {df3.shape}")
df3.to_csv("qmsum_processed_bw_13000_14000.csv", index=False)

## Split 3, 17500 < qdf.length < 18500
df4 = qdf[(qdf['length'] >= 17500) & (qdf['length'] < 18500)]
print(f"QMSUM dataset size with 17500 < length < 18500: {df4.shape}")
df4.to_csv("qmsum_processed_bw_17500_18500.csv", index=False)