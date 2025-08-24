# Biased Tales 

Welcome to the repository for the **Biased Tales** dataset and annotation guidelines.

## 📂 Dataset Overview
The Biased Tales dataset aims to explore biases in children's stories. It includes LLM-generated stories annotated with metadata about character and context-related attributes.

## 📦 Data Format

Each record corresponds to a single story and its metadata.

| Field                  | Type        | Description                                                                        |
| ---------------------- | ----------- | ---------------------------------------------------------------------------------- |
| `id`                   | string      | Unique story identifier.                                                           |
| `story`                | string      | Full story text.                                                                   |
| `number`               | integer     | Story index within a generation batch (if applicable).                             |
| `model`                | string      | Source LLM or configuration used to generate the story.                            |
| `readability_fkes`     | float       | Flesch Reading Ease Score (higher = easier).                                       |
| `readability_fkg`      | float       | Flesch–Kincaid Grade Level.                                                        |
| `readability_cli`      | float       | Coleman–Liau Index.                                                                |
| `readability_ari`      | float       | Automated Readability Index.                                                       |
| `aoa`                  | float/int   | Approx. age of acquisition / target age (if computed).                             |
| `role`                 | string      | Narrative role of the focal character (e.g., protagonist, sidekick, antagonist).   |
| `ethnicity`            | string      | Ethnicity label for focal character (see guidelines).                              |
| `gender`               | string      | Gender label for focal character (see guidelines).                                 |
| `religion`             | string      | Religion label (if present/identifiable).                                          |
| `country`              | string      | Country setting referenced in the story.                                           |
| `nationality`          | string      | Nationality of focal character (if applicable).                                    |
| `geolocation`          | string      | Broader geo context (e.g., region, coordinates, or place name).                    |
| `urbun`                | string      | Urbanicity (e.g., urban/suburban/rural). *(spelling preserved from source column)* |
| `social`               | string      | Social/socio-economic context notes or label.                                      |
| `protagonist_attrs`    | string/JSON | Attribute list for the protagonist (e.g., `["curious","brave"]`).                  |
| `protagonist_category` | string      | Category bucket for protagonist (e.g., “child”, “animal”, “mythical”).             |


## 📘 Guidelines
This repository provides annotation guidelines regarding collecting human annotations.

## 📣 Citation

If you use Biased Tales, please cite:
@misc{biased_tales_2025,
  title  = {Biased Tales: A Dataset of LLM-Generated Children's Stories with Bias-Focused Annotations},
  author = {Rooein, Donya and contributors},
  year   = {2025},
  note   = {Dataset and guidelines},
  url    = {}
}

