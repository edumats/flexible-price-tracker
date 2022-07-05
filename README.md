# Flexible Price Tracker

#### Video Demo: TODO

#### Description:

E-commerce websites have different Html structures that make scrapping prices a case by case task. Some websites might have a specific id atribute for prices, others purposefuly makes finding the price difficult, by using class attributes that change over time or refers to other prices that are present in the page (from related products, for example). This price scrapper can be used in most of e-commerce websites by requiring the user to provide a [X-Path](https://www.w3schools.com/xml/xpath_intro.asp) of the element that contains the price.

Different countries uses different currency formats, like . In order to correctly extract the price from shops that uses different formats, the scraper also needs a location setting. It must be provided if 



#### Instalation

Install all required modules by:

```
pip install -r requirements.txt
```

#### Usage

```
python3 project.py <url> <xpath> <target_price>
```


| Required argument | Description                                             |
|-------------------|---------------------------------------------------------|
| url               | URL to be scrapped                                      |
| xpath             | X-Path of the element that contains the product's price |
| target_price      | Target price to activate a notification                 |

| Optional argument | Description                         |
|-------------------|-------------------------------------|
| -h, --help        | show this help message and exit     |
| -l, --locale      | Set the locale for price formatting |

##### How to get the price element's X-Path

In Chrome:

1. Right click "inspect" on the item you are trying to find the xpath
1. Right click on the highlighted area on the console.
1. Select Copy xpath
