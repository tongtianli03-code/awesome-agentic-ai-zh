> **繁體中文** | [简体中文](./README.zh-Hans.md) | [English](./README.en.md)

# 練習 1：Embeddings + nearest neighbors

對應 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.md) 練習 1。

## 任務

把 100 個句子做 embedding、給一個 query、找出 top-k 最相近的句子。觀察 cosine similarity 排序意義。

## 怎麼跑 — 兩條路徑

### Path A（默認、本機免費）

```bash
pip install -r requirements.txt
python starter.py   # 第一次自動下載 model (~80 MB)
```

預算：**$0**。`sentence-transformers/all-MiniLM-L6-v2` 模型在 CPU 跑、約 100 句 < 1 秒。

### Path B（cloud embedding，對照、極便宜）

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python starter_anthropic.py
```

預算：每次 ≈ **$0.00002**（text-embedding-3-small、100 句）。

> 💡 **Anthropic 沒提供 embedding API**——官方推薦 [Voyage AI](https://www.voyageai.com/)。這份用 OpenAI 示範（最常見），改 Voyage 只需換 client。

## 不花錢驗證程式邏輯

```bash
python test.py             # mock SentenceTransformer、不下載 model
python test_anthropic.py   # mock OpenAI client、驗 normalize 邏輯
```

## 核心觀念

```python
# 1. Encode → vector
sent_vecs = model.encode(sentences, normalize_embeddings=True)  # 100 × 384 vec
q_vec = model.encode([query], normalize_embeddings=True)[0]      # 384 vec

# 2. Cosine similarity = dot product (因為 normalized)
sims = sent_vecs @ q_vec        # 100 個 similarity score

# 3. Top-k
top_idx = np.argsort(-sims)[:top_k]
```

**為什麼 normalize**：normalized vector 的 dot product 直接等於 cosine similarity（範圍 [-1, 1]）、不用每次重算 norm。是 vector DB 通用技巧。

## 本機 vs cloud embedding 對照

| 維度 | sentence-transformers (本機) | OpenAI text-embedding-3-small (cloud) |
|---|---|---|
| 維度 | 384 | 1536 |
| 速度（100 句、CPU） | < 1 秒 | 1-2 秒（含網路） |
| 成本 | $0 | $0.00002 / 100 sentences |
| Multilingual | OK（多語版見 `paraphrase-multilingual-MiniLM-L12-v2`） | 強 |
| Long context（>512 token） | 截斷 | 強 |
| 一致性（同 input 同 output） | 100% | 99%（API 偶爾微擾） |

**結論**：個人 / 小資料 / 本機實驗、用 sentence-transformers 完全夠。大量 multilingual / 長文檔 / SaaS、用 cloud。

## 常見坑

- **沒 normalize**：cosine similarity ≠ dot product、要 `sim = dot(a,b) / (|a||b|)` 自己算
- **Mixed precision**：sentence-transformers 預設 fp32、若用 fp16 量化（省記憶體）相似度會差 1-2%
- **不同模型 vector 不能比**：MiniLM 跟 OpenAI 是兩個語意空間、不要把 cosine sim 直接比
- **太短 query**：1-2 字 query embedding 不穩、結果可能跳很遠。query 至少要句子

## 想看更好的 embedding？

```bash
# 本機更大 model（精度更好、速度較慢）
# 把 starter.py 的 MODEL_NAME 改成：
#   "sentence-transformers/all-mpnet-base-v2"           # 768 維、accuracy↑
#   "sentence-transformers/paraphrase-multilingual-..." # 多語

# Cloud 高精度
EMBED_MODEL=text-embedding-3-large python starter_anthropic.py   # 3072 維、$$
```

## 延伸

- **改成 BM25 + embedding hybrid**：keyword 跟 semantic 各取優、production 常用
- **加 reranker**：top-k 拿來丟 cross-encoder（`cross-encoder/ms-marco-MiniLM-L-6-v2`）做 reranking、精度大躍進
- **接練習 2 vector DB**：放到 Chroma 裡能跑萬筆規模、不必每次重 embedding
