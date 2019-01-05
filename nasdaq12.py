import financials as f
from matplotlib import pyplot as plt
from statistics import mean
import numpy as np


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.incomestatement = f.IncomeStatement(ticker)
        self.balancesheet = f.BalanceSheet(ticker)
        self.analysis = f.Analysis(ticker)
        self.statistics = f.Statistics(ticker)
        self.score = 0

    def getscore(self):
        functions =  [self.revenueincreasing(), self.epsincreasing(),
                      self.roeincreasing(),
                      self.buyrecommendation(),
                      self.positiveearningsurprises(),
                      self.earningsforecastincreasing(), self.highearningsgrowth(),
                      self.lowpegratio(), self.lowindustryearnings(),
                      self.shortdaystocover(),
                      self.positiveinsidertrading(),
                      self.positiveweightedalpha()]


        for function in functions:
            if function:
                self.score += 1


        return self.score

    def visualizerevenue(self):
        plt.scatter([1,2,3,4],self.incomestatement.items['Gross Income'])
        plt.show()


    def best_fit_slope(self, ys):
        ys = np.array(ys, dtype=np.float64)
        xs = np.array([1, 2, 3, 4], dtype=np.float64)
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
             ((mean(xs) * mean(xs)) - mean(xs * xs)))

        return m

    def revenueincreasing(self):
        m = self.best_fit_slope(self.incomestatement.items['Gross Income'])
        if m > 0:
            return True

        return False


    def epsincreasing(self):
        if self.best_fit_slope(self.analysis.items['Earnings Per Share']) > 0:
            return True

        return False

    def returnonequity(self):
        roe = []
        netincome = self.incomestatement.items['Gross Income']
        stockholderequity = self.balancesheet.items['Stockholder Equity']

        for x in range(len(netincome)):
            r = netincome[x]/stockholderequity[x]
            r = round(r, 2)
            roe.append(r)

        return roe

    def roeincreasing(self):
        if self.best_fit_slope(self.returnonequity()) > 0:
            return True

        return False

    def buyrecommendation(self):
        if self.analysis.items['Analyst Recommendation'] == "Buy" or \
        self.analysis.items['Analyst Recommendation'] == "Overweight":
            return True

        return False

    def positiveearningsurprises(self):
        try:
            for items in self.analysis.items['Earnings Surprises']:
                if items < 0:
                    return False

            return True

        except:
            return False

    def earningsforecastincreasing(self):
        if self.best_fit_slope(self.analysis.items['Earnings Forecast']) > 0:
            return True

        return False

    def highearningsgrowth(self):
        if self.analysis.items['Earnings Growth'] >= 8:
            return True

        return False

    def lowpegratio(self):
        if self.statistics.items['PEG Ratio'] != '-':
            if self.statistics.items['PEG Ratio'] < 1:
                return True

            return False

        return False

    def lowindustryearnings(self):
        if self.statistics.items['PE Ratio'] == "-" or \
        self.statistics.items['Industry Average'] == "-":
            return False

        if self.statistics.items['PE Ratio'] >= self.statistics.items['Industry Average']:
            return True

        return False


    def shortdaystocover(self):
        if self.statistics.items['Short Interest Ratio'] <= 2:
            return True

        return False

    def positiveinsidertrading(self):
        if self.statistics.items['Insider Trading'] > 0:
            return True

        return False

    def positiveweightedalpha(self):
        if self.statistics.items['Weighted Alpha'] > 0:
            return True

        return False

    def getsummary(self):
        print("Ticker: " + self.ticker + "\n")

        if self.revenueincreasing():
            print("1. Increasing Revenue: Pass\n")
            self.score += 1

        else:
            print("1. Increasing Revenue: Fail\n")

        if self.epsincreasing():
            print("2. Earnings Per Share Increasing: Pass\n")
            self.score +=1

        else:
            print("2. Earnings Per Share Increasing: Fail\n")

        if self.roeincreasing():
            print("3. Increasing Returns on Equity: Pass\n")
            self.score +=1

        else:
            print("3. Increasing Returns on Equity: Fail\n")

        if self.buyrecommendation():
            print("4. Analyst Recommends Buying: Pass\n")
            self.score += 1

        else:
            print("4. Analyst Recommends Buying: Fail\n")

        if self.positiveearningsurprises():
            print("5. Positive Earnings Surprises: Pass\n")
            self.score += 1

        else:
            print("5. Positive Earnings Surprises: Fail\n")

        if self.earningsforecastincreasing():
            print("6. Increasing Earnings Forecast: Pass\n")
            self.score +=1

        else:
            print("6. Increasing Earnings Forecast: Fail\n")

        if self.highearningsgrowth():
            print("7. High Earnings Growth: Pass\n")
            self.score +=1

        else:
            print("7. High Earnings Growth: Fail\n")

        if self.lowpegratio():
            print("8. Low PEG Ratio: Pass\n")
            self.score +=1

        else:
            print("8. Low PEG Ratio: Fail\n")

        if self.lowindustryearnings():
            print("9. Price-Earnings Ratio > Industry Average: Pass\n")
            self.score +=1
        else:
            print("9. Price-Earnings Ratio > Industry Average: Fail\n")

        if self.shortdaystocover():
            print("10. Days To Cover < 2: Pass\n")
            self.score +=1

        else:
            print("10. Days To Cover < 2: Fail\n")

        if self.positiveinsidertrading():
            print("11. Positive Net Activity (Previous 6 Months): Pass\n")
            self.score +=1

        else:
            print("11. Positive Net Activity (Previous 6 Months): Fail\n")

        if self.positiveweightedalpha():
            print("12. Positive Weighted Alpha: Pass\n")
            self.score +=1
        else:
            print("12. Positive Weighted Alpha: Fail\n")

        print(f"OVERALL SCORE: {str(self.score)}/12")


def sample_run():
    ticker = input("Enter Stock Symbol: ")
    s = Stock(ticker)
    s.getsummary()
    s.visualizerevenue()


sample_run()