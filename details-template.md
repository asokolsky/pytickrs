# {{longName}} | {{symbol}}:{{fullExchangeName}}

## Overview

|Current|Post Market|
|-------|-----------|
|{{currentPrice}} {{'%.2f' % regularMarketChange}} ({{'%.2f' % regularMarketChangePercent}}%)|{{postMarketPrice}} {{'%.2f' % postMarketChange}} ({{'%.2f' % postMarketChangePercent}}%)|


|Title|Name|
|-----|----|
|Prev Close|{{'%.2f' % previousClose}}
|Day's Range|{{regularMarketDayRange}}|
|52 Week Range|{{fiftyTwoWeekRange}}|
|Volume|{{volume}}|
|Avg Volume|{{averageVolume}}|

## Business Summary

{{longBusinessSummary}}

## Corporate Officers

|Title|Name|Pay|Born|
|-----|----|---|----|
{% for officer in companyOfficers -%}
|{{ officer['title'] }}|{{ officer['name'] }}|{{ officer['totalPay'] }}|{{ officer['yearBorn'] }}|
{% endfor %}

{% if corporateActions %}
## Corporate Actions
{% for action in corporateActions -%}
### {{action['header']}}
{{action['message']}}
{% endfor %}
{% endif %}
