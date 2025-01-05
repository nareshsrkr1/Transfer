This query doesn't seems to be fulfilling, we have wpd table where we grouped and updated our overrides data here, but when this grouping gets new column, the overrides should also need to spill to granular level,

Example, 

A, B,C segments hash exist strategy new as Residual
A cmbs
B national bank
C usd
Exit_strategy new Residual

Now when I added city to this grouping, it splitter to 2 records

A cmbs
B national bank
C Usd
D union bank

A cmbs
B national bank
C Usd
D indian bank
And these 2 records should have Residual value carry forwarded

How can we implant logic for this
