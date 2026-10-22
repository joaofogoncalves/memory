---
date: 2026-10-22
post_type: original
authored: true
post_url: "https://www.linkedin.com/feed/update/urn:li:ugcPost:7518945521659625472/"
x_url: "https://x.com/joaofogoncalves/status/2113181337939014073"
substack_note_url: "https://substack.com/@joaofogoncalves/note/c-367237859"
tags: [ai, robotics, physical-ai, open-source]
source_urls:
  - https://x.com/DrJimFan/status/2112597587987689912
  - https://research.nvidia.com/labs/gear/flora/
  - https://huggingface.co/collections/nvidia/flora
angle: "Language models learned from text people already wrote; Flora is a step toward robots learning the same way from video people already filmed, and open labeling weights make that footage training signal for anyone"
template: short-form
media: media/flora-30s.mp4
---

Language models got good by reading the text people had already written, and robotics has always had an equivalent pile sitting in plain sight in the form of every hour of video anyone has filmed of hands doing things.

This week Jim Fan and the GEAR lab at NVIDIA open-sourced Flora, a suite of models that watches human and robot footage and writes down what happened, when it happened and how well it went, as timestamped captions, dense progress rewards and rubric scores.

Flora already labels 200,000 hours of video a day on 512 GPUs inside the pipeline that trains GR00T, and the team reports quality competitive with GPT-6 Astra at roughly 125 times lower cost.

Labeling has always been the expensive step between raw footage and usable training signal, and with open weights any lab sitting on a camera archive can now run that step on its own hardware.

#AI #Robotics
