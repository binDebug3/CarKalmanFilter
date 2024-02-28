# CarKalmanFilter
A program to filter noisy data from vehicle sensors by Dallin Stewart, Gwen Martin, Eliza Powell, and Ethan Crawford

Data from: https://www.kaggle.com/datasets/jefmenegazzo/pvs-passive-vehicular-sensors-datasets/data


- Upload a Notebook with comments describing what you discovered
- Not on perfect formatting, but exploring the data and  the consequences

When and how you will hold out data for model evaluation? Explain
  - (Tave totally independent data you have never seen before to evaluate model performance at the end.
  - If you do want to hold out the same data every time, consider fixing a random seed when you make the test-train split.

Print out a few dozen rows of the data.
- Is there anything you didn't expect to see?
- Do data cleaning and feature engineering

Plot a few individual time series
- Do a similar check
- Is there anything unbelievable you see?

Evaluate
- How much data is missing?
- Is the distribution of missing data likely different from the distribution of non-missing data?
- How might you do a meaningful imputation (if needed)?
- Are there variables that should be dropped?
- Implement some initial solutions.
- Is there any hint that the data you have collected is differently distributed from the actual application of interest?
- If so, is there a strategy, such as reweighing samples, that might help?

Histogram
- Use a histogram or KDE to visualize the distribution of key variables.
- Consider log-scaling or other scaling of the axes.
- How should you think about outliers?
- Is there a natural scaling for certain variables?

Relationships
- Use 2D and/or 3D plot scatter plots, histograms, or heat maps to look for important relationships between variables.
- Consider using significance tests, linear model fits, or correlation matrices to clarify relationships.

Action Items
- Does what you see change any of your ideas for what models might be appropriate?
- Among other things, if your models rely on specific assumptions, is there a way you can check if these assumptions actually hold by looking at the data?
- If you are using linear models, do the relevant plots look linear? Is there some other scaling where the model assumptions might more nearly hold?

Note:
Beware that a test set for time-series data is trickier to build than for independent data points.  If you have training data just before and just after the test data point, the correlation between them means the test depends a lot on the training data and hence is a bad test.  At least ensure your test set comes after your training data, and ideally in a separate data-collection session.
