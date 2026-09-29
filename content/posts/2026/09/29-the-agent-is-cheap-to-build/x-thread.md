# X post — the-agent-is-cheap-to-build

Paste into X manually. No hashtags.

---

**Main post:**
The agent is cheap to build now, and the products showing up around it are pricing what comes after the demo. AWS Bedrock AgentCore wraps an agent you already have in a microVM that lives for one session, up to eight hours, and is wiped when that session ends. Microsoft Foundry Hosted Agents take a container, attach a managed identity, and scale it to zero while it is idle. Aiven's Runtime, generally available since 23 September, is the data version of the same offer: you push a container and it runs next to the Postgres or Kafka you already operate, with Azure still marked as later. Google's Vertex AI Agent Engine prices the memory separately, as a short-term session plus a longer-term store.

The choice in front of a team is which of those costs to hand off: the credential, the session that has to be thrown away, the idle meter, or where the data sits while the agent is reading it.
*Attach: media/image-1.webp, media/image-2.webp*

**Reply 1 (to main post):**
The comparison of the three cloud runtimes:
https://dreaming.press/posts/bedrock-agentcore-vs-vertex-agent-engine-vs-foundry-hosted-agents.html

**Reply 2 (to reply 1):**
Aiven's announcement:
https://aiven.io/blog/deploy-your-apps-and-agents-where-your-data-lives-with-aiven-runtime

---

**After posting:** copy the X permalink (of the main post) and paste it into `post.md` as `x_url:`.
