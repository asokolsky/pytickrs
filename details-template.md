# {{longName}} | {{symbol}}:{{fullExchangeName}}

## Overview

{% if marketState != 'REGULAR' %}

|Current Price|Change (Change%)|Post Market Price|Post Market Change (Change%)|
|-------------|----------------|-----------------|----------------------------|
|{{currentPrice}}|{{'%.2f' % regularMarketChange}} ({{'%.2f' % regularMarketChangePercent}}%)|{{'%.2f' % postMarketPrice}}|{{'%.2f' % postMarketChange}} ({{'%.2f' % postMarketChangePercent}}%)|

{% else %}

|Current Price|Change (Change%)|
|-------------|----------------|
|{{currentPrice}}|{{'%.2f' % regularMarketChange}} ({{'%.2f' % regularMarketChangePercent}}%)|

{% endif %}


| | | | | | | | |
|-|-|-|-|-|-|-|-|
|Prev Close|{{'%.2f' % previousClose}}|Day's Range|{{regularMarketDayRange}}|Market Cap|{{format_num(marketCap)}}|Earnings Date|{{format_date(earningsTimestamp)}}|
|Open|{{open}}|52 Week Range|{{fiftyTwoWeekRange}}|Beta|{{beta}}|Forward Dividend & Yield|{{'%.2f' % dividendRate}} ({{'%.2f' % dividendYield}}%)|
|Bid|{{bid}}|Volume|{{format_num(volume)}}|PE (ttm)|{{'%.2f' % trailingPE}}|Ex-Dividend Date|{{format_date(dividendDate)}}|
|Ask|{{ask}}|Avg Volume|{{format_num(averageVolume)}}|EPS (ttm)|{{'%.2f' % epsTrailingTwelveMonths}}|Target Price (mean)|{{'%.2f' % targetMeanPrice}}|

## Business Summary

{{longBusinessSummary}}

{% if companyOfficers %}
## Corporate Officers
|Title|Name|Pay|Born|
|-----|----|---|----|
{% for officer in companyOfficers -%}
|{{ officer['title'] }}|{{ officer['name'] }}|{{ format_num(officer['totalPay']) }}|{{ officer['yearBorn'] }}|
{% endfor %}
{% endif %}

{% if corporateActions != [] %}
## Corporate Actions
{% for action in corporateActions -%}
### {{action['header']}}
{{action['message']}}
{% endfor %}
{% endif %}
