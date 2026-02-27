# Event Calendars

I'm interested in community events throughout the Greater Toronto & Hamilton Area.
Many organizations publish event information on their websites,
but not in form easily subscribed to.

This project periodically checks various websites and
exports an iCalendar (.ical) feed of upcoming events.

[Subscribe to them in your calendar app](https://jamesdoc.com/blog/2024/webcal/).

(This unifies several other projects from disparate git repositories.)

## Feeds
<!-- [[[cog
    from typing import NamedTuple
    from glob import glob
    from os import environ
    from pathlib import Path

    server_url = environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = environ.get("GITHUB_REPOSITORY", "ellieayla/event-calendars")
    ref = "refs/heads/main"  # published permalink not dependent on what branch/pr we're working on now

    files = sorted(glob("out/*.ical"))

    for filename in files:
        label = Path(filename).name
        url = f"{server_url}/{repo}/raw/{ref}/{filename}"
        cog.outl(f"* [{label}]({url})")
]]] -->
* [burlington-pools.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/burlington-pools.ical)
* [cycle-toronto.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/cycle-toronto.ical)
* [httpbin.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/httpbin.ical)
* [respect-cyclists-facebook.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/respect-cyclists-facebook.ical)
* [toronto-community-bikeways.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/toronto-community-bikeways.ical)
* [tour-de-cafe-newhope.fb.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/tour-de-cafe-newhope.fb.ical)
* [ymca-hamilton-burlington.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/ymca-hamilton-burlington.ical)
<!-- [[[end]]] -->

## Plans

Track in [open issues](../../issues).
