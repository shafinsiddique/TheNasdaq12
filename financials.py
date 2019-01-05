from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Financials:
    """This class is used to represent all Financial Data.
    Subclasses include BalanceSheet, Income Statement, Analysis
    and Statistics.

    This class is an abstract class and should not be instantiated directly.

    ===Attributes==
    soup: represents a beautifulsoup object of the given html link."""

    soup: BeautifulSoup

    def __init__(self, ticker, link) -> None:
        """Initializer for the Financials class."""
        self.ticker = ticker

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        driver.get(link)

        html = driver.page_source

        driver.quit()

        self.soup = BeautifulSoup(html, features='lxml')

    def gethtml(self, link: str) -> BeautifulSoup:
        """This function is used to create and return any additional
        soup objects that we might need. """
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        driver.get(link)

        html = driver.page_source

        driver.quit()

        soup = BeautifulSoup(html, features='lxml')

        return soup


class IncomeStatement(Financials):
    """This class is a subclass of the Financials class and represents the income
    statement of the company.

    ===Attributes==

    soup: A BeautifulSoup object of the given link.
    allitems: represents all items found in the income statement link.
    totals: all the totals in the income statement link.
    items: A dictionary mapping the elements of the income statement to their values."""


    soup: BeautifulSoup
    _allitems: BeautifulSoup
    _totals: BeautifulSoup
    items: dict
    def __init__(self, ticker: str) -> None:
        """Initializer for the IncomeStatement class."""

        link = "https://ca.finance.yahoo.com/quote/" + ticker + "/financials?p=" + ticker

        Financials.__init__(self, ticker, link)

        self._allitems = self.soup.find_all("tr",
                {"class": "Bdbw(1px) Bdbc($c-fuji-grey-c) Bdbs(s) H(36px)"})

        self._totals = self.soup.find_all("tr", {"class": "Bdbw(0px)! H(36px)"})

        self.items = {"Gross Income": self.grossIncome()
                      }

    def grossIncome(self) -> list:
        """Returns a list of the gross incomes of the company over the last 4 years."""
        values= []
        t = self._totals[0].find_all("td",{"class":"Fw(b) Fz(s) Ta(end) Pb(20px)"})

        for links in t:
            se = float(str(links.text).replace(",",""))
            values.insert(0, se)

        return values


class BalanceSheet(Financials):
    """This class is a subclass of the Financials class and represents the Balance
    Sheet of the company.

    ===Attributes ==
    soup: A BeautifulSoup object of the given link.
    allitems: represents all items found in the income statement link.
    totals: all the totals in the income statement link.
    items: a dictionary mapping the elements of the balance sheet to their values,
    """

    soup: BeautifulSoup
    _allitems: BeautifulSoup
    _totals: BeautifulSoup
    items: dict

    def __init__(self, ticker):
        link = "https://ca.finance.yahoo.com/quote/" + ticker + "/balance-sheet?p="\
               +ticker

        Financials.__init__(self, ticker, link)

        self._allitems = self.soup.find_all("tr",
                                       {"class": "Bdbw(1px) Bdbc($c-fuji-grey-c) Bdbs(s) H(36px)"})

        self._totals = self.soup.find_all("tr", {"class": "Bdbw(0px)! H(36px)"})

        self.items = {"Stockholder Equity": self.stockholderequity()}

    def stockholderequity(self):
        """Returns a list of the shareholder equities over the last 4 years.
        """
        values = []
        t = self._allitems[-1].find_all("td",{"class":"Fz(s) Ta(end) Pstart(10px)"})

        for links in t:
            se = float(str(links.text).replace(",",""))
            values.insert(0, se)

        return values


class Analysis(Financials):
    """This class is a subclass of the Financials class and represents the
    Analysis ratios of the company.

        ===Attributes ==
        summary: represents all items found in the income statement link.
        items: a dictionary mapping """

    summary: BeautifulSoup
    items: dict

    def __init__(self, ticker: str):

        link = "https://ca.finance.yahoo.com/quote/"+ticker+"/analysis?p="\
                                                                     +ticker
        Financials.__init__(self, ticker, link)
        self.summary = self.soup.find_all("tr", {"class" : "BdT Bdc($c-fuji-grey-c)"})

        self.items = {"Earnings Per Share": self.earningspershare(),
                      "Analyst Recommendation": self.analystrecommendation(),
                      "Earnings Surprises": self.earningsurprises(),
                      "Earnings Forecast": self.earningsforecast(),
                      "Earnings Growth": self.earningsgrowth()}

    def earningspershare(self):
        """Return the eps values over the last 4 years.
        """
        id = 207
        eps = []
        for x in range(4):

            e = float(str(self.summary[12].find("span",{"data-reactid":str(id)}).text))
            eps.append(e)

            id += 2

        return eps

    def analystrecommendation(self):
        """Return the current analyst recommendation for the given stock.

        """
        marketwatchlink = "https://www.marketwatch.com/investing/stock/"+self.ticker+"/analystestimates"

        soup = self.gethtml(marketwatchlink)

        ar = str(soup.find("td",{"class" :"recommendation"}).text).replace(" ","").\
            replace("\n","")

        return ar

    def earningsurprises(self):
        """Return earnings surprise of the stock."""
        id = 229
        es = []

        try:
            for x in range(4):
                e = float(str(self.summary[14].find("span", {"data-reactid":str(id)}).text).replace
                          ("%",""))
                es.append(e)

                id += 2

            return es

        except:
            return

    def earningsforecast(self):
        """Return the earnings forecast of the company."""
        id = 196
        ef = []

        for x in range(4):
            e = float(str(self.summary[11].find("span", {"data-reactid": str(id)}).text))
            ef.append(e)

            id += 2

        return ef

    def earningsgrowth(self):
        """Return the earnings growth of the company.
        """
        eg = float(str(self.summary[-2].find("td",
                                             {"class":"Ta(end) Py(10px)"}).text).replace("%",""))
        return eg


class Statistics(Financials):
    """This class is a subclass of the Financials class and represents
    all statistics data of a company.

    ===Attributes==
    items: a dictionary mapping names of the items to their values.
    """

    items: dict

    def __init__(self, ticker: str):
        """Initializer for the Statistics Class."""

        link = "http://quote.morningstar.ca/Quicktakes/Valuation/" \
               "stockvaluation.aspx?t=" + ticker + "&region=USA&culture=en-CA&ops=clear"

        Financials.__init__(self, ticker, link)

        self.currentvaluationtable = self.soup.find_all("table",{"id":"currentValuationTable"})
        self.ratios = self.currentvaluationtable[0].find_all("td",{"align" : "right"})
        self.items = {"PEG Ratio": self.pegratio(), "PE Ratio":
                      self.priceearnings(),
                      "Industry Average": self.industryaverage(),
                      "Short Interest Ratio":self.shortinterestratio(),
                      "Insider Trading":self.insidertrading(),
                      "Weighted Alpha":self.weightedalpha()}

    def pegratio(self):
        """Return the PEG ratio of the company."""
        peg = self.ratios[4].text

        if str(peg) == "-":
            return "-"

        return float(peg)

    def priceearnings(self):
        """Return the PE Ratio of the company."""
        pe = self.ratios[0].text

        if str(pe) == '—':
            return "-"

        return float(pe)

    def industryaverage(self):
        """Return the industry average of the company."""
        ia = self.ratios[1].text

        if str(ia) == "-":
            return "-"

        return float(ia)

    def shortinterestratio(self):
        """Return the short interest ratio of the company."""
        link = "https://ca.finance.yahoo.com/quote/"+ self.ticker+"/key-statistics?p="+self.ticker

        soup = self.gethtml(link)

        values = soup.find_all("td",{"class":"Fz(s) Fw(500) Ta(end)"})

        sir = float(values[45].text)

        return sir


    def insidertrading(self):
        """Return the net activity over the last 6 months of the company.
        """
        link = "https://ca.finance.yahoo.com/quote/"+self.ticker+"/insider-transactions?p="+self.ticker

        soup = self.gethtml(link)

        rows = soup.find_all("tr",{"class":"Ta(end) BdB Bdc($c-fuji-grey-c)"})

        values = rows[2].find_all("td",{"class": "Py(10px)"})

        netactivity = int(str(values[1].text).replace(",",""))

        return netactivity

    def weightedalpha(self):
        """Return the weighted alpha of the company."""
        link = "https://www.barchart.com/stocks/quotes/" + self.ticker

        soup = self.gethtml(link)

        rows = soup.find_all("div",{"class":"financial-data-row"})

        wa = float(str(rows[4].find("span",{"class":"right"}).text).replace(" ",""))

        return wa

