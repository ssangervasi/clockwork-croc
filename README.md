# Croc

> Snap snap

## Experience using [Disco]

* Current stable version v0.0.12 doesn't work with Python 3.7
  due to gevent dependency not working with `async def`
  ... So I pinned to v0.0.13-rc.2

* The gateway code blocks and times out if you try and use it by importing it,
  even when configured correctly.
    - It turns out this is because it relies on `gevenet.monkey.patch_all()`
    - But the gateway.client module doesn't import this, only the CLI does.
    - And that's super annoying to figure out!

* Some api.client methods like `guilds_channels_list` literally use the word
  "list" but return a custom HashMap class where the keys are ids. This confusing
  and doesn't match the discord API spec.

* Straight up missing method `users_me_guilds_list` and maybe more. 
  (I should just submit a PR.)

[disco]: https://github.com/b1naryth1ef/disco