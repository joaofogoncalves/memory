# LinkedIn: micro1-dual-arm-sim-false-success

Published with micro1's 37-second video clip attached (the same clip X shows through the quote; the clip is not stored in the repo). micro1, NVIDIA, Neuralink (first mention, paragraph 4) and Cleo Abram (first mention, paragraph 4) are LinkedIn @ mentions in the published post, written here as plain names. The 1.5 second per thread figure is Cleo Abram's narration in the episode, not a Neuralink statement. Source links at the end of the body; they show as shortened LinkedIn links when published.

---

Ten frontier AI models controlled a surgical robot in a simulated operating room across 800 trials, and only 11 runs finished the task.

That is the Dual-Arm Sim benchmark from micro1, a self-published test. Each model got the same two-armed robot in NVIDIA Isaac Sim, four tasks such as swapping an instrument and packing a surgical kit, and no training for it. Gemini 4 Argon finished 9 trials and GPT-6 Astra finished 2. The other eight models finished none.

The number I keep thinking about is 213. In 213 trials the model said the task was complete, and in every one of them it was wrong. In 94 of those the robot had never touched the object.

Compare that with the robot Neuralink showed on camera this week in Cleo Abram's new episode. It is built for one surgical step, placing electrode threads, and Cleo says each thread takes about 1.5 seconds, with cameras and sensors tracking the brain surface as it goes. Neuralink's devices are still investigational, but the design is clear: one narrow machine, one job, checked as it works.

I think robots reach medicine that way, as narrow machines with checked steps, while general models learn the less glamorous skill of saying "I did not do it." A benchmark that counts false claims is how that gets measured, and I am glad someone built one.

Source: micro1's Dual-Arm Sim page https://www.micro1.ai/benchmark/dual-arm-sim and Cleo Abram's episode https://www.youtube.com/watch?v=Vna0hkq7U1g
