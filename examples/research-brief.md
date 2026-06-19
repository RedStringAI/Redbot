# Example: Research Brief

```bash
redbot run research-brief \
  --topic "开源 AI Agent 工具趋势" \
  --audience "准备做抖音科技号的人" \
  --context "关注 GitHub 开源、二创空间、短视频传播点。" \
  --demo
```

Redbot writes two files:

- `redbot_workspace/artifacts/*.md`
- `redbot_workspace/traces/*.json`

The artifact is the publishable output. The trace is the execution record you can inspect, commit, or share.
