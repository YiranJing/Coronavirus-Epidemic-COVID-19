# Estimating current cases in Wuhan

#### Author: Yiran Jing
#### Date: Jan 26 - Jan 28 2020

Goal: Re-produce model in [Estimating the potential total number of novel Coronavirus cases in Wuhan City, China (Jan 21 2020)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)

Based on cases detected outside mainland China. **We use Observation on Jan 22**. Since on 2 am Jan 23, Wuhan shut down.


## Conclusion:
- There are at least **4600** (2100, 8550) cases in Wuhan, until Jan 19. (There is time deley between suspected and confirmed)
- Based on 29 confirmed overseas cases in Jan 26, There are at least more than 16000 cases(11310, 23480) until Jan 23.
- **Human migration control** has significant impact on `epidemic growth rate`
***

## Statistical Modelling:

### Sensitivity analysis:
Sensitivity analysis to estimate current cases in wuhan based on 4 scenario
1. Baseline
     - **8** overseas confirmed cases until 22 Jan.
     - 10 mean time to detection
     - 19000000 airportCatchment
2. Smaller catchment:
     - airportCatchment = wuhan_population = 11000000
3. Shorter detection window:
     - 8 mean time to detection
4. More exported cases:
     - **29** overseas confirmed cases until 26 Jan.

### Profile likelihood CI
In general, the confidence interval based on the standard error strongly depends on the assumption of normality for the estimator, which is something we cannot guarantee in this case. The "profile likelihood confidence interval" provides an alternative.

We defined a Binomial likelihood for the number of exported cases and used this function to find the MLE of the number of cases in Wuhan, using the profile likelihood approach to identify the 95% CI around the MLE. The lower and upper bounds of the 95%CI are those values by which the log-likelihood difference from the maximum log-likelihood is 1.92 (95%-percentile of the Chi-square(1) distribution).


***

## Key assumptions:

#### 95% Confidence interval (uncertainty range) represents uncertainty in Epi-based assumptions as well as statistical assumptions

### Epi-based assumptions
1. Unable to estimate the epidemic growth rate
2. Total number of international travel from Wuhan over the last 2 months has been [3301](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf) per day.
   - This number is based on previous year data, we can calculate more accurately by airport data of 2019
   - This number is 0 after Jan 23 (Wuhan shut down)
3. Estimates donot include cases with mild or no symptoms
4. The incubation period is unknown, and has been approximated by MERS-nCov and SARS.

### Statistical assumptions

1. We assume `independent relationship` between `exported cases` and `confirmed cases` within Wuhan
    - However, exit screening may have reduced exports in recent days
    - Outcome: underestimate of the true number
2. The number of cases detected overseas is **binomially distributed** with Binomial(p), where p is the probability any one caze will be detected overseas.
    - This assumption only influence the interval estimation
3. Assume international travel is independent of the risk of exposure to 2019n-CoV and infection status.
    - However, the international traveller might be wealthier people and with lower risk of exposure to 2019n-CoV

***
### Issues uncovered in paper:
1. Consider **Suspected cases** in the model:
    - the cases havenot been confirmed
    - `Time delay`, official under-report
    - Official report there meybe 1000 cases more in Wuhan (Jan 26)
        1. 确诊比例在45%以上,（截止26日，武汉有2209位疑似病例未被检测，643位留院观察）
