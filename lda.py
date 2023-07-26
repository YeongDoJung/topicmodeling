import pandas as pd
import numpy as np
import konlpy
import gensim
import pyLDAvis
import pyLDAvis.gensim as ldagensim
from tqdm import tqdm

fp = './data/crawl_인구소멸_2023-07-25_kkma_morphs.xlsx'
f = pd.read_excel(fp, dtype=str)
f = f.dropna()
f = f.values.tolist()

dict_article = gensim.corpora.Dictionary(f)
corpus = [dict_article.doc2bow(i) for i in f]

ldamodel = gensim.models.ldamodel.LdaModel(corpus = corpus, id2word= dict_article, passes = 15)

vis = ldagensim.prepare(ldamodel, corpus, dict_article, mds='mmds')

pyLDAvis.save_html(vis, f'./{fp}_ldavis.html')
