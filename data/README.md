
***
## Data Sources
- Merged Dataset output: [data/mergedData/combined.csv](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/data/mergedData/combined.csv)
- Referenced: [coronavirus-ds](https://github.com/pdtyreus/coronavirus-ds)
The data for tracking the 2019-nCoV outbreak is provided by the [Johns Hopkins Center for Systems Science and Engineering](https://systems.jhu.edu/research/public-health/ncov/)

#### Pulling Updates from Google Sheets

The data is updated in a read-only [Google Sheet](https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w).

Download credentials and install dependencies as described [in the Google documentation.](https://developers.google.com/sheets/api/quickstart/python).

```shell script
pip install -r ../requirements.txt
python pull_gsheet_csse.py  # within data folder
```
