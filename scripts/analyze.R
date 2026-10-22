# Run from the project root: Rscript scripts/analyze.R
# No external R packages required for the core analysis.
d <- read.csv('data/fictional_bank_nps.csv', stringsAsFactors=FALSE)
stopifnot(all(d$recommendation_score %in% 0:10))
score <- d$recommendation_score
nps <- function(x) 100 * (mean(x >= 9) - mean(x <= 6))
cat('Respondents:', nrow(d), '\nNPS:', round(nps(score), 1), '\n')
cat('Promoters:', mean(score >= 9), 'Passives:', mean(score %in% 7:8), 'Detractors:', mean(score <= 6), '\n')
# The original 0-10 recommendation score is the respondent-level outcome.
# Topic indicators are derived from the same open-ended question for everyone.
fit <- lm(recommendation_score ~ topic_fees + topic_reliability +
  topic_navigation + topic_speed + topic_features + topic_trust +
  topic_clarity + segment + tenure_years, data=d)
print(summary(fit))
# HC3 robust SEs are used by the Python precomputed website results.
# Optional R verification when sandwich is installed:
if (requireNamespace('sandwich', quietly=TRUE)) {
  se <- sqrt(diag(sandwich::vcovHC(fit, type='HC3')))
  tab <- data.frame(term=names(coef(fit)), estimate=coef(fit),
                    low=coef(fit)-1.96*se, high=coef(fit)+1.96*se)
  print(tab)
}
# Sampling variance for NPS, treating promoter/passive/detractor as +1/0/-1.
nps_variance <- function(p_promoter,p_detractor) {
  p_promoter + p_detractor - (p_promoter-p_detractor)^2
}
required_n <- function(variance,margin=10,z=1.96) {
  ceiling(z^2 * 10000 * variance / margin^2)
}
cat('n for +/-10, population A:',required_n(nps_variance(.30,0)),'\n')
cat('n for +/-10, population B:',required_n(nps_variance(.65,.35)),'\n')
# Replicate a simple simulation in R for practice.
set.seed(20261016)
simulate_nps <- function(n,p_promoter,p_passive,reps=20) {
  replicate(reps, {
    response <- sample(c(1,0,-1),size=n,replace=TRUE,
                       prob=c(p_promoter,p_passive,1-p_promoter-p_passive))
    100*mean(response)
  })
}
print(simulate_nps(100,.65,0))

# Lesson 4, Part B: independently sampled monthly NPS results.
# This illustrates uncertainty around a difference between waves (not an individual NPS).
# Both hypothetical waves have no passives; these proportions are NOT real observations.
compare_waves <- function(n_sept, n_oct, z=1.96) {
  sept_p <- .65; sept_d <- .35  # NPS +30
  oct_p <- .68; oct_d <- .32    # NPS +36
  change <- 100 * ((oct_p - oct_d) - (sept_p - sept_d))
  se_change <- 100 * sqrt(nps_variance(sept_p, sept_d)/n_sept +
                          nps_variance(oct_p, oct_d)/n_oct)
  c(estimate=change, lower=change-z*se_change,
    upper=change+z*se_change)
}
cat('Approximate 95% CI for +30 to +36, 300 each:',
    paste(round(compare_waves(300,300),1),collapse=', '), '\n')
cat('Approximate 95% CI for +30 to +36, 3000 each:',
    paste(round(compare_waves(3000,3000),1),collapse=', '), '\n')
