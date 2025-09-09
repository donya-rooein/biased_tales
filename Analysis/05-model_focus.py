# %%
import csv
import collections

data = list(csv.DictReader(open('data/stories_v2.csv', 'r')))
data_agg = collections.defaultdict(collections.Counter)

for line in data:
    attributes = eval(line["protagonist_category_gpt4"].lower())
    # sometimes we get a not found message
    attributes = [x for x in attributes if len(x) < 20]
    data_agg[line["model"]].update(attributes)

# %%

MODEL_TO_NAME = {
    "GPT4": "GPT4",
    "llama3": "Llama3",
    "Mixtral8x": "Mixtral",
}

for category in ["physical", "emotional", "mental", "moral", "other"]:
    print(category.capitalize(), "&")
    for model in ["GPT4", "llama3", "Mixtral8x"]:
        total = sum(data_agg[model].values())
        print(
            # MODEL_TO_NAME[model],
            f"{data_agg[model][category] / total:.0%}".replace("%", "\\%"),
            end=" & ",
        )
    print("\\\\")