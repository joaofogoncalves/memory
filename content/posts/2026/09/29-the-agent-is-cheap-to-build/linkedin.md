# LinkedIn post — the-agent-is-cheap-to-build

Paste this directly into LinkedIn's composer. Zero emojis, 2-4 hashtags at the end.
Do **not** put external URLs in the body.

---

The agent is cheap to build now, and the products showing up around it are pricing what comes after the demo. Bedrock AgentCore from @Amazon Web Services wraps an agent you already have in a microVM that lives for one session, up to eight hours, and is wiped when that session ends. Foundry Hosted Agents from @Microsoft take a container, attach a managed identity, and scale it to zero while it is idle. Runtime from @Aiven, generally available since 23 September, is the data version of the same offer: you push a container and it runs next to the Postgres or Kafka you already operate, with Azure still marked as later. Vertex AI Agent Engine from @Google prices the memory separately, as a short-term session plus a longer-term store.

The choice in front of a team is which of those costs to hand off: the credential, the session that has to be thrown away, the idle meter, or where the data sits while the agent is reading it.

#AI #Agents

---

**Attach as a carousel (in order):**
- media/image-1.webp
- media/image-2.webp

LinkedIn renders 2+ images as a swipeable carousel. Order matters — image-1 is the feed thumbnail, and readers swipe left in sequence.

---

**First comment (post immediately after the main post goes live):**
The comparison of the three cloud runtimes:
https://dreaming.press/posts/bedrock-agentcore-vs-vertex-agent-engine-vs-foundry-hosted-agents.html

**Second comment:**
Aiven's announcement:
https://aiven.io/blog/deploy-your-apps-and-agents-where-your-data-lives-with-aiven-runtime

---

**After posting:** copy the LinkedIn permalink and paste it into `post.md` as `post_url:`.
