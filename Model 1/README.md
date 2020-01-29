# Estimating Potential Outbreak Size in Wuhan until 22 Jan

#### Author: Yiran Jing
#### Date: Jan 26 - Jan 29 2020

### Goal:
1. Re-produce model in [Estimating the potential total number of novel Coronavirus cases in Wuhan City, China (Jan 21 2020)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)
2. Estimate potential Outbreak Size in Wuhan until 22 Jan using the number of cases detected overseas on Jan 22, Jan 26 and Jan 29. (2 am Jan 23, Wuhan shut down). We believe the estimated result based on the observation of 29 Jan is more accurate.(See details below)

The sample, used in the model estimation, is the number of cases detected outside mainland China (international travel from Wuhan). We use Observation on Jan 22, Jan 26 and Jan 29.
- 8 detected cases overseas until 22 Jan. (they are all out from Wuhan)
- 29 detected cases overseas until 26 Jan (they are all out from Wuhan).
- 67 detected cases overseas until 29 Jan (they are all out from Wuhan).

## Main Conclusion:
**Since 29 Jan is 6 days after Wuhan Shut down, most overseas cases have been detected until 29 Jan. We believe the estimated result based on the observation of 29 Jan is more accurate.**

- There are at least **4600** 95% CI(2100, 8550) cases in Wuhan, until Jan 19. (There is time deley between suspected and confirmed)
- Based on 29 confirmed overseas cases in Jan 26, There are at least more than **16600** cases 95% CI (11310, 23480) before Jan 23.
- Based on 67 confirmed overseas cases in Jan 29, There are at least more than **38500** cases 95% CI (30000, 48470) before Jan 23.
- **Commuting flows** has significant impact on `2019-nCov epidemic growth rate`

***

## Statistical Modelling:

Suppose population follows binomial distribution Bin(p,N)
- p: probability any one case will be detected overseas (international travel from Wuhan)
- n: negative binomially distributed function of X (number of cases detected outside mainland China)

### Sensitivity analysis:
Sensitivity analysis to estimate current cases in wuhan based on 3 scenarios:
1. Baseline
     - **8** or (67) overseas confirmed cases until 22 Jan.
     - 10 day mean time to detection
     - 19 million airportCatchment
2. Smaller catchment:
     - airportCatchment = wuhan_population = 11 million
3. Shorter detection window:
     - 8 day mean time to detection

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
2. The number of cases detected overseas is **binomially distributed** with Binomial(p), where p is the probability any one case will be detected overseas.
    - This assumption only influence the interval estimation
3. Assume international travel is independent of the risk of exposure to 2019n-CoV and infection status.
    - However, the international traveller might be wealthier people and with lower risk of exposure to 2019n-CoV
