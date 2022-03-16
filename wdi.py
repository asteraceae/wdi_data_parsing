from multiprocessing import allow_connection_pickling
import pandas as pd
import time

def depunc(sentence):
    for char in sentence:
        if char in ".,?/;-:()":
            sentence = sentence.replace(char,'')
    return sentence
#read csv into df
df = pd.read_table("WDIData.csv", sep = ",")

#read allowed attributes text file
#each line sliced to remove \n
with open("WorldDIDataAttributeList.txt", "r+") as f:
    allow = [depunc(line[:-1]) for line in f]
f.close()

#read a list of attributes
attributes = df["Indicator Name"]
attributes = attributes.values.tolist()
attributes = list(dict.fromkeys(attributes))

#read a list of years
years = list(df.columns)
years = [int(y) for y in years if len(y) == 4]

while(True):
    target = input("What year to make a csv for? Enter a year between 1960 - 2020, 4 digits.")
    if int(target) not in years:
        print("Not a valid answer.")
    else:
        break

print("Iterating over rows...")

countries = {}
for index, row in df.iterrows():
    print("\r", end="")
    print (f"{row['Country Name']}, {index + 1}/{len(df.index)}                                                      ", end = "")

    cnm = depunc(row["Country Name"])

    if cnm not in countries:
        countries[cnm] = dict()
        c = countries[cnm]
    else:
        c = countries[cnm]
    c[depunc(row["Indicator Name"])] = row[target]

#output
out = open(f"output_{target}.csv", "w+")
out.write("Country Name,")
count = 0

attributes = [depunc(a) for a in attributes if depunc(a) in allow]

for a in attributes:
    if a in allow:
        out.write(f"{a},")
        count += 1

for c in countries:
    out.write(f"\n")
    out.write(f"{c},")
    for a in attributes:
        out.write(f"{countries[c][a]}")
        out.write(f",")

out.close()

print("\nGenerated output.csv.")
print(f"{count} attribute(s) written.\n")




