The dataset.zip file contains 2 folders: `repo-data` and `repo-bug-data`
The `scripts` folder contains all the source code used to process data and generate the graphs.

## repo-data 
This folder contains 53 `.json` files, each belonging to one of the 53 Java open-source projects.
The sample JSON schema of a file from `hawtio` repository is given below:

```json


    {
        "hawtio-3976.json": {
            "Age": 794,
            "sloc": [11,11,11],
            "slocAsItIs": [11,14,14],
            "slocNoCommentPretty": [11,11,11],
            "diffSizes": [0,7,0 ],
            "bodychanges": [0,1,0], 
            "newAdditions": [0,5,0],
            "isGetter": [false,false,false],
            "isSetter": [false,false,false],
            "changeDates": [0,3,794],
            "isEssentialChange": [false,true,false],
            "isBuggy": [false,false,false],
            "changeTypes": ["Yintroduced","Ybodychange","Yfilerename"],
            "filename": "hawtio-3976.json",
            "authors": ["X","Y","Z"],
            "editDistance": [0, 68, 0],
            "repo": "hawtio"
        },
        "method_id": {...},
        "method_id": {...}
    }

```
The above method with id `hawtio-3976.json` has total 3 revisions which is why the array of values for a particular metric (e.g., sloc: `[11,11,11]`) are of length 3. `Index 0` of the array represents the introduction value of a particular metric for the above method.

### Description of the metrics
- `Age`: Age of the method in days
- `sloc`: Source line of code of a method without comment and blank lines
- `slocAsItIs`: Source line of code of a method with comment and blank lines
- `slocNoCommentPretty`: Source line of code pretty printed without comment and blank lines
- `diffSizes`: Total number of lines added + removed in git `diff`
- `bodychanges`: Contains value 0 or 1; where 1 implies occurrence  of body change
- `newAdditions`: Total number of lines added in git `diff`
- `isGetter`: Contains `true` or `false`; where `true` indicates it is a `get` method
- `isSetter`: Contains `true` or `false`; where `true` indicates it is a `set` method
- `changeDates`: Contains the date difference in days from when the method was introduced. Index `0` is always 0 which indicates the introduction date
- `isEssentialChange`: Contains `true` or `false`; where `true` indicates it is an essential change. Essential change includes: `Ybodychange`, `Ymodifierchange`, `Yexceptionschange`, `Yrename`, `Yparameterchange`, `Yreturntypechange` and `Yparametermetachange` detected by `CodeShovel`
- `isBuggy`: Contains `true` or `false`; where `true` indicates the method bug was fixed at a particular revision
- `changeTypes`: All transformations applied to the method at each revision. The full list of transformation that is detected by `CodeShovel` are: `Ybodychange`, `Ymodifierchange`, `Yexceptionschange`, `Yrename`, `Yparameterchange`, `Yreturntypechange`, `Yparametermetachange`, `Yannotationchange`, `Ydocchange`, `Yformatchange`, `Yfilerename` and `Ymovefromfile`
- `filename`: It is the method `id`

## repo-bug-data
This folder contains 53 `.json` files with bug information, each belonging to one of the 53 Java open-source projects.
The sample JSON schema of a file is given below:

```json
{
    "hawtio-3976.json":{
        "exactBug0Match": [false, false, false],
        "exactBug1Match": [false, false, false],
        "exactBug2Match": [false, false, false],
        "exactBug3Match": [false, false, false],
        "regExBug0": [false, false, false],
        "regExBug1": [false, false, false],
        "regExBug2": [false, false, false],
        "regExBug3": [false, false, false]
    },
    "method_id": {...},
    "method_id": {...},
}

```

The above method can be mapped to its metrics dataset using the `method_id`. For e.g., the above method with id `hawtio-3976.json` in `repo-bug-data/hawtio.json`that has 3 revision can be found in  the metric dataset using the same id `hawtio-3976.json` in the file `repo-data/hawtio.json`.

### Description of bug dataset
Each key in the above example contains value `true` or `false` indicating if a method was buggy or not at each revision. The `"hawtio-3976.json` method has 3 revisions (including method's introduction) which is why the array length is 3. The `keys` in the above json output represent `bug-fix` classification based on buggy keywords adopted from prior work.

We identified bug-fix commit using two approaches: 
1. Exact case insensitive match of buggy keywords from the commit message (keys prefix wih `exact` represent this)
2. Partial case insensitive substring match (using regular expression) excluding words that ends with `fix` or `bug`. (keys prefix with `regEx` represent this)

- `Bug0`: This is the approach that we have used for classifying bug-fix commit. Buggy keyword list: ["error", "bug", "fixes", "fixing", "fix", "fixed", "mistake", "incorrect", "fault", "defect", "flaw"]
- `Bug1`: Same keyword list as `exactBug0Match` with the addition of keyword `issues`
- `Bug2`: Buggy keyword list from prior work [[1]](#1): ["bug", "fix", "error", "issue", "crash", "problem", "fail", "defect", "patch"]
- `Bug3`: Buggy keyword list from prior work [[2]](#2): ["error", "bug", "fix", "issue", "mistake", "incorrect", "fault", "defect", "flaw", "type"]


## Appendix

53 projects information: [53ProjectsStats.csv](/Stats/53ProjectsStats.csv)

**RQ1**
- All Kendall Tau correlation values per repository: [RQ1-SLOCMeasures-CorrelationValuesPerRepo.csv](/Stats/RQ1/RQ1-SLOCMeasures-CorrelationValuesPerRepo.csv)
- Cliff's delta effect size and Mann-Whitney U test of difference in correlation values of SLOC with \#Revisions and \#Bugs for all methods in 53 projects: [RQ1-SLOCMeasures-all-methods.csv](/Stats/RQ1/RQ1-SLOCMeasures-all-methods.csv)
- Cliff's delta effect size and Mann-Whitney U test of correlation values of SLOC with \#Revisions and \#Bugs for methods modified at least once in 53 projects: [RQ1-SLOCMeasures-modified-methods.csv](/Stats/RQ1/RQ1-SLOCMeasures-modified-methods.csv)

**RQ2**
- All kendall Tau correlation values per repository of SLOC with revisions and bug density: [RQ2-SLOCControl-CorrelationValuesPerRepo.csv](Stats/RQ2/RQ2-SLOCControl-CorrelationValuesPerRepo.csv)
- Cliff's delta value and Mann-Whitney U test of the difference in revision and bug density between small, medium and large methods: [RQ2-SLOCControl-getSet.csv](/Stats/RQ2/RQ2-SLOCControl-getSet.csv)

**RQ3**
- Cliff's delta and Mann-Whitney U test for the difference in correlation values in 53 projects for SLOC with \#Revisions and \#Bugs in different time range: [RQ3-AgeNorm.csv](/Stats/RQ3/RQ3-AgeNorm.csv)

- Cliff's delta and Mann-Whitney U test for the difference in correlation values in 53 projects for SLOC with \#Revisions and \#Bugs in different time interval: [RQ3-interval.csv](/Stats/RQ3/RQ3-interval.csv)


## References
<a id="1">[1]</a> 
Zhang, F., Hassan, A. E., McIntosh, S., & Zou, Y. (2016). The use of summation to aggregate software metrics hinders the performance of defect prediction models. IEEE Transactions on Software Engineering, 43(5), 476-491.

<a id="2">[2]</a> 
Ray, B., Hellendoorn, V., Godhane, S., Tu, Z., Bacchelli, A., & Devanbu, P. (2016, May). On the" naturalness" of buggy code. In 2016 IEEE/ACM 38th International Conference on Software Engineering (ICSE) (pp. 428-439). IEEE.
