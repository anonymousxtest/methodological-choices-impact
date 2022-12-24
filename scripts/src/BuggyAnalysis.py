import csv

import pandas as pd
from matplotlib import pyplot as plt

from src.Final.AbstractReader import AbstractReader
from src.Final.FileUtil import FileUtil
from src.Final.constants import Constants
import seaborn as sns


class BuggyAnalysis(AbstractReader):
    def __init__(self):
        self.BUGGY_CODE = ["error", "bug", "fix", "mistake", "incorrect", "fault", "defect", "flaw", "type"]
        self.ISSUE = "issue"
        self.result = []
        super(BuggyAnalysis, self).__init__()

    def process(self, method_hist):
        bug_count = 0
        for commit, hist in method_hist["changeHistoryDetails"].items():
            contains_bug = set(hist["commitMessage"].split()) & set(self.BUGGY_CODE)
            if contains_bug:
                bug_count += 1

        self.result.append({
            "bugCount": bug_count,
            "changeCount": len(method_hist["changeHistory"]),
            "repo": self.repo,
            "filename": self.filename
        })


    def save_json(self):
        FileUtil.save_json(Constants.BUGGY_ANALYSIS + 'bug_data.json', self.result)
        print("save json in {0}".format(Constants.BUGGY_ANALYSIS + 'bug_data.json'))

    def analyze(self):
        if not self.result:
            self.result = FileUtil.load_json(Constants.BUGGY_ANALYSIS + 'bug_data.json')
        df = pd.DataFrame.from_dict(self.result)
        corr_result = []
        all = df[['bugCount', 'changeCount']]
        all_corr = all.corr(method="spearman")
        corr_result.append({"repo": "all", "corr": all_corr.iloc[0][1]})

        for repo in Constants.ALL_REPOS:
            repo_data = df[df['repo'] == repo]
            r = repo_data[['bugCount', 'changeCount']]
            val = r.corr(method="spearman")
            corr_result.append({"repo": repo, "corr": val.iloc[0][1]})


        self.write_csv(corr_result)
        self.plot_box(["commons-io", "jna", "checkstyle", "gson", "titan", "commons-lang"], df)
        self.plot_box(["pmd","okhttp","mockito", "wicket","ant","hibernate-search", "jgit", "javaparser"], df)

    def write_csv(self, result):
        with open(Constants.BUGGY_ANALYSIS + "buggy_vs_change.csv", 'w') as csvfile:
            fieldnames = ['repo', 'corr']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for r in result:
                writer.writerow(r)
        print("CSV writing done in {0}".format(Constants.BUGGY_ANALYSIS + "buggy_vs_change.csv"))


    def plot_box(self, repos, df):
        boolean_series = df.repo.isin(repos)
        filtered_df = df[boolean_series]
        filtered_df.boxplot(by="repo", column=['bugCount'])
        plt.show()



b = BuggyAnalysis()
# b.read_all_files_in_tar_dir()
b.analyze()