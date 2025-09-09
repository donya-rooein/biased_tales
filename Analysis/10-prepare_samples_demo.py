# %%
import csv
import os
import json
import gzip

data = list(csv.DictReader(open('data/stories_v5.csv', 'r')))

data_out = []
for line_i, line in enumerate(data):
    categories_category = eval(line["protagonist_category_gpt4"].lower())
    categories_values = eval(line["protagonist_gpt4"].lower())
    if len(categories_category) != len(categories_values):
        continue
    # sometimes we get a not found message
    categories = [x for x in zip(categories_values, categories_category) if len(x[0]) < 20 and len(x[1]) < 20]

    # x = line["nationality"]
    # line["ethnicity_group"] = (
    #     "North American" if x in {"American", "Canadian"} else
    #     "South American" if x in {"Mexican", "Brazilian"} else
    #     "European" if x in {"British", "German", "French", "Italian", "Russian"} else
    #     "Middle Eastern" if x in {"Armenian", "Afghan", "Azerbaijani", "Egyptian", "Iranian", "Iraqi"} else
    #     "Africa" if x in {"Ethiopian", "Kenyan", "Malian", "Nigerian", "South African", "Sudanese"} else
    #     "Asia" if x in {"Chinese", "Filipino", "Indian", "Indonesian", "Japanese", "Sri Lankan", "Tajik", "Thai", "Vietnamese"} else
    #     ""
    # )
    data_out.append({
        "id": line["id"],
        "story": line["story"],
        "categories" : dict(categories),
        "complexity_aoa": f'{float(line["aoa"]):.2f}',
        "complexity_fkg": f'{float(line["readability_fkg"]):.2f}',
        "complexity_fkes": f'{float(line["readability_fkes"]):.2f}',
        "g_model": line["model"],
        "g_nationality": line["nationality"],
        "g_country": line["country"],
        "g_gender": line["gender"],
        "g_ethnicity": line["ethnicity_group"],
        "g_religion": line["religion"],
        "g_role": line["role"],

        "s_location": line["geolocation_gpt4"],
        "s_urban": line["urbun_gpt4"],
        "s_social": line["social_gpt4"],
    })


os.makedirs('../demo/web/stories', exist_ok=True)

with gzip.open('../demo/web/stories/data_all.json.gz', 'wt', encoding='utf-8') as f:
    f.write(json.dumps(data_out, ensure_ascii=False))

# save json
with open("../demo/web/stories/data_all.json", "w") as f:
    f.write(json.dumps(data_out, ensure_ascii=False))

# %%

print(line.keys())