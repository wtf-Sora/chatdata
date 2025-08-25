import json
import random
import argparse

# 🔑 Word variation for Banglish spelling feel
def banglish_variation(word):
    mapping = {
        "valo": ["valo", "bhalo"],
        "koros": ["koros", "korsos", "korteso"],
        "ache": ["ache", "ase"],
        "achi": ["achi", "asi", "ase"],
        "thik": ["thik", "tik"],
        "kemon": ["kemon", "kemne", "kmn"],
        "ki": ["ki", "ki re", "ki vai"],
    }
    return random.choice(mapping.get(word, [word]))

# 🔑 Random fillers/slang
def add_filler(ans):
    fillers = ["hmm", "arre", "oyee", "acha", "jhamela nai", "lol", "xD", "hahaha"]
    if random.random() < 0.25:
        return random.choice(fillers) + " " + ans
    return ans

# 🔑 Random emoji add
def add_emoji(ans):
    emojis = ["😂", "😅", "😌", "😔", "🤔", "🤟", "😎", "🥹", "🔥", "👌"]
    if random.random() < 0.2:
        return ans + " " + random.choice(emojis)
    return ans

# ---------------------------
# Categories with templates
# ---------------------------
CHAT_CATEGORIES = {
    "greeting": {
        "ask": ["hi", "hello", "hie", "ki obostha?", "kemon aso?", "ki khobor?"],
        "ans": [
            ["valo " + banglish_variation("achi"), "bhalo asi", "good good"],
            ["thik " + banglish_variation("ache"), "acha asi", "fine re"],
        ],
    },
    "where": {
        "ask": ["tui koi?", "kothay?", "aj kothay thakis?", "bari koi?", "campus e?"],
        "ans": [
            ["ghore", "bari te", "home e"],
            ["campus e", "library te", "class e"],
            ["bondhu-r sathe", "dhaka e", "bashundhara"],
        ],
    },
    "doing": {
        "ask": ["ki " + banglish_variation("koros") + "?", "aj ki korli?", "ekhon ki korteso?"],
        "ans": [
            ["ghumaitesi", "kaj kortesi", "class e"],
            ["movie dekhsi", "game kheltasi", "youtube e chill"],
            ["porashona kortesi", "drive kortesi", "bas chill"],
        ],
    },
    "meet": {
        "ask": ["aj meet korbi?", "chal baire jabo?", "coffee khabi?", "bondhu der sathe meet?"],
        "ans": [
            ["sure asbo", "chole asbo", "ok thik ase"],
            ["maybe dekhi", "parbo na", "next time"],
        ],
    },
    "food": {
        "ask": ["khawa hoyeche?", "ki khaccho?", "aj ki kheli?", "cha khabi?"],
        "ans": [
            ["rice khailam", "biriyani khaisi", "khawa shesh"],
            ["burger khaitesi", "cha khaitesi", "coffee khaitesi"],
            ["ekhon khaitesi", "ekhon na", "pore khabo"],
        ],
    },
    "study": {
        "ask": ["class kemon holo?", "exam ready?", "assignment korsi?", "lab holo?"],
        "ans": [
            ["exam valo hoise", "porashona cholse", "hmm ready"],
            ["assignment sesh", "lab complete", "onek kaj baki"],
            ["parbo na", "onek tough", "onek hard"],
        ],
    },
    "misc": {
        "ask": ["fb chalchis?", "game kheli?", "movie cholbi?", "aj tired"],
        "ans": [
            ["hahaha", "lol", "xD"],
            ["parbo na", "dekhi kal", "next time"],
            ["hmm", "ok", "acha"],
        ],
    },
}

# ---------------------------
# Chat generator (natural style)
# ---------------------------
def random_chat():
    category = random.choice(list(CHAT_CATEGORIES.keys()))
    asks = CHAT_CATEGORIES[category]["ask"]
    answers_pool = CHAT_CATEGORIES[category]["ans"]

    ask = random.choice(asks)
    ans = random.choice(answers_pool)

    # variation: fillers + emoji + spelling mix
    ans = [add_emoji(add_filler(a)) for a in ans]

    # sometimes add emoji to ask too
    if random.random() < 0.15:
        ask += random.choice(["!", "?", " 🤔", " 😅", " 😂", " 🤷‍♂️"])

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
# CLI
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="chat_pairs.jsonl")
    parser.add_argument("--n", type=int, default=10000)
    parser.add_argument("--array", action="store_true")
    args = parser.parse_args()

    generate_dataset(path=args.out, n_records=args.n, as_array=args.array)
