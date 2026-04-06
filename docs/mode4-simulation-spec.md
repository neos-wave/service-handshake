# Mode 4 Simulation — Design Specification
**Neos Wave · Dual CX Framework**
Version: 1.0 · 6 April 2026

---

## Overview

A 86-second animated simulation demonstrating a Mode 4 (Customer AI ↔ Brand AI) interaction using the Service Handshake framework. Lives at neoswave.com/mode4/

The simulation shows the complete journey from a human's initial message through to a fully resolved interaction — replacement approved, return organised, pickup booked — with no human involvement beyond the first message.

---

## Design Principles

1. **The human prompt completes the story.** The simulation opens with a human typing a message. This grounds the demo before the machines take over.

2. **The consumer AI builds the declaration through conversation.** It doesn't arrive pre-loaded with instructions. It asks the human what they want, what they won't accept, and requests photo evidence — building the Service Handshake declaration from those answers.

3. **The brand AI does not expose its declaration.** It receives the consumer's declaration and verifies it internally — returning only a verdict (tick, tick, tick → accepted). The brand's thresholds remain private. This reflects how a real brand would operate: exposing authority limits creates an attack surface.

4. **Return instructions are machine-structured, consumer-translated.** After the resolution, the brand AI sends structured return instructions. The consumer AI translates these into natural language and handles the logistics on the human's behalf.

5. **Visual language distinguishes human from machine.** Left pane = white background, WhatsApp-style bubbles (human conversation). Right pane = dark background, monospace font (machine-to-machine protocol). Both panes visible simultaneously.

---

## Layout

**Two-pane side-by-side layout** (stacks vertically on mobile):

| Left pane | Right pane |
|---|---|
| "Your Conversation" | "What happened next" |
| Human ↔ Consumer AI | Consumer Agent ↔ Brand Agent |
| White background | Dark navy (#1a1a2e) background |
| Chat bubbles | Monospace protocol messages |
| Human: right-aligned, teal | Consumer agent: left-aligned, dark teal |
| AI agent: left-aligned, grey | Brand agent: right-aligned, dark purple |

Below both panes: a full-width green resolution bar slides in at the end.

---

## Animation Sequence

### Left pane — Human ↔ Consumer AI

| Time | Speaker | Message |
|---|---|---|
| 0.5s | Human | "My delivery arrived damaged — I need help sorting it out" |
| 3s | Consumer AI | "I'll handle this. What would you like me to go for — full refund, replacement, or store credit?" |
| 7s | Human | "Full refund ideally. Replacement if that's not possible." |
| 10s | Consumer AI | "Got it. Anything you want me to rule out entirely?" |
| 13s | Human | "No partial refunds. No store credit." |
| 16s | Consumer AI | "Perfect. Attach a photo of the damage and I'll have everything I need." |
| 20s | Human | 📷 damage_photo.jpg |
| 24s | Consumer AI | "All set. I've built your Service Handshake declaration. Contacting the retailer now." |
| 48s | Consumer AI | "Sorted. Replacement approved — arriving within 2 business days. Reference: REF-4471-X." |
| 52s | Human | "Brilliant, thank you!" |
| 61s | Consumer AI | "One more thing — they need the damaged item back within 14 days. I can book a DPD pickup for you, or find your nearest drop-off. Which would you prefer?" |
| 66s | Human | "Pickup please." |
| 70s | Consumer AI | "Done. Pickup booked. Your returns label is on its way." |

### Right pane — Consumer Agent ↔ Brand Agent

| Time | Speaker | Message |
|---|---|---|
| 27s | Consumer Agent | SH DECLARATION SUBMITTED (Goals, Constraints, Evidence) |
| 33s | Brand Agent | VERIFYING SH DECLARATION... ✓ Request type within scope ✓ Constraints within policy ✓ Evidence sufficient |
| 40s | Brand Agent | SH DECLARATION ACCEPTED / Processing request... |
| 44s | Brand Agent | OUTCOME: Replacement approved / Ref: REF-4471-X / ETA: 2 business days |
| 56s | Brand Agent | RETURN INSTRUCTIONS (14 days, returns label URL, DPD or drop-off, packaging) |

### Resolution bar

| Time | Event |
|---|---|
| 76s | Full-width green bar: "✓ Resolved · Replacement dispatched · Return arranged · No human involvement required" |

---

## Service Handshake Declaration (Consumer Agent)

```
SH DECLARATION SUBMITTED
─────────────────────
Goals:       Full refund (preferred)
             Replacement (acceptable)
Constraints: No partial refund
             No store credit
Evidence:    damage_photo.jpg attached
```

## Brand Agent Verification

The brand does NOT share its declaration. It verifies the consumer's declaration internally:

```
VERIFYING SH DECLARATION...
✓  Request type within scope
✓  Constraints within policy
✓  Evidence sufficient
SH DECLARATION ACCEPTED
Processing request...
```

## Return Instructions (Brand Agent → Consumer Agent)

```
RETURN INSTRUCTIONS
─────────────────────
Return window:  14 days
Label:          returns.nwretail.com/REF-4471-X
Collection:     DPD pickup or drop-off
Packaging:      Any secure packaging
```

---

## Design Rationale: Why the Brand Doesn't Expose Its Declaration

A brand exposing its full authority declaration (e.g. "we auto-approve under £200 within 30 days") creates a gaming risk — consumer agents could optimise against known thresholds. The Service Handshake is designed so the brand verifies the consumer's declaration against its own internal policy without revealing what that policy is. The consumer agent only sees the verdict.

This mirrors how credit checks work: you get approved or declined without seeing the algorithm.

---

## Voice Narration

Voice ID: D7ue8wE6ek2ji78PnFiN (AI Maria voice, ElevenLabs)
Duration: 86 seconds
Model: eleven_turbo_v2_5

Full script — see Mode4-Voiceover-Script.txt

---

## Technical

- Self-contained HTML/CSS/JS (no external dependencies)
- All CSS prefixed `m4-`
- Audio: `./mode4-voiceover.mp3` — fails silently if missing
- Mobile: panes stack vertically with the human conversation first
- Full replay via "Watch again" button
- Lives at `/mode4/index.html` with the site nav and footer
