from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()),
)

URL = "https://www.fundsexplorer.com.br/ranking"


def main():
    driver.get(URL)

    sleep(5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    try:
        table = soup.find_all(
            attrs={"data-element": "table-ranking-container"},
        )[0]
        titles = [th.string for th in table.thead.find_all("th")]
        fiis = [
            [td.get("data-value") for td in row.find_all("td")]
            for row in table.tbody.find_all("tr")
        ]

        df = pd.DataFrame(data=fiis, columns=titles)
        df.set_index("Fundos", inplace=True)
        df.drop(
            columns=[
                "Dividend Yield",
                "DY (3M) Acumulado",
                "DY (6M) Acumulado",
                "DY (3M) média",
                "DY (6M) média",
                "DY (12M) média",
                "DY Ano",
                "Variação Preço",
                "Rentab. Período",
                "Rentab. Acumulada",
                "VPA",
                "P/VPA",
                "DY Patrimonial",
                "Variação Patrimonial",
                "Rentab. Patr. Período",
                "Rentab. Patr. Acumulada",
                "Vacância Financeira",
            ],
            inplace=True,
        )

        breakpoint()
    except Exception:
        pass


if __name__ == "__main__":
    main()
