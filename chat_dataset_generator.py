# -*- coding: utf-8 -*-
# Chat dataset generator (Bangla + Banglish)
# Usage:
#   python chat_dataset_generator.py --out chat_pairs.jsonl --n 1000000
import json, random, re, argparse

random.seed(42)

PRONOUNS = ["tui", "tumi", "apni"]
TIME_WORDS = ["sokal", "dupure", "bikal", "raat", "shondha", "aj", "kal", "porshur", "ekhuni", "ekto pore"]
TIME_WORDS_BN = ["সকাল", "দুপুরে", "বিকাল", "রাত", "সন্ধ্যা", "আজ", "কাল", "পরশু", "এখনই", "একটু পরে"]
EMOJIS = ["🙂","😅","😂","🤔","🙃","🥹","😴","😎","✨","🔥","❤️","👍","🙌","🤝","🤟","🤷‍♂️","🤷‍♀️"]
PUNCS = ["?", "?!", "...?", "!!", "?!", "…?"]

def maybe_emoji(s):
    import random
    if random.random() < 0.25:
        return s + " " + random.choice(EMOJIS)
    return s

def maybe_punc(s):
    import random
    if not s.endswith(tuple("?!")) and random.random() < 0.7:
        return s + random.choice(PUNCS)
    return s

def maybe_lower(s):
    import random
    if random.random() < 0.15:
        return s.lower()
    return s

def bangla_or_banglish(s):
    import re, random
    if re.search(r"[\\u0980-\\u09FF]", s):
        return s
    s = maybe_lower(s)
    if random.random() < 0.2:
        s = s.replace("bh", random.choice(["b","v"]))
    if random.random() < 0.15:
        s = s.replace("th", "t")
    if random.random() < 0.1:
        s = s.replace("ee", "i")
    return s

ANS = {
    "greet": [
        ["hi", "hello", "hey"],
        ["হাই", "হ্যালো", "ওহে"],
        ["hello hello", "hey there", "yo"],
        ["কেমন আছো?", "ভালো আছি", "তুমি?"]
    ],
    "wellbeing": [
        ["ভালো আছি", "মোটামুটি", "আজকে একটু tired"],
        ["bhalo", "valo achi", "onak bhalo vibe"],
        ["alhamdulillah bhalo", "good good", "you tell"],
        ["চলছে", "ম্যানেজ হচ্ছে", "তুই কেমন?"]
    ],
    "where": [
        ["বাড়িতে", "ঢাকায়", "উত্তরায়"],
        ["home e", "office e", "campus e"],
        ["road e", "bus e", "class e"],
        ["মায়ের কাছে", "বন্ধুর বাসায়", "লাইব্রেরি"]
    ],
    "doing": [
        ["class e", "kaj kortesi", "khali chill"],
        ["খাচ্ছি", "ঘুমাচ্ছি", "সিরিজ দেখছি"],
        ["meeting e", "assignment likhtesi", "game khelchi"],
        ["bashe boshe asi", "walk dite gesi", "drive kortesi"]
    ],
    "plan_invite": [
        ["hobe", "sure", "cholo jabo"],
        ["parbo na", "next time", "dekhi kal"],
        ["ok", "confirm korbo", "maybe"],
        ["জায়", "যাই", "চলো যাই"]
    ],
    "time": [
        ["ekhon", "koyta baje bolo", "thik bujhlam na"],
        ["এখন", "কিছুক্ষণ পরে", "রাতে"],
        ["9 ta hobe", "shondhay beshi hoy", "kal notun kore dekhbo"],
        ["ok", "thik ache", "note korlam"]
    ],
    "meet": [
        ["chole asho", "map pathacchi", "wait korbo"],
        ["parbo na", "porer din", "kal jodi hoy"],
        ["tikache", "see you", "on my way"],
        ["আসছি", "পৌঁছে যাচ্ছি", "গেটে আছি"]
    ],
    "food": [
        ["চল খাই", "biriyani?", "burger?"],
        ["khawa sesh", "coffee lagbe", "cha dibo"],
        ["বাসার খাবার", "ক্যান্টিন", "street food"],
        ["ranna korchi", "hungry", "ডায়েট করতেছি"]
    ],
    "ent": [
        ["movie?", "ott te ki ache", "series recommend kor"],
        ["game on", "valo lobby", "rank push?"],
        ["gaan shunbo", "concert jabo?", "reel banabi"],
        ["হল এ যাবো", "টিকিট পাইলে যাই", "late show"]
    ],
    "weather": [
        ["বৃষ্টি পড়ছে", "গরম", "হাওয়া ভালো"],
        ["rainy", "onak heat", "cool hoyeche"],
        ["আজ storm ashte pare", "umbrella nao", "ভিজে গেলে call dio"],
        ["ac on korchi", "outside jabo na", "meh"]
    ],
    "net_power": [
        ["loadshedding", "net slow", "router reboot diya"],
        ["light gelo", "pc off", "backup on"],
        ["wifi thik ache", "mobile data e ashi", "hotspot dibo"],
        ["আসে", "নেই", "দেখি কি হয়"]
    ],
    "thanks": [
        ["thanks", "thank you", "শুকরিয়া"],
        ["onak dhonnobad", "appreciate it", "valo laglo"],
        ["❤️", "🙏", "ধন্যবাদ ভাই"],
        ["means a lot", "saved me", "legend"]
    ],
    "apology": [
        ["sorry", "bhul hoye gese", "amar doss"],
        ["ক্ষমা কর", "দুঃখিত", "আর হবে না"],
        ["late hoye gesi", "traffic chilo", "bolo ki kora lagbe"],
        ["next time careful thakbo", "noted", "my bad"]
    ],
    "study": [
        ["sesh", "ekto baki", "rat e korbo"],
        ["আজ hobe", "sir bolse cancel", "quiz tough"],
        ["note dibo", "drive e rekhechi", "inbox check"],
        ["ভাল হয়েছে", "পাস করছি", "next bar better"]
    ],
    "work": [
        ["meeting e", "later ping", "calendar inv sent"],
        ["deadline kal", "extend hobe", "done almost"],
        ["leave nilam", "onsite aj", "wfh"],
        ["salary paisi", "ek dui diner moddhe", "HR e mail"]
    ],
    "health": [
        ["bhalo", "ekto cold", "med nitesi"],
        ["fever chilo", "ekhon kom", "rest nitesi"],
        ["gym jabo", "aj skip", "kal chest"],
        ["ঘুম কম", "টেনশন কমাতে হবে", "পানি খাচ্ছি"]
    ],
    "transport": [
        ["uber peye gelam", "path nilam", "aschi"],
        ["bus e", "jam onek", "late hobe"],
        ["bike e jachi", "rickshaw dilam", "foot e aschi"],
        ["landing 8 ta", "train 6:30", "flight delay"]
    ],
    "shopping": [
        ["online e", "store visit", "compare kortesi"],
        ["cash on", "bkash", "card"],
        ["kal delivery", "same day", "pick up korbo"],
        ["coupon paisi", "no coupon", "price komano jay"]
    ],
    "sports": [
        ["jitse", "hariye gelo", "draw"],
        ["awesome match", "boring chilo", "last over e"],
        ["score 2-1", "century hoyeche", "penalty diye jitse"],
        ["practice kal", "aj rest", "coach happy"]
    ]
}

ASK_BANK = []
def add(cat, texts):
    for t in texts:
        ASK_BANK.append((cat, t))

add("greet", ["hi","hello","hey","hie","yoo","hey there","হাই","হ্যালো","ওই","কি খবর","শুনছো","আরে","কেমন আছো"])
add("wellbeing", ["kemon acho","kemon aso","valo aso?","bhalo aso?","কেমন আছো","কি খবর","ভালো তো","সব ঠিকঠাক?","আজ কেমন লাগছে"])
add("where", ["tui koi","koi aso","kothay","kothay acho","kothay asho","কোথায়","তুই কোথায়","কোথায় আছো","এখন কোথায়","কোথায় ছিলে"])
add("doing", ["ki korcho","ki korsos","ki korteso","ki korsis","কি করছো","কি করছিলে","এখন কি করছো","busy naki","free acho"])
add("plan_invite", ["ber hobo?","coffee jabi?","cha khabi?","ghurte jabi?","movie jabi?","game khelbi?","meet korbo?","call dibo?","দেখা হবে?","চা খাই?","আজ বেরুবা?","একটু আউট হই"])
add("time", ["kobe ashbi","kobe free","koytay start","koyta baje","aj kobe","কখন আসবে","কত টায়","আজ কয়টা","কখন সময় পাবি","টাইম দিবি"])
add("meet", ["kothay meet","place confirm","map patha","gate e asho","jibon tower e?","uttara sector 4?","dukan er samne","campus gate?","গেটে আসো","লাইব্রেরি সামনের বেঞ্চে","কোথায় দেখা"])
add("food", ["khawa ki","khawa ki hobe","vaja khabi?","biriyani cholbe?","burger naki pizza","বাসায় খাইছো?","ফুচকা খাবি?","ডায়েট চলি?"])
add("ent", ["movie dekhbi?","series suggest kor","game khelbi?","rank push?","gaan shunbi?","concert jabi?","reel banabi?","ott e ki ache","হল এ যাবি?","টিকিট পাবো?","লাস্ট শো নাকি ম্যাটিনি"])
add("weather", ["brishti porbe?","aj brishti?","onek gorom","thanda lagche","আবহাওয়া কেমন","বৃষ্টি হবে?","গরম পড়ছে","কুয়াশা পড়বে?"])
add("net_power", ["net kacche","wifi chole?","router restart korbi?","net slow","light gelo?","loadshedding?","charge koita%","battery down","বিদ্যুৎ আছে?","নেট কেমন","ইন্টারনেট নাই"])
add("thanks", ["thanks","thank you","ধন্যবাদ","অনেক ধন্যবাদ","appreciate it"])
add("apology", ["sorry","doya kore maf","ভুল হয়ে গেছে","দুঃখিত","my bad"])

def expand_pronoun(patterns_bn, patterns_en, cat):
    for p in patterns_en:
        for pr in PRONOUNS:
            add(cat, p.replace("{you}", pr))
    for p in patterns_bn:
        add(cat, p)

expand_pronoun(
    patterns_bn=["তুমি কি করছো","তুমি কেমন আছো","আজ কী প্ল্যান","আজ কোথায়","কখন আসবে","চলো দেখা করি","চা খেতে যাবা","এখন ফ্রি নাকি","কাজ কেমন চলছে","মন কেমন","ঘুম থেকে উঠেছো?","বাসায় আছো?"],
    patterns_en=["{you} ki obostha","{you} kothay","{you} aj ki korbi","{you} kal free naki","{you} ki khawabi","{you} khelbi aj","{you} school jachho?","{you} office e naki","{you} raat e time dibi","{you} call nibi","{you} msg korbi?"],
    cat="mixed"
)

for tw in TIME_WORDS:
    add("time", f"{tw} kobe ashbi")
    add("doing", f"{tw} ki korcho")
    add("plan_invite", f"{tw} ber hobo")
    add("where", f"{tw} kothay thakbi")

for tw in TIME_WORDS_BN:
    add("time", f"{tw} কখন আসবি")
    add("doing", f"{tw} কি করছিস")
    add("plan_invite", f"{tw} বের হবো")
    add("where", f"{tw} কোথায় থাকবি")

add("study", ["assignment sesh?","report likhso?","exam kemon holo","lab ache?","read korbi?","group study korbo?","sir class niben?","quiz hobe?","ফলাফল কবে","প্রেজেন্টেশন বানাইছো?","নোট দিবি?"])
add("work", ["standup koi tay","deadline ase","jira ticket niye kaj","meeting ache?","leave niteso?","office jachho?","remote naki onsite","salary elo?","কাজ দিচ্ছে?","বস ডেকেছে?","পে-স্লিপ পাইছো?"])
add("health", ["mon bhalo?","cold lagse?","jhor?","fever ase?"," মাথা ব্যাথা?","doctor dekhaso?","শরীর কেমন","ঘুম হইছে?","gym jabi?"])
add("transport", ["uber dhorte parbi?","bus pabi?","train kobe","flight koto tay","jam koto","traffic onek","bike e jabi?","rickshaw nibi?","গাড়ি আছে?","সিএনজি ধরবি?","বাসায় নিতে আসবা?"])
add("shopping", ["bazaar jabi?","kisu kinbi?","sale chalche?","shohag store e jabi?","dress nibo","shoe lagbe","gift nibo","book fair jabi?","অনলাইনে নাকি দোকান","কুপন আছে?","ডেলিভারি কবে"])
add("sports", ["match dekhli?","gelam stadium?","cricket kemon holo","football aj","messi goal dil?","bd jitse?","ipl dekhbi?","practice korbi?","জিমে জাস?","কোচ ডাকছে?","স্কোর কতো"])

ASK_BANK = list(dict.fromkeys(ASK_BANK))

def sample_answers(cat, k=None):
    import random
    pool = random.choice(ANS.get(cat, [["ok"]]))
    out = list(dict.fromkeys(pool))
    if random.random() < 0.35:
        out.extend(random.choice(ANS.get(cat, [["ok"]]))[:2])
    if k is None:
        k = random.randint(3, 6)
    random.shuffle(out)
    return out[:k]

def make_ask(cat, text):
    t = text
    if not t.endswith(tuple("?!।")):
        t = maybe_punc(t)
    t = maybe_emoji(t)
    t = bangla_or_banglish(t)
    return t

def make_pair():
    import random
    cat, text = random.choice(ASK_BANK)
    ask = make_ask(cat, text)
    ans = sample_answers(cat)
    out = []
    seen = set()
    for a in ans:
        a = bangla_or_banglish(a)
        if random.random() < 0.25:
            a = maybe_punc(a)
        if random.random() < 0.25:
            a = maybe_emoji(a)
        if a not in seen:
            out.append(a)
            seen.add(a)
    while len(out) < 3:
        out.append("ok")
    return {"ask": ask, "ans": out}

def generate(path, n=10000, as_array=False):
    count = 0
    if as_array:
        with open(path, "w", encoding="utf-8") as f:
            f.write("[")
            for i in range(n):
                obj = make_pair()
                if i > 0:
                    f.write(",")
                f.write(json.dumps(obj, ensure_ascii=False))
                count += 1
            f.write("]")
    else:
        with open(path, "w", encoding="utf-8") as f:
            for i in range(n):
                obj = make_pair()
                f.write(json.dumps(obj, ensure_ascii=False) + "\\n")
                count += 1
    return count

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="chat_pairs.jsonl", help="output path (.jsonl or .json)")
    ap.add_argument("--n", type=int, default=100000, help="number of records")
    ap.add_argument("--array", action="store_true", help="write as a single JSON array instead of JSONL")
    args = ap.parse_args()
    generate(args.out, n=args.n, as_array=args.array)
