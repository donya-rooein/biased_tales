# %%
from typing import List
import csv
import tqdm
import numpy as np
import sentence_transformers
import collections

model_embd = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")

for model_name in ["all", "GPT4", "llama3", "Mixtral8x"]:
    def process_data(data):
        for line in data:
            if "ethnicity" in line:
                line["ethnicity"] = line["ethnicity"].replace("African-American", "African-Amer.").replace("European-American", "European-Amer.")
                
            if "nationality" not in line:
                continue
            x = line["nationality"]
            line["nationality_group"] = (
                "North American" if x in {"American", "Canadian"} else
                "South American" if x in {"Mexican", "Brazilian"} else
                "European" if x in {"British", "German", "French", "Italian", "Russian"} else
                "Middle Eastern" if x in {"Armenian", "Afghan", "Azerbaijani", "Egyptian", "Iranian", "Iraqi"} else
                "Africa" if x in {"Ethiopian", "Kenyan", "Malian", "Nigerian", "South African", "Sudanese"} else
                "Asia" if x in {"Chinese", "Filipino", "Indian", "Indonesian", "Japanese", "Sri Lankan", "Tajik", "Thai", "Vietnamese"} else
                "Other"
            )
            line["nationality_developed"] = (
                "Developed" if x in {"American", "British", "Canadian", "French", "German", "Italian", "Japanese", "Russian"} else
                "Developing" if x in {"Afghan", "Armenian", "Azerbaijani", "Brazilian", "Chinese", "Egyptian", "Ethiopian", "Filipino", "Indian", "Indonesian", "Iranian", "Iraqi", "Kenyan", "Malian", "Mexican", "Nigerian", "South African", "Sri Lankan", "Sudanese", "Tajik", "Thai", "Vietnamese"} else
                "Other"
            )
        return data

    data = process_data(list(csv.DictReader(open('data/stories_v2.csv', 'r'))))
    if model_name != "all":
        data = [line for line in data if line["model"] == model_name]

    def get_diversity_list_embd(data: List[dict]):
        embd = model_embd.encode([line["story"] for line in data])
        embd = np.array(embd)
        # average cosine similarity
        sim = np.dot(embd, embd.T)
        sim = sim / np.linalg.norm(embd, axis=1) / np.linalg.norm(embd, axis=1)[:, np.newaxis]
        sim = np.average(sim)
        return sim

    def get_diversity_list_unigram(data: List[dict]):
        embds = [set(line["story"].split()) for line in data]
        sims = []
        for embd1_i, embd1 in enumerate(embds):
            for embd2 in embds[embd1_i+1:]:
                if embd1 != embd2:
                    sim = len(embd1 & embd2) / len(embd1 | embd2)
                    sims.append(sim)
        
        return np.average(sims)

    results = collections.defaultdict(dict)

    def get_diversity_all(key: str):
        values_uniq = {
            line[key]
            for line in data
        }
        for value in tqdm.tqdm(values_uniq):
            data_filtered = [row for row in data if row[key] == value]
            print(f"{key}: {value} ({len(data_filtered)})")
            results[key][value] = get_diversity_list_embd(data_filtered)


    get_diversity_all("nationality")
    get_diversity_all("nationality_developed")
    get_diversity_all("nationality_group")
    get_diversity_all("gender")
    get_diversity_all("ethnicity")
    get_diversity_all("religion")
    get_diversity_all("role")

    with open(f"generated/04-diversity_{model_name}.tex", "w") as f:
        f.write(r"\begin{tabular}{l>{\raggedright\arraybackslash}p{12cm}}")
        f.write(r"\toprule")
        for key, values in results.items():
            f.write(
                r"\bf " +
                (
                    key.replace("_", " ").title()
                    .replace("Nationality Parent Developed", "Nationality Developed")
                    .replace("Nationality Parent Group", "Nationality Group")
                ) +
                " & "
            )
            # map interval from [-0.45, -0.15] to [0, 100]
            cell_color = lambda x: f"\\hlc[yellow!{int((x - 0.46) / (0.62-0.46) * 100)}!blue!20]" 
            values = list(values.items())
            values.sort(key=lambda x: x[1])
            # remove empty ones (in ethnicity)
            values = [(value, result) for value, result in values if value != ""]
            f.write(
                " ".join([f"{cell_color(result)}{{{value.replace('American', 'Amer.').replace(' ', '~')}={result:.0%} }}".replace("%", r"\%") for value, result in values]) +
                " \\\\ \\\\[-0.4em]"
            )
        f.write(r"\bottomrule")
        f.write(r"\end{tabular}")
