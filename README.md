# Flexible Price Tracker


### Video Demo: TODO


### Description:

E-commerce websites have different HTML structures that make scrapping prices a case by case task. Some websites might have a specific id attribute for the product's price, but others makes finding the price difficult by using identifiers that are not exclusive to the element that contains the price, like classes, or no usable identifiers at all.

 This price scrapper can be used with most of e-commerce websites by requiring the user to provide a [X-Path](https://www.w3schools.com/xml/xpath_intro.asp) of the element that contains the price. X-Path is similar to a path to a folder or file inside a file directory. As long as the path to a element does not change, the element containing the price can be retrieved.

 This scrapper can be run only once or run every X hours, minutes or days, using the --time argument. As an alternative, it is also possible to use OS specific schedulers like [Cron](https://en.wikipedia.org/wiki/Cron) if using Linux or MacOS, [Task Scheduler](https://en.wikipedia.org/wiki/Windows_Task_Scheduler) if using Windows.


### Notifications

The scrapper will send a notification to the user's desktop if the price of the product is lower than the target price set by the user.


### Price formats in various countries

Different countries uses different currency formats, commas and dots will have different roles. For example:

| Currency Name        | Currency Code | Format(s)        | Output       |
|----------------------|---------------|------------------|--------------|
| United States Dollar | USD           | $ ###,###,###.## | $123,000.50  |
| Brazilian Real       | BRL           | R$ ###.###.###,## | R$123.000,50 |
| Japanese Yen         | JPY           | ¥ ###,###,###    | ¥ 123,000,050    |

In order to correctly format the price used in different countries, the scraper needs a location setting. It is required to provide the locale in the arguments in order to run the scrapper. See [Usage](#usage) and [list of available locales](#list-of-locales) for more details.


### Installation

Install all required modules by:

```
pip install -r requirements.txt
```

#### Problems during installation

It is possible to encounter a problem related to pkg-config during installation of dbus-python on pip:

````
configure: error: The pkg-config script could not be found or is too old.  Make sure it
      is in your PATH or set the PKG_CONFIG environment variable to the full
      path to pkg-config.
      
      Alternatively, you may set the environment variables DBUS_CFLAGS
      and DBUS_LIBS to avoid the need to call pkg-config.
      See the pkg-config man page for more details.
````

To solve this problem, it is necessary to install system packages using apt on Linux or brew on MacOS:

On Linux:

```
apt install pkg-config build-essential libpython3-dev libdbus-1-dev
```

On MacOS:

```
brew install pkg-config dbus glib
````

then install dbus-python again using pip to install it successfuly:

```
pip install dbus-python
```


### Usage

```
python3 project.py <url> <xpath> <target_price> <locale>
```


| Required argument | Description                                             |
|-------------------|---------------------------------------------------------|
| url               | URL to be scrapped                                      |
| xpath             | X-Path of the element that contains the product's price |
| target_price      | Target price to activate a notification                 |
| locale            | Locale setting in order to correctly convert price      |

| Optional argument   | Description                                      |
|---------------------|--------------------------------------------------|
| -h, --help          | Show help message and exit                       |
| -t, --time          | Run between X time itervals                      |
| --all-notifications | Notify even if price is higher than target price |

### **Important**

It is common for urls and XPaths to have characters such as / (forward slash) or " (double quotes) that needs to be escaped to avoid unwanted behavior at the terminal shell. **Always use single quotes (') around the url and the XPath for the program to work correctly.**

### Using scheduling

Use the -t or --time argument to run between available intervals. 
Available intervals are:

| Option | Description         |
|--------|---------------------|
| m      | Run every X minutes |
| h      | Run every X hours   |
| d      | Run every X days    |

For example:

````
python3 project.py 'www.shop.com' '//*[@id="price"]' 49 en_US.UTF-8 --time m10
````
It will run the scrapper once every 10 minutes

````
python3 project.py 'www.shop.com' '//*[@id="price"]' 49 en_US.UTF-8 --time h2
````
It will run the scrapper once every 2 hours

````
python3 project.py 'www.shop.com' '//*[@id="price"]' 49 en_US.UTF-8 --time d1
````

It will run the scrapper once every day

**Important**: Notifications will appear only when the actual price of product is equal or below the targetprice. They also will not appear if user's computer is set on "Do not disturb" mode. Please deactivate this mode if desktop notifications are desired.


### How to get the price element's X-Path

The X-Path can be obtained by using the browser's developer's tools. Specifics will vary form browser to browser, but the process is usually similar.

#### In Chrome:

1. Right click "Inspect" on the item you want to find the xpath
1. Right click on the highlighted element in Devtools
1. Select Copy > Copy XPath

#### In Firefox:

1. Right click "Inspect" on the item you want to find the xpath
1. Right click on the highlighted element in Devtools
1. Select Copy > XPath


### File contents

#### project.py

Contains the following functions:

**main**: Calls the other functions for a single scrapping task

**extract_time**: Used for the scheduling feature, validates schedule input

**scrap_page**: Given an url, XPath and driver, returns the target element's contents

**convert_string_to_float**: Given a price like string, considers locale for correctly converting to float

**create_message**: Given a price and a target price, generates appropriate message for user

#### test_project.py

Contains tests for each of the functions contained in project.py.

#### requirements.txt

Contains all dependencies for the project.

### List of locales

Use the list below to get the appropriate locale for your currency format:

| Locale             | Description                              |
|--------------------|------------------------------------------|
| af_ZA.UTF-8        | Afrikaans, South Africa                  |
| ar_AE.UTF-8        | Arabic, United Arab Emirates             |
| ar_BH.UTF-8        | Arabic, Bahrain                          |
| ar_DZ.UTF-8        | Arabic, Algeria                          |
| ar_EG.UTF-8        | Arabic, Egypt                            |
| ar_IQ.UTF-8        | Arabic, Iraq                             |
| ar_JO.UTF-8        | Arabic, Jordan                           |
| ar_KW.UTF-8        | Arabic, Kuwait                           |
| ar_LY.UTF-8        | Arabic, Libya                            |
| ar_MA.UTF-8        | Arabic, Morocco                          |
| ar_OM.UTF-8        | Arabic, Oman                             |
| ar_QA.UTF-8        | Arabic, Qatar                            |
| ar_SA.UTF-8        | Arabic, Saudi Arabia                     |
| ar_TN.UTF-8        | Arabic, Tunisia                          |
| ar_YE.UTF-8        | Arabic, Yemen                            |
| as_IN.UTF-8        | Assamese, India                          |
| az_AZ.UTF-8        | Azerbaijani, Azerbaijan                  |
| be_BY.UTF-8        | Belarusian, Belarus                      |
| bg_BG.UTF-8        | Bulgarian, Bulgaria                      |
| bn_IN.UTF-8        | Bengali, India                           |
| bs_BA.UTF-8        | Bosnian, Bosnia and Herzegovina          |
| ca_ES.UTF-8        | Catalan, Spain                           |
| cs_CZ.UTF-8        | Czech, Czech Republic                    |
| da_DK.UTF-8        | Danish, Denmark                          |
| de_AT.UTF-8        | German, Austria                          |
| de_BE.UTF-8        | German, Belgium                          |
| de_CH.UTF-8        | German, Switzerland                      |
| de_DE.UTF-8        | German, Germany                          |
| de_LI.UTF-8        | German, Liechtenstein                    |
| de_LU.UTF-8        | German, Luxembourg                       |
| el_CY.UTF-8        | Greek, Cyprus                            |
| el_GR.UTF-8        | Greek, Greece                            |
| en_AU.UTF-8        | English, Australia                       |
| en_BW.UTF-8        | English, Botswana                        |
| en_CA.UTF-8        | English, Canada                          |
| en_GB.UTF-8        | English, United Kingdom                  |
| en_HK.UTF-8        | English, Hong Kong SAR China             |
| en_IE.UTF-8        | English, Ireland                         |
| en_IN.UTF-8        | English, India                           |
| en_MT.UTF-8        | English, Malta                           |
| en_NZ.UTF-8        | English, New Zealand                     |
| en_PH.UTF-8        | English, Philippines                     |
| en_SG.UTF-8        | English, Singapore                       |
| en_US.UTF-8        | English, U.S.A.                          |
| en_ZW.UTF-8        | English, Zimbabwe                        |
| es_AR.UTF-8        | Spanish, Argentina                       |
| es_BO.UTF-8        | Spanish, Bolivia                         |
| es_CL.UTF-8        | Spanish, Chile                           |
| es_CO.UTF-8        | Spanish, Colombia                        |
| es_CR.UTF-8        | Spanish, Costa Rica                      |
| es_DO.UTF-8        | Spanish, Dominican Republic              |
| es_EC.UTF-8        | Spanish, Ecuador                         |
| es_ES.UTF-8        | Spanish, Spain                           |
| es_GT.UTF-8        | Spanish, Guatemala                       |
| es_HN.UTF-8        | Spanish, Honduras                        |
| es_MX.UTF-8        | Spanish, Mexico                          |
| es_NI.UTF-8        | Spanish, Nicaragua                       |
| es_PA.UTF-8        | Spanish, Panama                          |
| es_PE.UTF-8        | Spanish, Peru                            |
| es_PR.UTF-8        | Spanish, Puerto Rico                     |
| es_PY.UTF-8        | Spanish, Paraguay                        |
| es_SV.UTF-8        | Spanish, El Salvador                     |
| es_US.UTF-8        | Spanish, U.S.A.                          |
| es_UY.UTF-8        | Spanish, Uruguay                         |
| es_VE.UTF-8        | Spanish, Venezuela                       |
| et_EE.UTF-8        | Estonian, Estonia                        |
| fi_FI.UTF-8        | Finnish, Finland                         |
| fr_BE.UTF-8        | French, Belgium                          |
| fr_CA.UTF-8        | French, Canada                           |
| fr_CH.UTF-8        | French, Switzerland                      |
| fr_FR.UTF-8        | French, France                           |
| fr_LU.UTF-8        | French, Luxembourg                       |
| gu_IN.UTF-8        | Gujarati, India                          |
| he_IL.UTF-8        | Hebrew, Israel                           |
| hi_IN.UTF-8        | Hindi, India                             |
| hr_HR.UTF-8        | Croatian, Croatia                        |
| hu_HU.UTF-8        | Hungarian, Hungary                       |
| hy_AM.UTF-8        | Armenian, Armenia                        |
| id_ID.UTF-8        | Indonesian, Indonesia                    |
| is_IS.UTF-8        | Icelandic, Iceland                       |
| it_CH.UTF-8        | Italian, Switzerland                     |
| it_IT.UTF-8        | Italian, Italy                           |
| ja_JP.UTF-8        | Japanese, Japan                          |
| ka_GE.UTF-8        | Georgian, Georgia                        |
| kk_KZ.UTF-8        | Kazakh, Kazakhstan                       |
| kn_IN.UTF-8        | Kannada, India                           |
| ko_KR.UTF-8        | Korean, Korea                            |
| ks_IN.UTF-8        | Kashmiri, India                          |
| ku_TR.UTF-8        | Kurdish, Turkey                          |
| ku_TR.UTF-8@sorani | Kurdish (Sorani), Turkey                 |
| ky_KG.UTF-8        | Kirghiz, Kyrgyzstan                      |
| lt_LT.UTF-8        | Lithuanian, Lithuania                    |
| lv_LV.UTF-8        | Latvian, Latvia                          |
| mk_MK.UTF-8        | Macedonian, Macedonia                    |
| ml_IN.UTF-8        | Malayalam, India                         |
| mr_IN.UTF-8        | Marathi, India                           |
| ms_MY.UTF-8        | Malay, Malaysia                          |
| mt_MT.UTF-8        | Maltese, Malta                           |
| nb_NO.UTF-8        | Bokmal, Norway                           |
| nl_BE.UTF-8        | Dutch, Belgium                           |
| nl_NL.UTF-8        | Dutch, Netherlands                       |
| nn_NO.UTF-8        | Nynorsk, Norway                          |
| or_IN.UTF-8        | Oriya, India                             |
| pa_IN.UTF-8        | Punjabi, India                           |
| pl_PL.UTF-8        | Polish, Poland                           |
| pt_BR.UTF-8        | Portuguese, Brazil                       |
| pt_PT.UTF-8        | Portuguese, Portugal                     |
| ro_RO.UTF-8        | Romanian, Romania                        |
| ru_RU.UTF-8        | Russian, Russia                          |
| ru_UA.UTF-8        | Russian, Ukraine                         |
| sa_IN.UTF-8        | Sanskrit, India                          |
| sk_SK.UTF-8        | Slovak, Slovakia                         |
| sl_SI.UTF-8        | Slovenian, Slovenia                      |
| sq_AL.UTF-8        | Albanian, Albania                        |
| sr_ME.UTF-8        | Serbian, Montenegro                      |
| sr_ME.UTF-8@latin  | Serbian, Montenegro (Latin)              |
| sr_RS.UTF-8        | Serbian, Serbia                          |
| sr_RS.UTF-8@latin  | Serbian, Serbia (Latin)                  |
| sv_SE.UTF-8        | Swedish, Sweden                          |
| ta_IN.UTF-8        | Tamil, India                             |
| te_IN.UTF-8        | Telugu, India                            |
| th_TH.UTF-8        | Thai, Thailand                           |
| tr_TR.UTF-8        | Turkish, Turkey                          |
| uk_UA.UTF-8        | Ukrainian, Ukraine                       |
| vi_VN.UTF-8        | Vietnamese, Vietnam                      |
| zh_CN.UTF-8        | Simplified Chinese, China                |
| zh_HK.UTF-8        | Traditional Chinese, Hong Kong SAR China |
| zh_SG.UTF-8        | Chinese, Singapore                       |
| zh_TW.UTF-8        | Traditional Chinese, Taiwan              |

Table from https://docs.oracle.com/cd/E23824_01/html/E26033/glset.html#glscx