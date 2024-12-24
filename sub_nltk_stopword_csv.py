import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
df_stopword_eng = pd.DataFrame(stopwords.words('english'), columns = ['stopword_eng'])

df_stopword_eng.to_csv('./format_files/stopwords_eng.csv')