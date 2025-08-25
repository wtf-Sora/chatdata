# improved_chat_generator.py
import json, random, argparse

# ---------------------------
# CATEGORIES: Ask -> Answer pool mapping
# ---------------------------

CHAT_CATEGORIES = {
    "greeting": {
        "ask": [
            "hi", "hello", "hie", "ki obostha?", "kemon aso?", "kemon acho?",
            "ki khobor?", "valo aso?", "ki obosta?"
        ],
        "ans": [
            ["hi", "hello", "hie"],
            ["valo achi", "bhalo", "good good"],
            ["thik achi", "acha achi", "fine"],
            ["onak valo", "bhalo re", "not bad"]
        ]
    },
    "where": {
        "ask": [
            "tui koi?", "kothay?", "bari koi?", "campus e?", "aj kothay thakis?",
            "koi geli?", "ki jaiga?"
        ],
        "ans": [
            ["ghore", "bari te", "home e"],
            ["campus e", "library te", "class e"],
            ["bondhu-r sathe", "dhaka e", "bashundhara"],
            ["bahire", "bazar e", "road e"]
        ]
    },
    "doing": {
        "ask": [
            "ki koros?", "ki korsos?", "ki kortesi?", "ki kortaso?", "aj ki korli?",
            "ki korchilam?", "ekhon ki koros?"
        ],
        "ans": [
            ["ghumaitesi", "kaj kortesi", "class e"],
            ["bas chill", "movie dekhsi", "game kheltasi"],
            ["porashona kortesi", "kaj kortesi", "drive kortesi"]
        ]
    },
    "meet": {
        "ask": [
            "meet korbi?", "aj ber hobi?", "chal baire jabo?", "chal coffee khabo?",
            "bondhu der sathe meet?", "aj khela dekhi?"
        ],
        "ans": [
            ["sure", "chole asbo", "asbo"],
            ["maybe", "dekhi kal", "na parbo"],
            ["ok", "hobe", "thik ache"]
        ]
    },
    "food": {
        "ask": [
            "khawa hoyeche?", "ki khaccho?", "aj ki kheli?", "bikel e khabi?",
            "chicken khabi?", "burger khabi?", "cha khabi?"
        ],
        "ans": [
            ["rice khailam", "biriyani khailam", "khawa sesh"],
            ["burger khaitesi", "cha khaitesi", "coffee khaitesi"],
            ["ekhon khaitesi", "ekhon na", "pore khabo"]
        ]
    },
    "study": {
        "ask": [
            "class kemon holo?", "exam hobe?", "parikkha ready?", "study koros?",
            "assignment korsi?", "lab holo?"
        ],
        "ans": [
            ["exam valo hoise", "porashona cholse", "hmm ready"],
            ["assignment sesh", "lab complete", "abbu help korse"],
            ["parbo na", "onek tough", "onak hard"]
        ]
    },
    "misc": {
        "ask": [
            "tor crush koi?", "fb chalchis?", "game kheli?", "movie cholbi?",
            "aj special kichu?", "aj onek tired", "valo lagche na"
        ],
        "ans": [
            ["hahaha", "lol", "xD"],
            ["parbo na", "dekhi kal", "next time"],
            ["hmm", "ok", "acha"]
        ]
    }
}

# ---------------------------
# Random Chat Generator (category-based)
# ---------------------------

def random_chat():
    category = random.choice(list(CHAT_CATEGORIES.keys()))
    asks = CHAT_CATEGORIES[category]["ask"]
    answers_pool = CHAT_CATEGORIES[category]["ans"]

    ask = random.choice(asks)
    ans = random.choice(answers_pool)

    # Variation: কখনো emoji/punctuation যোগ
    if random.random() < 0.2:
        ask += random.choice(["!", "?", " 🤔", " 😅", " 😂", " 🤷‍♂️"])
    if random.random() < 0.3:
        ans = ans + [random.choice(["ok", "hmm", "acha"])]

    return {"ask": ask, "ans": ans}

# ---------------------------
# Dataset Writer
# ---------------------------

def generate_dataset(path="chat_pairs.jsonl", n_records=10000, as_array=False):
    if as_array:
        with open(path, "w", encoding="utf-8") as f:
            f.write("[")
            for i in range(n_records):
                obj = random_chat()
                chunk = json.dumps(obj, ensure_ascii=False)
                if i > 0:
                    f.write(",")
                f.write(chunk)
            f.write("]")
    else:
        with open(path, "w", encoding="utf-8") as f:
            for i in range(n_records):
                obj = random_chat()
                chunk = json.dumps(obj, ensure_ascii=False)
                f.write(chunk + "\n")
    print(f"✅ Done: {path} with {n_records} records")

# ---------------------------
# CLI Entry
# ---------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="chat_pairs.jsonl")
    parser.add_argument("--n", type=int, default=10000)
    parser.add_argument("--array", action="store_true")
    args = parser.parse_args()

    generate_dataset(path=args.out, n_records=args.n, as_array=args.array)
