
# Bangla + Banglish Casual Chat Data Generator

A **Python-based dataset generator** for creating large-scale **Bangla + Banglish conversational pairs** in a natural, casual style.  
Useful for training **chatbots, LLM fine-tuning, or data augmentation**.

---

## 🚀 Features
- **Category-based generation** → Questions always match appropriate answers (no random mismatch).  
- Supports **Bangla + Banglish** mixed text.  
- Adds **casual variations** (emoji, punctuation, slang).  
- Scales to **1M+ records** easily.  
- Two output modes:
  - **JSONL** → Each line is `{ "ask": ..., "ans": [...] }`
  - **JSON Array** → One big array `[{...}, {...}, ...]`

---

## 📦 Installation
Clone the repo and install Python (3.8+ recommended).

```bash
git clone https://github.com/wtf-Sora/chatdata
cd chatdata
```

No external dependencies required (only Python standard library).

---

## 🛠 Usage

### Generate 10k JSONL dataset

```bash
python improved_chat_generator.py --out chat_pairs_10k.jsonl --n 10000
```

### Generate JSON Array instead

```bash
python improved_chat_generator.py --out chat_pairs_10k.json --n 10000 --array
```

### Generate 1M+ dataset

```bash
python improved_chat_generator.py --out chat_pairs_1m.jsonl --n 1000000
```

---

## 📂 Example Output

**JSONL format**

```
{"ask": "ki obostha?", "ans": ["valo achi", "bhalo", "good good"]}
{"ask": "tui koi?", "ans": ["ghore", "bari te", "home e"]}
{"ask": "aj ki korli? 🤔", "ans": ["porashona kortesi", "kaj kortesi", "drive kortesi"]}
```

**JSON Array format**

```json
[
  {"ask": "meet korbi?", "ans": ["sure", "chole asbo", "asbo"]},
  {"ask": "khawa hoyeche?", "ans": ["rice khailam", "biriyani khailam", "khawa sesh"]}
]
```

---

## 📊 Categories Covered

* Greeting (`hi`, `kemon aso?`, `ki khobor?`)
* Where (`tui koi?`, `kothay?`, `aj kothay thakis?`)
* Doing (`ki koros?`, `aj ki korli?`)
* Meet/Plan (`meet korbi?`, `chal baire jabo?`)
* Food (`ki khaccho?`, `khawa hoyeche?`)
* Study/Exam (`class kemon holo?`, `exam ready?`)
* Misc (`fb chalchis?`, `game kheli?`, `aj tired`)

---

## 📌 License

MIT License – free to use, modify, and distribute.

---

## ✨ Author
[WTF SORA](https://github.com/wtf-Sora)<br>
Made with ❤️ for chatbot.

```
