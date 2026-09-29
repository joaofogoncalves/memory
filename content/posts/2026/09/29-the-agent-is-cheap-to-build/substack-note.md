# Substack Note — the-agent-is-cheap-to-build

Paste into Substack Notes (substack.com/notes). No hashtags. Links welcome.

---

The agent is cheap to build now, and the products showing up around it are pricing what comes after the demo. AWS Bedrock AgentCore wraps an agent you already have in a microVM that lives for one session, up to eight hours, and is wiped when that session ends. Microsoft Foundry Hosted Agents take a container, attach a managed identity, and scale it to zero while it is idle. Aiven's Runtime, generally available since 23 September, is the data version of the same offer: you push a container and it runs next to the Postgres or Kafka you already operate, with Azure still marked as later. Google's Vertex AI Agent Engine prices the memory separately, as a short-term session plus a longer-term store.

The choice in front of a team is which of those costs to hand off: the credential, the session that has to be thrown away, the idle meter, or where the data sits while the agent is reading it.

The comparison of the three cloud runtimes: https://dreaming.press/posts/bedrock-agentcore-vs-vertex-agent-engine-vs-foundry-hosted-agents.html

Aiven's announcement: https://aiven.io/blog/deploy-your-apps-and-agents-where-your-data-lives-with-aiven-runtime

---

**Attach inline (in order):**
- media/image-1.webp (primary — shown above the fold)
- media/image-2.webp

Substack Notes supports multiple inline images. Paste the text first, then drag each image in at the cursor position where it should appear in the flow. If you want all images at the top (simplest), drag them in as a block before the first paragraph.

---

**After posting:** copy the Note URL and paste it into `post.md` as `substack_note_url:`.
