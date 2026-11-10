# Content guide: how to add walkthroughs, cheats and guides

All content lives in **one file**: `content.json` in your GitHub repo. Edit it, **raise `version` by 1**, and save. Everyone's app picks up the change the next time they open it or pull down to refresh. You don't need an App Store update.

Before saving, paste the file into jsonlint.com to check it. If the file has a mistake, the app keeps showing the last good version, so a typo won't crash it, but your update won't appear either.

**Rule #1: only publish what you've verified.** Being the most accurate app is worth more than being 10 minutes faster. Mark anything unconfirmed as a `rumor` in news, and leave `verified: false` on cheats until you've tested them.

---

## Story mission (shows in the Story tab)

```json
{
  "id": "story-001",
  "mode": "story",
  "chapter": "Chapter 1",
  "order": 1,
  "title": "Mission name",
  "giver": "Character who gives it",
  "summary": "One or two sentences on what happens.",
  "steps": [
    "Drive to the marked location.",
    "Follow the target **without being spotted**.",
    "Escape the area."
  ],
  "objectives": ["Bonus objective 1", "Bonus objective 2"],
  "tips": ["Useful tip"],
  "rewards": "What you earn or unlock"
}
```
- `order` controls the mission number and sort order. Missions are grouped under each `chapter` in the order they first appear.
- Story missions are spoiler-protected automatically. Add `"spoiler": false` to turn that off.
- Players can check off each step. **Never change a mission's `id` or reorder its steps after publishing**, or players lose their progress.

## Online job or heist (shows in the Online tab)

Same structure as a story mission, with `"mode": "online"` and `chapter` used for the type, for example `"Heists"`, `"Contact Missions"` or `"Business Sales"`.

## Cheat (shows in the Cheats tab)

```json
{
  "id": "cheat-weapons-1",
  "name": "Cheat name",
  "effect": "What it does",
  "category": "Weapons",
  "playstation": ["TRIANGLE", "R2", "LEFT", "L1", "CROSS"],
  "xbox": ["Y", "RT", "LEFT", "LB", "A"],
  "phone": "1-999-000-0000",
  "disablesAchievements": true,
  "notes": "Story mode only.",
  "verified": true
}
```
**Button names**
- PlayStation: `CROSS`, `CIRCLE`, `SQUARE`, `TRIANGLE`, `L1`, `L2`, `R1`, `R2`, `L3`, `R3`
- Xbox: `A`, `B`, `X`, `Y`, `LB`, `LT`, `RB`, `RT`, `LS`, `RS`
- Both platforms: `UP`, `DOWN`, `LEFT`, `RIGHT`
- `phone` is optional. Leave it out if the cheat has no phone code.
- Categories you use become filter chips automatically.

## Guide (money methods, vehicles, collectible routes, tips)

```json
{
  "id": "online-money-1",
  "section": "online",
  "category": "Money",
  "title": "Best solo money method",
  "subtitle": "One-line description",
  "icon": "dollarsign.circle.fill",
  "tags": ["Solo", "Beginner"],
  "spoiler": false,
  "body": "## Heading\nA paragraph.\n- **Bold** bullet\n- [A link](https://example.com)"
}
```
- `section`: `story` (Story tab), `online` (Online tab), or `general` (More tab).
- Guides are grouped by `category` within each tab.
- `icon` is any SF Symbol name. Use Apple's free SF Symbols app to browse them.

## Checklist (Tracker: collectibles, 100% completion)

```json
{
  "id": "collectibles-1",
  "title": "Hidden packages",
  "icon": "star.circle.fill",
  "items": [
    { "id": "pkg-01", "title": "Package 1", "detail": "On the roof behind the diner" }
  ]
}
```

## News

```json
{ "id": "n-123", "title": "Headline", "summary": "Two sentences.", "date": "2026-11-19",
  "status": "official", "sourceURL": "https://..." }
```
`status` is `official`, `rumor` or `community`.

---

## Launch-week content plan

| When | Publish |
|---|---|
| Day 1 (Nov 19) | First 5–10 story missions, a beginner tips guide, any confirmed cheats |
| Days 2–4 | Rest of Chapter 1–2 walkthroughs, first Online money guide, a collectibles checklist |
| Week 2 | Full story walkthrough, heist guides, best vehicles, 100% completion tracker |
| Ongoing | Online updates and events the week they drop |

Each time you publish, post a short clip on TikTok, Reddit or X saying "now in the app."
