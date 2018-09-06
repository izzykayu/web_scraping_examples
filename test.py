from bs4 import BeautifulSoup
import urllib
import urllib.request
import pandas as pd
import pprint

lnk = "https://jobs.mo.gov/content/missouri-warn-notices-py-2017"


def to_string(s):
    """
    makes a string
    input example: 10000
    output example: '1000'

    """
    try:
        return str(s)
    except:
        # Change the encoding type if needed
        return s.encode('utf-8')


def clean_up_cols(s):
    """

    :param s: string for example # AFFECTED
    :return: space removed for example #_affected
    """
    s = to_string(s)
    s = s.lower()
    s = s.replace(' ', '_')
    return s


def web_scraper_table(link):
    """

    :param link: this will be the link where you want to scrape table
    :return: json that returns metadata or table data with header keys
    # """
    # table = BeaputifulSoup.find("table", {"class": "lineItemsTable"})
    # for row in table.findAll("tr"):
    #     cells = row.findAll("td")
    #     print(cells)
    keys_ls = []
    with urllib.request.urlopen(link) as response:
        the_page = response.read()
        bs = BeautifulSoup(the_page,features="lxml")
        #print(bs.fi)
        table = bs.find(lambda tag: tag.name == 'table') #$ and tag.has_attr('id') and tag['id'] == "Table1")
        rows = table.findAll(lambda tag: tag.name == 'tr')
        keys=rows[0]
        split_keys=keys.text.split('\n')
        for key in split_keys:
            if key != '':
                keys_ls.append(clean_up_cols(key))
        data=[]
        for row in rows:
            values = row.find_all('td')
            data.append([to_string(ele.text.strip()) for ele in values])

    df=pd.DataFrame(data)
    df=df.dropna(axis=0, how="all")
    df.columns= keys_ls
    print(df.head(2))
    print(df.tail(2))
    print(df.info())
    df.to_json(path_or_buf='json_table_test.json')
    pprint.pprint(df.to_json())

web_scraper_table(lnk)


