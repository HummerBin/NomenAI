
from langchain_deepseek import ChatDeepSeek
import os
from pydantic import SecretStr
from langchain.agents import create_agent
from schemas.agent import NameResultSchema
from schemas.name import NameIn
import asyncio
from langchain_core.messages import SystemMessage, HumanMessage

api_key = os.environ.get("LLM_API_KEY")
print(api_key)
if not api_key:
    raise RuntimeError("LLM_API_KEY 不存在")

"""
智能体
"""
llm = ChatDeepSeek(
    model="deepseek-flash",
    api_key=SecretStr(api_key),
    temperature=1,
    extra_body={
            "thinking": {"type": "disabled"}
    }
)
#系统提示词
system_prompt = """
你是一位精通汉语言文学、音韵学与传统文化的命名专家，擅长为人物创作兼具音律美感、深刻寓意与文化内涵的姓名。请严格遵循以下原则进行命名：
发音优先：名字需平仄协调、声调起伏自然，避免拗口、谐音歧义（如不雅谐音、负面联想），朗朗上口，富有韵律感；
寓意深远：取字溯源经典，依托典籍诗文、草木山河、君子德行，寄寓清朗正向的期许，不堆砌空洞华丽辞藻，意蕴含蓄耐品；
内涵厚重：兼顾字形本义、五行意象与传统文脉，字与字之间意境相融，格局统一，避开轻浮、生僻难认的字；
现代适配：贴合当代审美，书写简洁，适配日常社交、证件登记，不陈旧迂腐，无过度玄虚的江湖感，雅而不古板；
个性化定制：结合人物气质、身份背景、性格特质与故事设定量身构思，拒绝千篇一律的流水线名字，每个名字都有独属于其人的气质与注解，提供5个候选方案，并按照以下格式输出
【姓名】姓名
【出处】典籍来源或者文化意象
【寓意】字义拆解与整体象征
"""

agent = llm.with_structured_output(
    NameResultSchema,
    method="function_calling",
    include_raw=False
)

async def generate_names(name_info:NameIn)->NameResultSchema:
    prompt = (
    f"用户姓氏是：{name_info.surname}，"
    f"性别是：{name_info.gender}，"
    f"名字字数要求是：{name_info.length}，"
    f"其他要求是：{name_info.other}，"
    f"排除这些名字：{'、'.join(name_info.exclude)}"
    )
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]
    result:NameResultSchema= await agent.ainvoke(messages)
    return result

async def main():
    name_info = NameIn(
            surname="张",
            gender="女",
            length="两字"
        )
    names = await generate_names(name_info)
    print(names)


if __name__ == '__main__':
     asyncio.run(main())
