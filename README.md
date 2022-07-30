# pyStudy
A Discord bot used to help students in their schoolworks using [Wikipedia](https://en.wikipedia.org/api/rest_v1) and [Wolfram|Alpha's REST API.](https://products.wolframalpha.com/api/pricing/)

## Available Commands
`?wikiFromQuery` - searches Wikipedia's API with the given query

`?wikiFromID` - searches Wikipedia's API using the page ID.

`?wikiDLPDF` - returns a link where you can download the Wikipedia's content in PDf's format.

`?whatIs` - uses the Wolfram|Alpha's API to answer your question.


## Invite Link
Invite the bot to your own server [using this link.](https://discord.com/api/oauth2/authorize?client_id=1002716114922516551&permissions=256064&scope=bot)


### NOTE:
- The `?whatIs` command can only be called 2000 times / month. When it reached it's limit, the bot will automatically switch to demo API.[^0]
- The bot will be offline every last week of the month.[^1]



[^0]: https://products.wolframalpha.com/api/faqs.html
[^1]: https://devcenter.heroku.com/changelog-items/907
