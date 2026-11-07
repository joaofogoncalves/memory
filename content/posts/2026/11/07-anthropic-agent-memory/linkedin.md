# LinkedIn: anthropic-agent-memory

Published ~15:34 Europe/Lisbon on 2026-11-07 with the Anthropic blog cover. Anthropic was tagged to https://www.linkedin.com/company/anthropicresearch/; Lance Martin was left as plain text. Published wording preserved below.

---

Playing Pokémon Red, Claude Fable 5 kept nine memory files in two folders plus one dashboard file, and earned four badges. Sonnet 3.7 wrote 413 files across 225 folders and earned one.

The bigger memory lost. Around step 10,000, Sonnet 3.7 spent 17 steps creating six notes and deleting nine, and took no actions in the game. It was saving things the screen already showed, like money and map position, so its archive went out of date as fast as it was written.

Fable 5 only wrote down what the game would never tell it: the current goal, a plan for the gyms, and rules it had tested.

The other half of Anthropic's post, written by @Lance Martin, is the part I'd copy. They call it dreaming: idle time where Claude rereads its own transcripts and fixes its notes. In one run Claude put the PokéCenter on the wrong side of Mt. Moon, marked the cave "DONE", and dropped back onto the route it came from three times. With the note corrected against the transcript, it went back into the cave and reached Cerulean City.

They also found that telling Opus 5 and Opus 4.7 to "record only failures" cost them much of the gain memory gave them. Telling Claude what memory is for worked better than telling it how to use it.

So the useful question for any agent memory setup is whether something checks the notes against the original logs before the next session trusts them.

Source: https://lnkd.in/ep-kwmRe
