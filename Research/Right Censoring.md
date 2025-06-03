# Right Censoring

Definition: Right censoring is the phenomenon of finite length of follow up. When we try to predict an event within a time window using a retrospective database, not all patients that stand the criterion of prediction at a given time have a follow up that covers the whole time window.

 

If the event does happen within a shorter time the longer follow up is not needed. If the event does not happen within the follow up we do not know if it could still happen within the time window but after end of folow up.

This phenomena is important for long prediction window or in databases of high turn around and short follow up.

Right censoring is expected to give higher weight to short range events as the long range events have a higher probability of being censored.

Right censoring can happen when patient is lost to follow up, when the experiment period ends or when patient dies (if the predicted event is not death).

The following paper discusses the IPCW method to compensate for this censoring: [https://www.sciencedirect.com/science/article/pii/S1532046416000496?via%3Dihub](https://www.sciencedirect.com/science/article/pii/S1532046416000496?via%3Dihub)

They assume that the loss to follow up distribution is independent from outcome.

For each included prediction that had enough follow up till event (case) or till end of prediction window (control) they give weight that represents all other predictions that were censored before an event or end of window happened.

We implemented their method for a model that predicts severe aortic stenosis within 5 years and also all cause death for same time window. We calculated weights on prediction file (using all test samples, including the ones that were censored), and used the weighted bootstrap to get the performance.

As expected AUC deteriorated by up to 2% when implementing this on the test only.

Implementation on training set is complicated if you also want to match for years.

 

