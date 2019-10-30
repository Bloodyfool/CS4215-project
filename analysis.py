#!/usr/bin/env python3

import csv
import pandas as pd
import researchpy as rp
import statsmodels.api as sm
import statsmodels.stats.anova as anova
import statsmodels.formula.api as ols
import os

DIRECTORY = "experiments"

experiment_names = [experiment for experiment in os.listdir(DIRECTORY)]

# print(experiments)

def Average(lst):
    return sum(lst) / len(lst)

def get_labels_csv(name):
    return name.split("_")[1:4]

def get_experiment_line(name):
    labels = get_labels_csv(name)
    sparkgen = open(DIRECTORY+"/"+name+"/sparkgen", "r")
    durations = list()
    for line in sparkgen:
        if ",true" in line:
            _, _, _, _, start, end = line.strip().split(",")
            exp = labels.copy()
            exp.append(float(end)-float(start))
            durations.append(exp)
    return durations

def get_averaged_experiment(experiment):
    return Average([run[-1] for run in experiment])

def get_averaged_experiment_with_label(experiment):
    label = experiment[0].copy()[:-1]
    label.append(int(get_averaged_experiment(experiment)))
    print(label)
    return label

experiments = [get_experiment_line(experiment) for experiment in experiment_names]

avg_experiments = [get_averaged_experiment(experiment) for experiment in experiments]
experiments_avg = ["-1", "-1", "-1", Average(avg_experiments)]

all_durations = [x for y in experiments for x in y]

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter = "&")
    writer.writerows([get_averaged_experiment_with_label(experiment) for experiment in experiments])

df_anova = pd.DataFrame(all_durations)
df_anova.columns = ['CPU', 'RAM', 'MR', 'duration']

all_durations.insert(0, experiments_avg)
df = pd.DataFrame(all_durations)
df.columns = ['CPU', 'RAM', 'MR', 'duration']

model_duration = ols.ols('duration ~ C(CPU)*C(RAM)*C(MR)', df).fit()
model_duration_anova = ols.ols('duration ~ C(CPU)*C(RAM)*C(MR)', df_anova).fit()
print(f"Duration Model: Overall model F({model_duration.df_model: .0f},{model_duration.df_resid: .0f}) = {model_duration.fvalue: .3f}, p = {model_duration.f_pvalue: .4f}")

summ = model_duration.summary()
# print(summ)

res_duration = sm.stats.anova_lm(model_duration_anova, typ= 2)
# print(res_duration)

with open('anova_duration2.tex','w') as tf:
    tf.write(res_duration.to_latex(index=True))

with open('model_duration2.tex','w') as tf:
    tf.write(model_duration.summary().as_latex())

