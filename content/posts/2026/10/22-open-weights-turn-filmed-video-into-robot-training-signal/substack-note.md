# Substack Note — open-weights-turn-filmed-video-into-robot-training-signal

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

Language models got good by reading the text people had already written, and robotics has always had an equivalent pile sitting in plain sight in the form of every hour of video anyone has filmed of hands doing things.

This week Jim Fan and the GEAR lab at NVIDIA open-sourced Flora, a suite of models that watches human and robot footage and writes down what happened, when it happened and how well it went, as timestamped captions, dense progress rewards and rubric scores. https://x.com/DrJimFan/status/2112597587987689912

Flora already labels 200,000 hours of video a day on 512 GPUs inside the pipeline that trains GR00T, and the team reports quality competitive with GPT-6 Astra at roughly 125 times lower cost. https://research.nvidia.com/labs/gear/flora/

Labeling has always been the expensive step between raw footage and usable training signal, and with open weights any lab sitting on a camera archive can now run that step on its own hardware. https://huggingface.co/collections/nvidia/flora

---

**Attach video:** media/flora-30s.mp4

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
