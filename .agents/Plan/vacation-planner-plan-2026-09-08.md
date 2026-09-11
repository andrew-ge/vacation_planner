# Vacation Planner — Initial Plan

**Created:** 2026-09-08
**Status:** Discovery; product decisions pending

## Confirmed requirements

- Help plan a personal vacation.
- Support either booking flights and hotels or planning around travel that is already booked.
- Suggest attractions, locally recommended places to eat, and city walks.
- Create a tagged Google Map.
- Keep private flight and hotel information out of the repository.
- Store private travel details locally in the ignored `Transportation/` and `Hotel/` directories.

## Proposed delivery plan

1. Define the first release and its primary user journey.
2. Design a private local-input format for booked transportation and accommodation.
3. Build destination research for attractions, food, and walkable routes, including source attribution.
4. Turn selected places into a day-by-day itinerary with tags.
5. Export or maintain the tagged Google Map.
6. Add booking discovery only if it remains necessary after the itinerary workflow works.

## Grill-me: round 1 decisions

### Q1 — Primary job for v1

Should the first version optimize for planning a trip from scratch (including flight/hotel discovery), or for building a detailed itinerary around travel already booked?

**Recommendation:** Start with existing bookings and itinerary planning. Add flight and hotel booking support after the planning flow is useful.

### Q2 — How private trip details work

Flight and hotel details must stay out of Git. Should they be entered manually into a local/private configuration, or connected from a provider such as email/calendar later?

**Recommendation:** Use manual entry stored locally and ignored by Git; defer account connections.

### Q3 — Primary experience

What should this project become: a web app, a command-line/local tool, or a generated trip document/map workflow?

**Recommendation:** Build a small web app with an itinerary view and map.

### Q4 — Planning depth

Is the desired output a curated shortlist, or a day-by-day schedule with travel time, reservations, budgets, and alternatives?

**Recommendation:** Build toward a day-by-day itinerary, but make the first release a shortlist plus a practical daily outline.

## Privacy boundary

- Never commit contents of `Transportation/` or `Hotel/`.
- Keep any future example data fictional and clearly labelled as such.
- Do not place reservation codes, dates, confirmation emails, or addresses for private lodging in tracked files.
