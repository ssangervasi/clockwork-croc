## My experience using [Disco]

Overall Disco has helped me a lot. I like that:

* The API defintions are organized.
* It handles websockets way better than anything I could have written
  from scratch.
* It has a usable tutorial, which most zero-point-x version projects don't.

Still, there I several things I should submit as github issues.

### Required monkey patch
The gateway code blocks and times out if you try and use it by importing it,
even when configured correctly.

After banging my head against the wall for a while, it turned out that
this is because the gateway relies on `gevenet.monkey.patch_all()`.

The `cli` module calls this method, which means Disco works if you
use the tutuorial examples. However, this is a sharp corner you're trying
to use Disco as "a generic-use library" as the documentation advertises.

The `gateway.client` module (and perhaps others) should apply the gevent
monkey patch if it's required for it to function. Alternatively, it could
detect whether the patch has happened and fail sooner rather than later
with an instructional message.


### Missing methods

One of the first API methods I needed to use was `users_me_guilds_list` in order
to find out which guilds my bot could interact with. This method doesn't exist,
so I forked and added it.

This is something I could totally contribute, if I were going to stop being
a lazy user 😴.

### Naming things is hard

There are `api.client` methods with names like `guilds_channels_list` which
use the word "list" but return a custom HashMap class where the keys are Ids.

This doesn't match the discord API specificiation, and it is one of the
first places I had to poke into Disco's source instead of trusting it to
match the spec.

This also applies an extra layer of looping to create the hash, which might not
have a big performance impact but is worth making optional.

### Python 3.7

Current stable version v0.0.12 doesn't work with Python 3.7
due to gevent dependency not working with `async def`

Forking from v0.0.13-rc.2 and pinning to that has been successful.

Since encountering this problem in Disco, I have had other Python 3.7 projects
run into this asyncio issue, so so this is more a frustration with
the Python release rather than with Disco.

[disco]: https://github.com/b1naryth1ef/disco