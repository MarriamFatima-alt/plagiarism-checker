# ============================================================
#   PLAGIARISM CHECKER — Interactive UI
#   Run: python plagiarism_ui.py
#   Requirements: pip install gradio
# ============================================================

import re
import math
from collections import Counter

STOPWORDS = set([
    'the','and','for','are','was','were','that','this','with',
    'from','have','has','been','will','they','their','which',
    'when','also','into','more','its','not','but','can','all',
    'one','had','there','what','about','who','each','she','him',
    'his','how','over','out','than','then','some','our','your',
    'would','could','should'
])

CODE_KEYWORDS = set([
    'if','else','elif','for','while','return','def','class',
    'import','from','in','not','and','or','true','false','none',
    'int','float','str','bool','print','range','len','append',
    'function','var','let','const','void','public','private',
    'static','new','this','self','try','except','catch','finally',
    'break','continue','pass','lambda','yield','switch','case',
    'html','head','body','div','span','p','a','ul','li','table',
    'tr','td','th','form','input','button','select','option',
    'style','link','script','meta','title','h1','h2','h3','h4',
    'href','src','class','id','type','value','placeholder',
    'margin','padding','color','background','font','border',
    'width','height','display','flex','grid','position','top',
    'left','right','bottom','float','clear','overflow'
])

# ── Text Functions ─────────────────────────────────────────
def tokenize_text(text):
    tokens = re.sub(r'[^a-z0-9\s]', ' ', text.lower()).split()
    return [w for w in tokens if len(w) > 2 and w not in STOPWORDS]

def cosine_sim(ta, tb):
    fa, fb = Counter(ta), Counter(tb)
    vocab = set(fa) | set(fb)
    dot = mag_a = mag_b = 0
    for w in vocab:
        idf = math.log(3 / (1 + (1 if w in fa else 0) + (1 if w in fb else 0))) + 1
        va, vb = fa.get(w,0)*idf, fb.get(w,0)*idf
        dot += va*vb; mag_a += va*va; mag_b += vb*vb
    return dot / (math.sqrt(mag_a)*math.sqrt(mag_b)) if mag_a and mag_b else 0.0

def jaccard(ta, tb):
    sa, sb = set(ta), set(tb)
    i = len(sa & sb)
    return i / len(sa | sb) if sa | sb else 0.0

def lcs(ta, tb):
    a, b = ta[:150], tb[:150]
    prev = [0]*(len(b)+1)
    for i in range(1, len(a)+1):
        curr = [0]*(len(b)+1)
        for j in range(1, len(b)+1):
            curr[j] = prev[j-1]+1 if a[i-1]==b[j-1] else max(prev[j], curr[j-1])
        prev = curr
    return prev[len(b)] / max(len(a),len(b)) if a else 0.0

def ngrams(tok, n=3):
    return [' '.join(tok[i:i+n]) for i in range(len(tok)-n+1)]

# ── Code Functions ─────────────────────────────────────────
def remove_comments(code, lang):
    if lang == 'Python':
        code = re.sub(r'#[^\n]*', '', code)
        code = re.sub(r'"""[\s\S]*?"""', '', code)
        code = re.sub(r"'''[\s\S]*?'''", '', code)
    elif lang == 'HTML':
        code = re.sub(r'<!--[\s\S]*?-->', '', code)
    elif lang == 'CSS':
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    else:
        code = re.sub(r'//[^\n]*', '', code)
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    return code

def normalize_vars(code):
    vm, c = {}, [0]
    def rep(m):
        w = m.group(0)
        if w.lower() in CODE_KEYWORDS or w[0].isdigit(): return w
        if w not in vm: c[0]+=1; vm[w]=f'V{c[0]}'
        return vm[w]
    return re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', rep, code)

def tokenize_code(code, lang):
    code = remove_comments(code, lang)
    code = re.sub(r'["\'`][^"\'`]*["\'`]', 'STR', code)
    code = re.sub(r'\b\d+(\.\d+)?\b', 'NUM', code)
    if lang not in ['HTML', 'CSS']:
        code = normalize_vars(code)
    return [t for t in re.split(r'[\s\(\)\{\}\[\];,:.=+\-\*\/\%<>!&\|\"\']+', code.lower()) if len(t) > 1]

# ── Main Check Function ────────────────────────────────────
def check_similarity(doc_a, doc_b, mode, lang):
    if not doc_a.strip() or not doc_b.strip():
        return "Dono boxes mein text/code daalo!", "", ""

    if mode == "Text":
        ta, tb = tokenize_text(doc_a), tokenize_text(doc_b)
        c  = cosine_sim(ta, tb)
        j  = jaccard(ta, tb)
        l  = lcs(ta, tb)
        ng = set(ngrams(ta)) & set(ngrams(tb))
        score = round((c*0.5 + j*0.25 + l*0.25)*100)
        ng_pct = round(len(ng)/len(set(ngrams(ta)))*100) if ngrams(ta) else 0
        details = f"TF-IDF Cosine  : {round(c*100)}%\nJaccard        : {round(j*100)}%\nLCS            : {round(l*100)}%\nN-gram Overlap : {ng_pct}%"
        matching = "\n".join([f'-> "{p}"' for p in list(ng)[:8]]) if ng else "Koi matching phrase nahi mili."
    else:
        ta, tb = tokenize_code(doc_a, lang), tokenize_code(doc_b, lang)
        c   = cosine_sim(ta, tb)
        j   = jaccard(ta, tb)
        ng_a = set(ngrams(ta, 3))
        ng_b = set(ngrams(tb, 3))
        ng_ov = len(ng_a & ng_b)/len(ng_a) if ng_a else 0
        score = round((c*0.4 + j*0.3 + ng_ov*0.3)*100)
        lines_a = [l.strip() for l in doc_a.split('\n') if l.strip()]
        lines_b = set(l.strip().lower().replace(' ','') for l in doc_b.split('\n') if l.strip())
        matched = [l for l in lines_a if l.lower().replace(' ','') in lines_b]
        details = f"Token Cosine   : {round(c*100)}%\nJaccard        : {round(j*100)}%\nN-gram Overlap : {round(ng_ov*100)}%\nMatched Lines  : {len(matched)} / {len(lines_a)}"
        matching = "\n".join([f'-> {l}' for l in matched[:8]]) if matched else "Koi matching line nahi mili."

    if score >= 65:
        verdict = f"HIGH similarity — {score}% — Likely copied!"
    elif score >= 35:
        verdict = f"MODERATE similarity — {score}% — Review karein"
    else:
        verdict = f"LOW similarity — {score}% — Mostly original"

    return verdict, details, matching

# ── Demo Data ──────────────────────────────────────────────
DEMOS = {
    "Text": (
        "Machine learning is a subset of artificial intelligence that enables systems to learn from data and improve their performance over time without being explicitly programmed.",
        "Machine learning is a branch of artificial intelligence that allows systems to learn from data and improve their performance without explicit programming."
    ),
    "Python": (
        "def calculate_sum(numbers):\n    total = 0\n    for num in numbers:\n        total = total + num\n    return total\n\nmy_list = [1, 2, 3, 4, 5]\nresult = calculate_sum(my_list)\nprint(result)",
        "def find_total(nums):\n    total = 0\n    for num in nums:\n        total = total + num\n    return total\n\ndata = [1, 2, 3, 4, 5]\nanswer = find_total(data)\nprint(answer)"
    ),
    "HTML": (
        "<div class='container'>\n  <h1>Welcome</h1>\n  <p>This is a paragraph.</p>\n  <button onclick='submit()'>Click me</button>\n</div>",
        "<div class='wrapper'>\n  <h1>Hello</h1>\n  <p>This is a paragraph.</p>\n  <button onclick='handleClick()'>Press here</button>\n</div>"
    ),
    "CSS": (
        ".container {\n  display: flex;\n  background-color: blue;\n  padding: 20px;\n  margin: 10px;\n  border-radius: 5px;\n}",
        ".wrapper {\n  display: flex;\n  background-color: red;\n  padding: 20px;\n  margin: 10px;\n  border-radius: 5px;\n}"
    ),
}

def load_demo(mode, lang):
    if mode == "Text":
        a, b = DEMOS["Text"]
    elif lang in DEMOS:
        a, b = DEMOS[lang]
    else:
        a, b = DEMOS["Python"]
    return a, b

def clear_all():
    return "", "", "", "", ""

# ── Gradio UI ──────────────────────────────────────────────
import gradio as gr

with gr.Blocks(title="Plagiarism Checker", theme=gr.themes.Soft()) as app:

    gr.Markdown("# Plagiarism Checker\n### Text & Code Similarity Detection")

    with gr.Row():
        mode = gr.Radio(["Text", "Code"], value="Text", label="Mode")
        lang = gr.Dropdown(
            ["Python", "Java/C++", "JavaScript", "HTML", "CSS"],
            value="Python",
            label="Language (Code mode ke liye)"
        )

    with gr.Row():
        doc_a = gr.Textbox(label="Document A — Student Submission", lines=10, placeholder="Yahan paste karo...")
        doc_b = gr.Textbox(label="Document B — Original / Source",  lines=10, placeholder="Yahan paste karo...")

    with gr.Row():
        btn_analyse = gr.Button("Analyse", variant="primary")
        btn_demo    = gr.Button("Load Demo")
        btn_clear   = gr.Button("Clear")

    verdict  = gr.Textbox(label="Result",                    lines=2)
    details  = gr.Textbox(label="Score Breakdown",           lines=6)
    matching = gr.Textbox(label="Matching Phrases / Lines",  lines=6)

    btn_analyse.click(fn=check_similarity, inputs=[doc_a, doc_b, mode, lang], outputs=[verdict, details, matching])
    btn_demo.click(   fn=load_demo,        inputs=[mode, lang],               outputs=[doc_a, doc_b])
    btn_clear.click(  fn=clear_all,        outputs=[doc_a, doc_b, verdict, details, matching])

app.launch()
