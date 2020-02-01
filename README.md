# Coronavirous Research and Insights Share
Epidemic prediction and estimation of 2019-nCoV

#### Date: Since Jan 26 2020

***
### Goals: (draft)
1. Translate the statistical models in the publihsed paper into python.
   - Update/track by new (real-time) data.
   - Compare with the reality: understanding models' limitation.
   - Try to improve model's estimation/prediction/inference further.
1. Collect data and Build dashboard for real-time visualisation.
1. Insights sharing


## Projects:
1. [Estimating the potential number of cases in Wuhan before shut down](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
   - Author: Yiran Jing
   - Reference: [report2 (Jan 21)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)
2. Visualisation Dashboard
***
## Data Sources
- Merged Dataset output: [data/mergedData/combined.csv](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/data/mergedData/combined.csv)
- Referenced: [coronavirus-ds](https://github.com/pdtyreus/coronavirus-ds)
The data for tracking the 2019-nCoV outbreak is provided by the [Johns Hopkins Center for Systems Science and Engineering](https://systems.jhu.edu/research/public-health/ncov/)

### Pulling Updates from Google Sheets

The data is updated in a read-only [Google Sheet](https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w).

Download credentials and install dependencies as described [in the Google documentation.](https://developers.google.com/sheets/api/quickstart/python).

```shell script
python pull_gsheet_csse.py  # within data folder
```
***

## Other projects on github
1. [Modelling of the nCoV-2019 outbreak in Wuhan](https://github.com/chrism0dwk/wuhan)
   - Author: Jon Read, Jess Bridgen, and Chris Jewell at Lancaster University
1. [微信公众号实时查询感染人数](https://github.com/echo-cool/2019-nCov)
   - Author: [echo-cool](https://github.com/echo-cool)
2. [2019新型冠状病毒疫情实时爬虫](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)
   - Author: [Isaac Lin](https://github.com/BlankerL)

***

### Key Reference
1. [Early Transmission Dynamics in Wuhan (Jan 29)](https://www.nejm.org/doi/full/10.1056/NEJMoa2001316)
1. [WHO report (Jan 23)](https://www.who.int/docs/default-source/coronaviruse/situation-reports/20200123-sitrep-3-2019-ncov.pdf)
2. [Estimating the potential total number of novel
Coronavirus cases in Wuhan City, China (Jan 21 2020)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)
    - [Statistical model and Python code](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
3. [Transmissibility of 2019-nCoV (Jan 24)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-2019-nCoV-transmissibility.pdf)
4. [Epidemic Prediction by UK scientists (Jan 24 2020)](https://www.medrxiv.org/node/71375.external-links.html)


***
## Welcome to join us!!
Please connect with us if you are interested in this project!
#### Require Skills: (at least one below)
1. Python/R (e.g. Data cleaning/processing, Plotting, modelling etc. )
2. Statistics/mathematics
3. Epidemic knowledge
4. Tableau/PowerBI
6. Corporate skills

- Email: yjin5856@uni.sydney.edu.au
- Wechat: A570281374
