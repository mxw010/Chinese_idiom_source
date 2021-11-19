#data source: https://github.com/pwxcoo/chinese-xinhua
#import: https://github.com/pwxcoo/chinese-xinhua/blob/master/scripts/clean.ipynb

#import the idioms through json, strip the source enclosed in 书名号.
#And then export as a csv to be read into R for plotting.

import json
import pandas as pd

with open("idiom.json") as fp:
    idioms = json.load(fp)

len(idioms)
j=0
data = []
no_source = []
for idiom in idioms:
    s = idiom['derivation']
    match_start=s.find("《")
    match_end=s.find("》")
    if match_start == -1 and match_end != -1:
        print("j=",j," ", idiom['word'], idiom['derivation'])
    elif match_start != -1 and match_end == -1:
        print("j=",j," ", idiom['word'], idiom['derivation'])
    elif match_start ==-1 and match_end ==-1:
        no_source.append([idiom['word'], idiom['derivation']])
    else:
        data.append([idiom['word'], s[s.find("《")+1:s.find("》")]])
    j+=1

df = pd.DataFrame(data, columns=['word','source'])
#about 9000 idioms missing source
#next: getting sources of those words
no_source_df = pd.DataFrame(no_source, columns=['word', 'source'])

for idx,item in no_source_df.iterrows():
    if not re.search("无", item[1]):
        print(item)
#for the idioms with a source, re-work them into a data frame:
#to be plotted
df['book'] = "nan"
df['chapter'] = "nan"
for idx, item in df.iterrows():
    if re.search("·", item[1]):
        split_item=item[1].split("·")
        df.loc[idx,'book']=split_item[0]
        df.loc[idx,'chapter']=split_item[1]
    else:
        df.loc[idx,'book'] = item[1]

df.to_csv("sourced.csv",na_rep="nan", header=True, index=False)

# 孙子兵法叫做《孙子》竟然没有多少成语来自孙子兵法
for idx, item in df.iterrows():
    if re.search("孙子", item[1]):
        print(item)
        
        
for idx, item in df.iterrows():
    if re.search("知彼知己", item[0]):
        print(item)
        
df['book'].value_counts().head(30)
df['chapter'][df['book'] == "史记"].value_counts().head(10)


 
