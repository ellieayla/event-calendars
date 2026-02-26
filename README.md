# Event Calendars

I'm interested in community events throughout the Greater Toronto & Hamilton Area.
Many organizations publish event information on their websites,
but not in form easily subscribed to.

This project periodically checks various websites and
exports an iCalendar (.ical) feed of upcoming events.

[Subscribe to them in your calendar app](https://jamesdoc.com/blog/2024/webcal/).

(This unifies several other projects from disparate git repositories.)

## Feeds

* [ymca-hamilton-burlington.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/ymca-hamilton-burlington.ical)
* [burlington-pools.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/burlington-pools.ical)
* [cycle-toronto.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/cycle-toronto.ical)
* [toronto-community-bikeways.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/toronto-community-bikeways.ical)
* [httpbin.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/httpbin.ical)
* [respect-cyclists-facebook.ical](https://github.com/ellieayla/event-calendars/raw/refs/heads/main/out/respect-cyclists-facebook.ical)

## Plans

* Find a better solution for https://cycleto.ca/events - fronted by cloudflare, currently fetching from the wayback archive instead
* Add support for Tour De Cafe rides from https://www.newhopecommunitybikes.com/womens-programming
* Add support for https://www.burlingtongreen.org/events/ - note structured JSON feed contains /published/ time, not /event/ date.
