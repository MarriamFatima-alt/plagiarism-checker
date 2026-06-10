# 🔍 Plagiarism Checker — Text & Code Similarity Detection

A fully interactive plagiarism detection tool built with Python and Gradio — supports both Text and Code comparison using multiple NLP algorithms.

![Status](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Live Demo
> Run locally using the steps below — interactive UI opens in your browser at `http://127.0.0.1:7860`

---

## 📌 Project Overview

| Metric | Detail |
|--------|--------|
| 🧠 Mode | Text & Code |
| 📏 Algorithms | TF-IDF, Jaccard, LCS, N-gram |
| 💻 Languages Supported | Python, Java/C++, JavaScript, HTML, CSS |
| 🎯 Output | Similarity score + matched phrases/lines |
| ⚙️ Dependencies | Only `gradio` needed |

---

## ✨ Features

- 🔤 **Text Plagiarism Detection** — compares essays, assignments, and documents
- 💻 **Code Plagiarism Detection** — detects copied code even when variable names are changed
- 📊 **3 Similarity Algorithms** — TF-IDF Cosine, Jaccard Index, Longest Common Subsequence
- 🌐 **5 Languages Supported** — Python, Java/C++, JavaScript, HTML, CSS
- 🟡 **Matching Highlights** — shows exactly which phrases/lines are copied
- 🎮 **Interactive UI** — Load Demo, Analyse, and Clear buttons
- ⚡ **Zero Heavy Dependencies** — no scikit-learn or NLTK needed

---

## 🧠 Algorithms Used

| Algorithm | Weight | What it Detects |
|-----------|--------|-----------------|
| TF-IDF Cosine Similarity | 40–50% | Overall vocabulary & topic similarity |
| Jaccard Index | 25–30% | Unique word overlap between documents |
| Longest Common Subsequence | 25% | Sequential structure & order similarity |
| N-gram Overlap | 25–30% | Exact phrase & expression matching |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Core logic & algorithms |
| Gradio | Interactive browser UI |
| Regex (re) | Text preprocessing & tokenization |
| Math & Collections | Cosine similarity calculations |

---

## ⚙️ How to Run

**Step 1 — Install Gradio:**
```bash
pip install gradio
```

**Step 2 — Run the app:**
```bash
python plagiarism_ui.py
```

**Step 3 — Open browser:**
```
http://127.0.0.1:7860
```

> ⚠️ Keep the terminal open while using the app — closing terminal stops the server.

---

## 📂 Project Structure

```
plagiarism-checker/
│
├── plagiarism_ui.py      # Main app — UI + all algorithms
├── README.md             # Project documentation
├── LICENSE               # MIT License
└── .gitignore            # Python gitignore
```

---

## 🎯 How It Works

1. Paste **Document A** (student submission) and **Document B** (original source)
2. Select mode — **Text** or **Code**
3. For code, select the **language** (Python, Java, JS, HTML, CSS)
4. Click **Analyse** — get similarity score instantly
5. View **matched phrases/lines** highlighted in results

---

## 👩‍💻 About

**Maryam Fatima**
- 🎓 BSCS Student
- 💡 Passionate about Data Science & Machine Learning
- 🔗 GitHub: [MarriamFatima-alt](https://github.com/MarriamFatima-alt)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
