import csv

input_file = "/home/ubuntu/st-prodstack-v/LMCache/serve/linear_coefficients3_original.csv"
output_file = "/home/ubuntu/st-prodstack-v/LMCache/serve/linear_coefficients3.csv"
keep_files = {"06.csv", "03.csv", "02.csv", "1.csv"}

with open(input_file, newline='') as fin, open(output_file, "w", newline='') as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)
    writer.writeheader()
    for row in reader:
        fname = row["filename"]
        if fname in keep_files and fname:
            try:
                row["a"] = str(float(row["a"]) / 4)
                row["b"] = str(float(row["b"]) / 4)
            except (ValueError, TypeError):
                pass  # 保留原始值，或者你想跳过可以写 continue
        writer.writerow(row)
