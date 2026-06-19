# Douyin Series Ideas

Use Redbot as a real open-source product, and mention your model gateway only as the interchangeable model backend.

## Episode 1: AI Intern

Hook: "I built an open-source AI intern that writes my research brief and leaves an execution trace."

Demo:

```bash
redbot run research-brief --topic "开源 AI Agent 项目趋势" --audience "科技博主" --context "找适合二创和拍视频的项目" --demo
```

Show:

- template list;
- generated artifact;
- trace JSON;
- switching from demo mode to a real Claude/GPT model endpoint.

## Episode 2: Script Factory

Hook: "Give it one topic, and it outputs a Douyin script with hook, shots, and ending question."

Demo:

```bash
redbot run short-video-script --topic "Claude 和 GPT 谁更适合写代码" --audience "AI 工具玩家" --context "要自然展示模型切换" --demo
```

## Episode 3: Open-Source Packaging

Hook: "Most GitHub projects lose stars because README is boring. I made Redbot write the first draft."

Demo:

```bash
redbot run github-readme --topic "Redbot 个人 AI 执行助理" --audience "GitHub 开源用户" --context "MIT 协议，支持 OpenAI-compatible API" --demo
```
