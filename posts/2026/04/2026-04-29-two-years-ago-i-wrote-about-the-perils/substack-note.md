# Substack Note — two-years-ago-i-wrote-about-the-perils

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

Two years ago I wrote about the perils of over-engineering. Heavy abstractions, premature microservices, solving problems that don't exist, picking technology for problems you don't have.

Reading it back, every bullet still fires. You just swap the vocabulary.

Heavy abstractions used to mean a factory pattern wrapped around a single function. Now it's an agent with five tools and a system prompt for a script that wanted to be 30 lines.

Solving problems that don't exist used to mean choosing a database for a billion records when you have three thousand. Now it's RAG over a 50-document knowledge base, when grep would be faster and more accurate.

Future-proofing your stack used to mean picking Kafka before you'd shipped v1. Now it's adopting an agentic framework before you've nailed the prompt that would have done the same job in one call.

Premature microservices used to mean six developers splitting a monolith. Now it's a five-agent swarm where one model with the right context would have closed the ticket.

Same disease, new vocabulary. Same treatment: solve the actual problem, then add complexity only when the problem demands it.

The agentic version just costs more per token to be wrong.

---

**Attach image:** media/image-1.webp

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
