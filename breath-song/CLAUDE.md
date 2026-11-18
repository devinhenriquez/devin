# Breath Song

A phone experience for Devin's NMDE class (final due **December 6**): **a song without words.** You play a short song with your face, an animal carries it to someone as a link, and they hear it and can answer with their own face. The class's projects are about communication (others did text in → emotion out, and a mail-like project), so on Nov 18, 2026 it was reframed from a solo "follow the song, get your animal" game into nonverbal messaging. It replaces the earlier two-phone game "Fog Call", which the professor and class didn't respond to. Inspired by the flute in Ghost of Tsushima.

## Flow
**Sender:** Begin → camera permission → **face scan** (about 4 s, live words like "soft eyes · chin up") → "The forest hears {mood} in you" → "Relax your face" (about 1.5 s; sets your flat pitch) → 4-tick count-in → **compose** (24 beats × 0.6 s ≈ 14 s) → the messenger animal arrives and plays your first bars in its own voice → **send screen** (To / From names, **Send it** = share sheet or copy link, **Show QR**, "Hear it as they will", "Play a new one").

**Receiver** (page opened with `#s=…`): "Devin sent you a song" → Listen → the messenger's scenery and silhouette paint in, and it plays the song while the ink line paints itself → "It carries longing." → card: "A song for Sam · The Crane · It carries longing. Devin misses you." → **Answer with your face** (runs the sender flow with To prefilled and the reply flag set; the receiver then sees "Sam answered your song") or Listen again.

## How composing works
- **Face = pitch, 5 notes.** Relaxed = middle, raised eyebrows = higher, **open mouth (or frown) = lower**. Frowning was hard for the user, so jawOpen is the main "low". The continuous value P (−1…1) maps to 5 levels with hysteresis, in a yo pentatonic scale (0, 2, 5, 7, 9 semitones). Face lost or no input = a rest. MediaPipe Face Landmarker blendshapes, loaded from jsDelivr at runtime.
- **A gentle beat:** soft wooden ticks (accent and a light taiko every 4), and a koto pluck of your current note on each beat. Your shakuhachi follows your face continuously, with vibrato that blooms when you hold a note.
- **The song is painted** as one ink line across the scroll (left→right = time, up/down = pitch), with jade strands and a soft wash, over five faint guides. Silences break the line. A red seal is stamped at the end.
- **Recorded as** 24 notes (each beat = the level held longest, or `-`) plus the ink line resampled to 8 points per beat (192 base-36 characters).

## The messenger (which animal carries it)
Half the scan expressions, half your expressions while composing, plus the song's shape (high → Crane/Owl, low → Bear, jumpy → Monkey/Fox, smooth and middle → Deer, many rests → Owl), then weighted luck (softmax, temperature 0.12). Your last messenger (`localStorage` `breathsong-last`) gets half weight. `#fox`, `#crane` and so on force it, for demos.

| Animal | Carries | Receiver reads | Plays on | Hints | Scenery |
|---|---|---|---|---|---|
| Monkey | joy | {who} wants to make you laugh. | shamisen | red maple leaves | maple branch |
| Bear | comfort | {who} wants you to feel safe. | flute | paw prints | red sun |
| Deer | tenderness | {who} is thinking of you gently. | koto | bamboo leaves | bamboo |
| Fox | mischief | {who} has a secret smile for you. | shamisen | foxfire | red torii |
| Owl | wonder | {who} has been thinking about you. | flute | feathers | moon |
| Cat | pride | {who} is proud of you. | koto | paw prints | temple roof |
| Crane | longing | {who} misses you. | flute | feathers | reeds and water |

Illustrations are hand-written SVG silhouettes in `ANIMALS[k].art` (200 x 200 box), given a sumi-e look by an SVG filter. Haiku, `sig` and `step` fields in `ANIMALS` are left over from the game version.

## The link
`https://devinhenriquez.github.io/devin/breath-song/#s=<base64url JSON>` with `{a, n, c, to?, fr?, re?}`, about 410 characters. The whole song lives in the link, so there's no server; GitHub Pages is enough. Links always point at the published page, even when made from a local file. Names are capped at 24 characters, and the sender's own name is remembered (`breathsong-from`). Incoming links are validated (known animal, `^[0-4-]{24}$` notes, base-36 line). QR codes come from `qrcode-generator@1.4.4` on jsDelivr, loaded only when asked. **Privacy:** only the song, the animal and optional first names are sent; nothing from the camera leaves the phone.

## Sound
All synthesized: a shakuhachi-like flute (you), Karplus-Strong koto and buzzy shamisen plucks, a shō-like drone cluster that changes key to the messenger's root, taiko, wooden ticks, wind and a wooden-hall reverb. No MP3s.

## Other inputs
Press and drag up/down, arrow keys, a PlayStation/Xbox left stick, or the Arduino flute (`../BreathSongFlute/`, Leonardo as a gamepad: Y axis = pitch). A / Cross = Begin, or Answer on a received song. `?debug` shows live face readings, and `?projector` enlarges everything for a classroom screen.

## Files
- `src/app.html` — **edit this.** The whole page (HTML, CSS, JS).
- `tools/build.py` — copies it to `index.html`. **Run `python3 tools/build.py` after every edit.**
- `index.html` — the built page (about 73 KB). Don't hand-edit it.
- `archive/app-follow-the-song.html` — the previous version (continuous follow-the-threads song, two-animal race, reveal, saved scroll), kept in case parts are wanted back.
- `songs/`, `tools/analyze.py`, `tools/cut-reference.py` — left over from the soundtrack version; not used.

## Design
Sumi-e ink on aged parchment (reference: the ink-painting style of Ghost of Yotei's story cutscenes; matched in style only, no images copied). Tokens: --paper #E6D5B2, --paper2 #CDB289, --ink #221B14, --ink2 #5C4A35, --seal #A8322A (red hanko accent), threads rgba(38,92,72). The background and each animal's scenery are painted once per resize into offscreen canvases. Shippori Mincho for display text, Zen Kaku Gothic New for body text.

## Hosting
GitHub Pages: https://devinhenriquez.github.io/devin/breath-song/ (the repo must be public with Pages on main / root). The camera only works over https, so the page can't run as a Claude artifact. A QR poster is in `qr-poster.png`.

## Figma
https://www.figma.com/design/3bPFcSOgtjLKGhhHypBOof holds static screens of the **previous** (follow-the-song) version, made by rendering the page headlessly and importing with the Figma MCP's html_to_figma. Re-export for the messaging version.

## Ideas discussed, not built yet
- An ink-drawn face in the corner (built from the face landmarks) instead of the live camera during composing.
- A classroom "forest wall" projector page.
- Arduino flute: parts still to buy are the MPU6050 (tilt) and a coin vibration motor.
- Renaming: there's no breathing any more, so "Breath Song" may not fit.

## Working notes
- Test in desktop Chrome. Opening `index.html` directly works with the camera (add `?debug` to tune). Test links by pasting the `#s=…` part after the local file path.
- iPhone: Safari over GitHub Pages only.
- Keep it smooth on phones: canvas DPR is capped at 2, the background and scenery are pre-rendered, the silhouette bleed is a clip of about 50 circles, there's no shadowBlur, and the face is read about 20 times a second.
- Clocks use `ac.currentTime - G.c0`, so tests can fast-forward by lowering `G.c0`.
- Claude's browser pane opens `index.html` as a data: URL, so hashes, `history.replaceState` (guarded) and the camera don't work there; the gamepad API also throws there (guarded).
