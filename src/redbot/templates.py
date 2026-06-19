from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskTemplate:
    id: str
    name: str
    description: str
    deliverable: str
    system_prompt: str

    def build_prompt(self, topic: str, audience: str, context: str) -> str:
        return "\n".join(
            [
                self.system_prompt.strip(),
                "",
                f"主题: {topic.strip()}",
                f"目标读者/观众: {audience.strip()}",
                "背景资料:",
                context.strip() or "无额外背景。",
                "",
                "交付要求:",
                self.deliverable.strip(),
                "",
                "请使用中文输出。结构要清晰、可直接复制使用。不要编造无法确认的事实；不确定时标注需要验证。",
            ]
        )


TEMPLATES: tuple[TaskTemplate, ...] = (
    TaskTemplate(
        id="research-brief",
        name="深度研究简报",
        description="把一个主题整理成可执行的研究简报，适合选题、竞品和趋势分析。",
        deliverable=(
            "输出 Markdown 简报，包含: 1. 一句话结论; 2. 背景判断; 3. 三个可拍/可做角度; "
            "4. 风险与验证清单; 5. 下一步行动。"
        ),
        system_prompt=(
            "你是 Redbot 的研究助理，擅长把模糊主题变成适合创作者和小团队执行的研究简报。"
        ),
    ),
    TaskTemplate(
        id="short-video-script",
        name="短视频脚本",
        description="生成抖音/小红书/B站短视频脚本，强调开头钩子和演示节奏。",
        deliverable=(
            "输出 60-90 秒短视频脚本，包含: 开头 3 秒钩子、镜头分段、口播文案、屏幕演示点、"
            "自然的模型/工具说明、结尾互动问题。"
        ),
        system_prompt=(
            "你是 Redbot 的短视频策划助理，擅长把技术项目讲成普通人愿意看完的内容。"
        ),
    ),
    TaskTemplate(
        id="content-table",
        name="内容整理表格",
        description="把零散资料整理成表格，适合资料抓取、竞品收集和选题池。",
        deliverable=(
            "输出 Markdown 表格，列包含: 项目/素材、核心价值、适合人群、可拍点、二创空间、优先级。"
        ),
        system_prompt="你是 Redbot 的资料整理助理，擅长把混乱信息变成可筛选的结构化表格。",
    ),
    TaskTemplate(
        id="weekly-report",
        name="日报周报",
        description="把进展记录转成团队能看懂的日报/周报。",
        deliverable=(
            "输出周报，包含: 本周完成、关键进展、遇到的问题、下周计划、需要协作/决策的事项。"
        ),
        system_prompt="你是 Redbot 的项目汇报助理，擅长把流水账改写成清楚、有推进感的工作汇报。",
    ),
    TaskTemplate(
        id="github-readme",
        name="GitHub README",
        description="为开源项目生成有吸引力的 README 初稿。",
        deliverable=(
            "输出 README 初稿，包含: 项目一句话定位、特性、快速开始、使用场景、路线图、许可证说明。"
        ),
        system_prompt="你是 Redbot 的开源产品助理，擅长把项目包装成开发者愿意 star 的 GitHub 仓库。",
    ),
)


def list_templates() -> list[TaskTemplate]:
    return list(TEMPLATES)


def get_template(template_id: str) -> TaskTemplate:
    for template in TEMPLATES:
        if template.id == template_id:
            return template
    valid = ", ".join(template.id for template in TEMPLATES)
    raise KeyError(f"Unknown Redbot template: {template_id}. Valid templates: {valid}")
