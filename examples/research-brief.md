# Example: Research Brief

```bash
redbot run research-brief \
  --topic "开源 AI Agent 工具趋势" \
  --audience "工程团队" \
  --context "关注 GitHub 开源项目、落地风险和下一步行动。" \
  --demo
```

Redbot writes two files:

- `redbot_workspace/artifacts/*.md`
- `redbot_workspace/traces/*.json`

The artifact is the publishable output. The trace is the execution record you can inspect, commit, or share.
